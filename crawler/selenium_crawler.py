from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def start_browser(headless: bool = True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
     # Thêm các tùy chọn để bỏ qua lỗi SSL
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--allow-insecure-localhost')
    
    # Thêm User-Agent để giả lập trình duyệt thông thường
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')
    
    # Thêm các tùy chọn để bật JavaScript
    options.add_argument('--enable-javascript')
    
    # Tắt các tính năng bảo mật có thể gây ra vấn đề
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    return driver

def fetch_html(driver, url: str) -> str:
    driver.get(url)
    return driver.page_source

def close_browser(driver):
    driver.quit()
