import json


def generate_strategy(leaders):

    print("\n===== AI交易策略 =====")

    strategies = {}

    for sector, stock in leaders.items():

        strategy = {
            "leader": stock,
            "action": "观察",
            "reason": "热点板块龙头股，关注回调机会"
        }

        print("\n板块:", sector)
        print("龙头股:", stock)
        print("策略:", strategy["action"])

        strategies[sector] = strategy

    return strategies


def save_strategy(strategies):

    with open("trade_report.json", "w", encoding="utf-8") as f:

        json.dump(strategies, f, ensure_ascii=False, indent=2)

    print("\n交易报告已保存 -> trade_report.json")