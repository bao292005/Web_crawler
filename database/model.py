import psycopg2
import psycopg2.extras
from config import DB_CONFIG

def connect_db():
    """Kết nối đến PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        # Tạo cursor với option RealDictCursor để trả về kết quả dạng dictionary
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        print("[INFO] Kết nối database thành công")
        return conn, cur
    except Exception as e:
        print(f"[ERROR] Lỗi kết nối database: {e}")
        return None, None

def close_db(conn, cur):
    """Đóng kết nối database"""
    if cur:
        cur.close()
    if conn:
        conn.close()
        print("[INFO] Đã đóng kết nối database")