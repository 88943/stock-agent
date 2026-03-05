import time
from news_collector import get_news
from market_analyzer import analyze_market
from sector_mapper import get_sector_stocks
from leader_selector import select_leader
from strategy_engine import generate_strategy, save_strategy

time.sleep(2)

print("AI财经系统启动\n")

# 1) 新闻
news = get_news()

# 2) 热点板块评分
hot_sectors = analyze_market(news)

# 3) 行业板块 -> 成分股
sector_stocks = get_sector_stocks(hot_sectors, top_n=10)

# 4) 龙头股评分（只拉一次行情）
leaders, leader_detail = select_leader(sector_stocks, top_k=1)

# 5) 策略 & 保存
strategies = generate_strategy(leaders)
save_strategy(strategies)