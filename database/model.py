import psycopg2
import psycopg2.extras
import os

def connect_db():
    """Kết nối đến PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
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