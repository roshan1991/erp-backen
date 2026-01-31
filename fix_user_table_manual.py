import pymysql

try:
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='SysAdmin@123',
        database='erp_db'
    )
    cursor = conn.cursor()
    
    # Check if 'users' exists
    cursor.execute("SHOW TABLES LIKE 'users'")
    if cursor.fetchone():
        print("Table 'users' already exists.")
    else:
        # Check if 'user' exists
        cursor.execute("SHOW TABLES LIKE 'user'")
        if cursor.fetchone():
            print("Table 'user' found. Renaming to 'users'...")
            try:
                cursor.execute("RENAME TABLE user TO users")
                print("Successfully renamed 'user' to 'users'.")
            except Exception as e:
                print(f"Failed to rename table: {e}")
        else:
            print("Table 'user' NOT found. Cannot rename.")

    conn.commit()
    conn.close()

except Exception as e:
    print(f"Connection failed: {e}")
