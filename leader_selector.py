import time
import akshare as ak


def _safe_float(v, default=0.0):
    try:
        if v is None:
            return default
        s = str(v).strip()
        if s in ("", "-", "None", "nan", "NaN"):
            return default
        # 有些字段可能带百分号或逗号
        s = s.replace("%", "").replace(",", "")
        return float(s)
    except Exception:
        return default


def _fetch_spot_with_retry(max_retry=3, sleep_s=1.2):
    """
    拉一次全市场实时行情（东方财富），带重试与退避
    如果东方财富接口失败，切换到备用接口
    """
    last_err = None
    for i in range(max_retry):
        try:
            # 首先尝试获取全市场实时行情
            print("尝试获取实时行情...")
            return ak.stock_zh_a_spot_em()
        except Exception as e:
            last_err = e
            print(f"获取实时行情失败，第 {i+1} 次重试: {e}")
            time.sleep(sleep_s * (i + 1))
    
    # 如果尝试多次失败，使用备用接口
    print("尝试备用行情接口...")
    try:
        return ak.stock_zh_a_hist(symbol="000001", period="daily")
    except Exception as e:
        print(f"备用接口获取失败: {e}")
        raise last_err


def select_leader(sector_stocks, top_k=1, max_retry=3):
    """
    sector_stocks: dict[str, list[str]]
      例如 {"食品饮料": ["贵州茅台", "五粮液", ...]}

    返回：
      leaders: dict[str, str]
      leader_detail: dict[str, list[dict]]  # 方便你后面做报告
    """
    print("\n===== 龙头股评分 =====")

    leaders = {}
    leader_detail = {}

    # 1) 只获取一次行情（关键优化：避免频繁请求）
    try:
        spot = _fetch_spot_with_retry(max_retry=max_retry)
    except Exception as e:
        print("龙头识别失败: 获取实时行情失败 ->", e)
        return leaders, leader_detail

    # 做个索引：名称 -> 行
    # 注意：不同接口字段名偶尔变化，这里尽量兼容常见列名
    name_col = "名称" if "名称" in spot.columns else None
    if name_col is None:
        print("龙头识别失败: 行情表缺少「名称」列，无法匹配个股")
        return leaders, leader_detail

    # 常见列：涨跌幅、换手率、成交额
    pct_col = "涨跌幅" if "涨跌幅" in spot.columns else None
    turnover_col = "换手率" if "换手率" in spot.columns else None
    amount_col = "成交额" if "成交额" in spot.columns else None

    spot_map = {}
    for _, r in spot.iterrows():
        spot_map[str(r[name_col]).strip()] = r

    # 2) 对每个板块成分股打分
    for sector, stocks in sector_stocks.items():
        print("\n分析板块:", sector)

        scores = []
        for name in stocks:
            r = spot_map.get(str(name).strip())
            if r is None:
                continue

            pct = _safe_float(r[pct_col]) if pct_col else 0.0
            turnover = _safe_float(r[turnover_col]) if turnover_col else 0.0
            amount = _safe_float(r[amount_col]) if amount_col else 0.0

            # 简单稳定的评分（你后面可以再调权重）
            # 成交额用“亿”为单位缩放，避免数值太大
            score = pct * 0.5 + turnover * 0.3 + (amount / 1e8) * 0.2

            scores.append({
                "name": name,
                "score": score,
                "pct": pct,
                "turnover": turnover,
                "amount": amount,
            })

        if not scores:
            print("本板块没有匹配到行情数据（可能名称不一致或接口波动）")
            continue

        scores.sort(key=lambda x: x["score"], reverse=True)

        # 选 top_k（默认 1 个龙头）
        leader_list = scores[:top_k]
        leader_detail[sector] = leader_list

        leaders[sector] = leader_list[0]["name"]
        print("龙头股:", leaders[sector])

        # 打印前几名
        for item in leader_list[:3]:
            print(
                f"  {item['name']} | score={item['score']:.2f} | 涨幅={item['pct']:.2f} | 换手={item['turnover']:.2f} | 成交额={item['amount']:.0f}"
            )

        # 轻微限速（板块级别）
        time.sleep(0.4)

    return leaders, leader_detail