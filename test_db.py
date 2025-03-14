import psycopg2
from psycopg2 import OperationalError

def test_connection():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="root",
            password="gpFs9JiscHRZYqdIG2KmuOjR",
            host="logan.liara.cloud",
            port="33282",
            connect_timeout=10
        )
        print("اتصال به دیتابیس موفقیت‌آمیز بود!")
        conn.close()
    except OperationalError as e:
        print(f"خطا در اتصال به دیتابیس: {e}")

if __name__ == "__main__":
    test_connection() 