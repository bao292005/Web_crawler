from bs4 import BeautifulSoup

def extract_by_class(html: str, class_name: str):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all(class_=class_name)

def extract_by_selectors(html: str, selectors: dict):
    soup = BeautifulSoup(html, "html.parser")
    data = {}
    for key, selector in selectors.items():
        elem = soup.select_one(selector)
        data[key] = elem.get_text(strip=True) if elem else None
    return data
