import json
from pprint import pprint
from extract_data import extract_data
from utils import get_driver, close_driver

# link = "https://book.myagentgenie.com/swift/cruise/package/1582430--3-day-comedy-getaway?siid=1117792&lang=1"

driver = get_driver()

with open("links.json", "r", encoding="utf-8") as f:
    links = json.load(f)

datas = []

for link in links["url"]:
    data = extract_data(driver, link)
    datas.append(data.dict())

close_driver(driver)

pprint(datas)

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(datas, f, indent=2)

