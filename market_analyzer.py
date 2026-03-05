def analyze_market(news_list):

    print("\n===== AI热点分析 =====")

    sectors = {
        "AI": ["AI", "算力", "人工智能", "大模型", "机器人"],
        "芯片": ["芯片", "半导体", "GPU"],
        "新能源": ["新能源", "锂电", "光伏", "储能"],
        "消费": ["消费", "食品", "白酒", "零食"],
        "汽车": ["汽车", "新能源车"],
        "电力": ["电力", "发电"],
        "金融": ["银行", "券商", "保险"]
    }

    sector_score = {}

    # 遍历新闻
    for news in news_list:

        title = news["title"]

        print("分析新闻:", title)

        # 遍历板块
        for sector, keywords in sectors.items():

            for k in keywords:

                if k in title:

                    sector_score[sector] = sector_score.get(sector, 0) + 1

    if not sector_score:

        print("未识别热点板块")
        return []

    print("\n===== 热点板块评分 =====")

    sorted_sectors = sorted(
        sector_score.items(),
        key=lambda x: x[1],
        reverse=True
    )

    result = []

    for sector, score in sorted_sectors:

        print("热点板块:", sector, "热度:", score)

        result.append({
            "sector": sector,
            "score": score
        })

    return result