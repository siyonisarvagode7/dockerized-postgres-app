import time
import os
import psycopg2

DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = int(os.getenv("POSTGRES_PORT", 5432))
DB_NAME = os.getenv("POSTGRES_DB", "mydb")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "pass")

def wait_for_db():
    for i in range(10):
        try:
            conn = psycopg2.connect(
                host=DB_HOST, port=DB_PORT,
                dbname=DB_NAME, user=DB_USER, password=DB_PASS
            )
            conn.close()
            print("Postgres is ready!")
            return
        except Exception as e:
            print(f"Postgres not ready yet ({e})... retrying...")
            time.sleep(2)

def main():
    wait_for_db()
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT,
        dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )
    conn.autocommit = True

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id SERIAL PRIMARY KEY,
            name TEXT
        );
    """)

    cur.execute("INSERT INTO people (name) VALUES ('Docker User') RETURNING id;")
    inserted_id = cur.fetchone()[0]
    print("Inserted ID:", inserted_id)

    cur.execute("SELECT * FROM people WHERE id = %s;", (inserted_id,))
    print("Row:", cur.fetchone())

    conn.close()

if __name__ == "__main__":
    main()
