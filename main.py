from crawler.selenium_crawler import start_browser, fetch_html, close_browser
from crawler.extractor import extract_by_class, extract_by_selectors
from crawler.pipeline import save_to_json

def run():
    driver = start_browser(headless=False)

    url = "https://www.droidviews.com/mythic-without-stress-how-wow-boosting-really-helps-in-the-war-within/"
    html = fetch_html(driver, url)
    if not html:
        print("Không thể tải trang web. Đang đóng trình duyệt...")
        close_browser(driver)
        return
    # Lấy danh sách elements theo class
    elements = extract_by_class(html, "postsmod1-details")
    print(f"Tìm thấy {len(elements)} elements")

    # Lấy theo selectors chi tiết
    selectors = {
        "title": "h1.entry-title",
        "content": "div.entry-content"
    }
    data = extract_by_selectors(html, selectors)
    print(data)

    save_to_json(data, "output.json")

    close_browser(driver)

if __name__ == "__main__":
    run()
