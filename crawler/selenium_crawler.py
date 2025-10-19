from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time

def start_browser(headless: bool = True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    
    # Tối ưu hóa performance
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")  # Không tải hình ảnh để nhanh hơn
    options.add_argument("--disable-javascript")  # Tắt JS nếu không cần thiết
    
    # Bỏ qua lỗi SSL
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    # User-Agent
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')
    
    # Tối ưu memory
    options.add_argument("--memory-pressure-off")
    options.add_argument("--max_old_space_size=4096")

    driver = webdriver.Chrome(options=options)
    
    # Timeout ngắn hơn
    driver.set_page_load_timeout(20)
    driver.implicitly_wait(5)
    return driver

def fetch_html_optimized(driver, url: str, wait_for_element=None, max_retries=3) -> str:
    """
    Lấy HTML với các tối ưu hóa:
    - Retry mechanism
    - Wait for specific elements
    - Performance monitoring
    """
    for attempt in range(max_retries):
        try:
            start_time = time.time()
            print(f"[INFO] Attempt {attempt + 1}/{max_retries} - Loading: {url}")
            
            driver.get(url)
            
            # Đợi element cụ thể load xong (nếu có)
            if wait_for_element:
                wait = WebDriverWait(driver, 10)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_element)))
                print(f"[INFO] Element '{wait_for_element}' đã load")
            
            # Đợi DOM load hoàn tất
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            page_source = driver.page_source
            load_time = time.time() - start_time
            
            print(f"[SUCCESS] Loaded {url} in {load_time:.2f}s - HTML: {len(page_source)} chars")
            return page_source
            
        except TimeoutException:
            print(f"[WARNING] Timeout on attempt {attempt + 1} for {url}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Đợi trước khi retry
                continue
            else:
                print(f"[ERROR] Max retries reached for {url}")
                return ""
                
        except Exception as e:
            print(f"[ERROR] Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            else:
                return ""
    
    return ""

def fetch_html(driver, url: str) -> str:
    return fetch_html_optimized(driver, url)

def close_browser(driver):
    try:
        driver.quit()
    except:
        pass
