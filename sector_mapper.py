import time
from data_provider import get_industry_boards, get_board_stocks


def get_sector_stocks(hot_sectors, top_n=10):
    """
    hot_sectors: list[dict] 例如 [{"sector":"消费","score":3}, ...]
    返回：dict[行业板块名, list[股票名称]]
    """

    print("\n===== 行业板块识别 =====")

    result = {}

    # 获取行业板块列表
    boards = get_industry_boards()

    if boards is None:
        print("板块识别失败: 获取行业板块列表失败")
        return result

    # 判断列名
    col = None
    if "板块名称" in boards.columns:
        col = "板块名称"
    elif "名称" in boards.columns:
        col = "名称"

    if col is None:
        print("板块识别失败: 行业板块列表缺少「板块名称」列")
        return result

    for item in hot_sectors:

        sector_name = item.get("sector", "")

        if not sector_name:
            continue

        print("\n分析热点:", sector_name)

        # 匹配行业板块
        matched = boards[boards[col].astype(str).str.contains(sector_name, na=False)]

        if matched.empty:
            print("未找到行业板块匹配")
            continue

        board_name = matched.iloc[0][col]

        print("匹配行业板块:", board_name)

        # 获取板块成分股
        cons = get_board_stocks(board_name)

        if cons is None:
            print("板块识别失败: 获取成分股失败")
            continue

        name_col = "名称" if "名称" in cons.columns else None

        if name_col is None:
            print("板块识别失败: 成分股表缺少「名称」列")
            continue

        stocks = cons[name_col].head(top_n).tolist()

        print("板块成分股(前{}):".format(min(top_n, len(stocks))))

        for s in stocks[:min(10, len(stocks))]:
            print(" ", s)

        result[board_name] = stocks

        # 限速
        time.sleep(1)

    return result
