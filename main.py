from crawler.selenium_crawler import start_browser, fetch_html, close_browser
from crawler.extractor import extract_by_class, extract_by_selectors, extract_multiple_items
from crawler.pipeline import save_to_json
import time
from database.model import connect_db,close_db


def run():
    connect_db()
    # close_db()
    driver = start_browser(headless=False)

    url = "https://www.droidviews.com/"
    html = fetch_html(driver, url)
    if not html:
        print("Không thể tải trang web. Đang đóng trình duyệt...")
        close_browser(driver)
        return
    # Lấy danh sách elements theo class
    elements = extract_by_class(html, "postsmod1-details")
    print(f"Tìm thấy {len(elements)} elements")

    # Lấy theo selectors chi tiết
    container_selector = ".postsmod1-details"
    selectors = {
        "title": "h3.entry-title",
        "author": "span.postsmod1-author-name a",
        "excerpt": "div.postsmod1-excerpt"
    }
    data = extract_by_selectors(html, selectors)
    # print(data)

       # Trích xuất tất cả các item
    all_items = extract_multiple_items(html, container_selector, selectors)
    print(f"Đã crawl được {len(all_items)} items")
    
    # In ra một vài item đầu tiên để kiểm tra
    for i, item in enumerate(all_items[:3], 1):
        print(f"Item {i}:")
        for key, value in item.items():
            print(f"  {key}: {value}")
    
    # Lưu tất cả dữ liệu vào file JSON
    save_to_json(all_items, "output.json")

    close_browser(driver)

if __name__ == "__main__":
    run()
