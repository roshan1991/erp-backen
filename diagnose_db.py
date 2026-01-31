import socket
import psycopg2
import pymysql
import sys

def check_port(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, port))
        s.close()
        return True
    except:
        return False

def check_postgres(host, port, user, password, db):
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=db,
            connect_timeout=2
        )
        conn.close()
        return "SUCCESS"
    except Exception as e:
        return f"FAILED: {e}"

def check_mysql(host, port, user, password, db):
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db,
            connect_timeout=2
        )
        conn.close()
        return "SUCCESS"
    except Exception as e:
        return f"FAILED: {e}"

print("--- DIAGNOSTIC START ---")
# 1. Check open ports
ports = [5432, 5433, 3306]
for p in ports:
    status = "OPEN" if check_port("127.0.0.1", p) else "CLOSED"
    print(f"Port 127.0.0.1:{p} is {status}")

# 2. Try to connect to Postgres on found ports
pg_user = "postgres"
pg_pass = "SysAdmin@123"
pg_db = "erp_db"

if check_port("127.0.0.1", 5432):
    print(f"Attempting Postgres connection on 5432...")
    print(check_postgres("127.0.0.1", 5432, pg_user, pg_pass, pg_db))

if check_port("127.0.0.1", 5433):
    print(f"Attempting Postgres connection on 5433...")
    print(check_postgres("127.0.0.1", 5433, pg_user, pg_pass, pg_db))

print("--- DIAGNOSTIC END ---")
