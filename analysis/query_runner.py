from .db_config import get_connection


def run_query(sql, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params or [])
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        return columns, results
    except Exception as e:
        return ["Error"], [[str(e)]]
    finally:
        conn.close()
