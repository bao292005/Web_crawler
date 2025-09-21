from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
def start_browser(headless: bool = True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
     # Thêm các tùy chọn để bỏ qua lỗi SSL
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    
    # Thêm User-Agent để giả lập trình duyệt thông thường
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')
    
    # Thêm các tùy chọn để bật JavaScript
    options.add_argument('--enable-javascript')
    
    # Tắt các tính năng bảo mật có thể gây ra vấn đề
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    

    driver = webdriver.Chrome(options=options)
    # print(driver.capabilities["browserName"])
    # print(driver.capabilities["browserVersion"])
    # print(driver.capabilities["chrome"]["chromedriverVersion"])
    # print(driver.capabilities["platformName"])
    
    # Thiết lập timeout dài hơn
    driver.set_page_load_timeout(60)
    return driver

def fetch_html(driver, url: str) -> str:
    try:
        driver.get(url)
        print(f"[INFO] Load {url} thành công")
        return driver.page_source
    except Exception as e:
        print(f"[ERROR] Lỗi khi load {url}: {e}")
        # Nếu cần in stack trace chi tiết
        import traceback
        traceback.print_exc()
        return ""

def close_browser(driver):
    driver.quit()
