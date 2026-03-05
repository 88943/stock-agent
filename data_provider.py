import akshare as ak
import time
import json


def retry(func, max_retry=5, sleep=3, **kwargs):
    last_err = None
    for i in range(max_retry):
        try:
            return func(**kwargs)
        except Exception as e:
            last_err = e
            print(f"接口失败，重试: {i+1} -> {e}")
            time.sleep(sleep * (i + 1))  # 每次重试延迟增加
    return None


def get_spot_data():
    """
    获取全市场行情 -> 只保留涨幅排行前 top_n
    """
    print("尝试获取实时行情(全市场)...")

    try:
        df = retry(ak.stock_zh_a_spot_em)
        return df
    except Exception as e:
        print(f"东方财富获取失败: {e}")
        print("尝试备用接口...")

    try:
        # 使用新浪接口作为备用
        df = ak.stock_zh_a_hist(symbol="000001", period="daily")
        return df
    except Exception as e:
        print(f"备用接口获取失败: {e}")
    return None


def get_industry_boards():
    """
    获取行业板块列表，第一次获取后保存到本地，下次直接读取
    """
    try:
        # 如果缓存文件存在，直接读取
        with open("industry_boards.json", "r", encoding="utf-8") as f:
            df_dict = json.load(f)
            df = pd.DataFrame.from_dict(df_dict)
            return df
    except FileNotFoundError:
        pass  # 如果缓存文件不存在，继续请求接口

    print("尝试获取行业板块列表...")
    try:
        df = ak.stock_board_industry_name_em()
        # 将行业板块数据缓存到本地文件
        with open("industry_boards.json", "w", encoding="utf-8") as f:
            json.dump(df.to_dict(), f, ensure_ascii=False)  # 保存为JSON格式
        return df
    except Exception as e:
        print(f"获取行业板块列表失败: {e}")
        return None


def get_board_stocks(board_name):
    """
    获取板块的成分股列表
    """
    print(f"获取板块成分股: {board_name}...")
    try:
        df = ak.stock_board_industry_cons_em(symbol=board_name)
        return df
    except Exception as e:
        print(f"获取板块成分股失败: {e}")
        return None
    