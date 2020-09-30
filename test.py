from dc_crawler import DCinsideCrawler
import json

# crawler.get_data(1, 1)
crawler = DCinsideCrawler()
info = crawler.get_data(330000, 330000)

print(json.dumps(info, ensure_ascii=False, indent=4))

with open("./dc_crawling.json", "w", encoding="UTF-8") as f:
    json.dump(info, f, ensure_ascii=False, indent="\t")
    