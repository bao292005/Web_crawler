from crawler.selenium_crawler import start_browser, fetch_html, close_browser
from crawler.extractor import extract_multiple_items
from crawler.pipeline import save_to_json
import time
from database.model import get_items, create_items
import json

def get_unique_urls(crawl_sites):
    urls = []
    for item in crawl_sites:
        urls.append(item['URL'])
    return list(set(urls))

def run():
    crawl_sites = get_items("crawl_sites")
    print(crawl_sites)
    unique_urls = get_unique_urls(crawl_sites)
    for url in unique_urls:
        driver = start_browser(headless=False)
        html = fetch_html(driver, url)
        if not html:
            print("Không thể tải trang web. Đang đóng trình duyệt...")
            close_browser(driver)
            return

        for item in crawl_sites:
            if item['URL'] == url:
                all_items = extract_multiple_items(html, item['container_selector'], item['css_selectors'])
                print(f"Đã crawl được {len(all_items)} items từ {url}")
                # Lưu tất cả dữ liệu vào file JSON
                filename = f"output_{item['site_name']}.json"
                save_to_json(all_items, filename)
        close_browser(driver)

    # with open("output.json", "r", encoding="utf-8") as f:
    #     data = json.load(f)
    # create_items("data_crawled", data)

if __name__ == "__main__":
    run()
