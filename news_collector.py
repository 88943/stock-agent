import akshare as ak

def get_news(limit=10):

    print("\n===== 最新财经新闻 =====")

    df = ak.stock_news_em()

    df = df.head(limit)

    news_list = []

    for _, row in df.iterrows():

        item = {
            "title": row["新闻标题"],
            "source": row["文章来源"],
            "time": row["发布时间"]
        }

        news_list.append(item)

        print("标题:", item["title"])
        print("来源:", item["source"])
        print("时间:", item["time"])
        print("------")

    return news_list