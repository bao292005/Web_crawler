from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Mở Chrome
# options = Options()
# options.add_argument("--headless")
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()

driver.get("https://www.droidviews.com/")

# Lấy toàn bộ HTML của trang
html = driver.page_source
# # Dùng BeautifulSoup để phân tích
soup = BeautifulSoup(html, "html.parser")

elements = []
# In ra tất cả CSS selectors + nội dung text
for elem in soup.find_all(True):  # True = lấy tất cả các tag
    if "postsmod1-details" in elem.get("class", []):
        elements.append(elem)

print(elements)

driver.close()
