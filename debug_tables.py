import pymysql
import sys

try:
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='SysAdmin@123',
        database='erp_db'
    )
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    with open("tables_output.txt", "w") as f:
        for table in tables:
            f.write(f"{table[0]}\n")
            
    print("Successfully wrote tables to tables_output.txt")
except Exception as e:
    with open("tables_output.txt", "w") as f:
        f.write(f"Error: {str(e)}")
    print(f"Error: {e}")
