with open("debug_status.txt", "w") as f:
    f.write("Starting imports\n")
    try:
        import sqlalchemy
        f.write("sqlalchemy ok\n")
        from app.core.config import settings
        f.write(f"settings ok: URI={settings.SQLALCHEMY_DATABASE_URI}\n")
        from app.db.session import SessionLocal
        f.write("SessionLocal ok\n")
        from app.initial_data import init_db
        f.write("initial_data ok\n")
    except Exception as e:
        f.write(f"Import Error: {e}\n")
