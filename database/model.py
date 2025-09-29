import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Config lấy từ .env
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("DIRECTUS_API_KEY")
HEADERS = None  # headers sẽ lưu sau khi xác thực


def authenticate():
    """Xác thực với Directus API"""
    global HEADERS

    if API_KEY:
        # Sử dụng API key
        HEADERS = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        return True
    return False


def get_items(collection, params=None):
    """Lấy dữ liệu từ collection"""
    if not HEADERS:
        if not authenticate():
            return None
        
    url = f"{BASE_URL}/items/{collection}"
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        print(f"[ERROR] Lỗi khi lấy dữ liệu từ collection {collection}: {e}")
        return None


def create_items(collection, items):
    """Tạo nhiều items trong collection"""
    if not HEADERS:
        if not authenticate():
            return None

    url = f"{BASE_URL}/items/{collection}"
    try:
        response = requests.post(url, headers=HEADERS, json=items)
        response.raise_for_status()
        print(f"[INFO] Đã tạo {len(items)} items trong collection {collection}")
        return response.json().get("data", [])
    except Exception as e:
        print(f"[ERROR] Lỗi khi tạo items trong collection {collection}: {e}")
        return None


def connect_db():
    """Kết nối đến Directus API"""
    if authenticate():
        print("[INFO] Kết nối đến Directus API thành công")
        return True
    print("[ERROR] Kết nối đến Directus API thất bại")
    return False


def close_db():
    """Không cần đóng kết nối với API"""
    pass
