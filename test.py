from dc_crawler import DCinsideCrawler
import json

# crawler.get_data(1, 1)
crawler = DCinsideCrawler()
crawler.save_data('./output/dc_crawling50000.json', 65001, 100001)

