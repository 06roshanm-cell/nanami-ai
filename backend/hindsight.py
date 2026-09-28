import sqlite3

def create_memory():

    conn = sqlite3.connect("feedback.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS hindsight(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue TEXT,
        solution TEXT,
        product TEXT,
        success_rate INTEGER
    )
    """)

    data = [
        ("Battery drains quickly",
         "Update to version 1.2 and recalibrate battery",
         "Galaxy S25",95),

        ("Camera blurry after update",
         "Clear camera cache and install latest patch",
         "Galaxy S25",91),

        ("WiFi disconnects",
         "Reset network settings and restart device",
         "Galaxy S25",89)
    ]

    cur.executemany(
        "INSERT INTO hindsight(issue,solution,product,success_rate) VALUES(?,?,?,?)",
        data
    )

    conn.commit()
    conn.close()

def search_solution(issue):

    conn = sqlite3.connect("feedback.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT solution,success_rate FROM hindsight WHERE issue LIKE ? LIMIT 1",
        ('%'+issue+'%',)
    )

    row = cur.fetchone()

    conn.close()

    if row:
        return {
            "solution":row[0],
            "success":row[1]
        }

    return None
def get_all_memory():

    conn = sqlite3.connect("feedback.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT issue, solution, success_rate
        FROM hindsight
        ORDER BY id DESC
    """)

    rows = cur.fetchall()
    conn.close()

    result = []

    for row in rows:
        result.append({
            "issue": row[0],
            "solution": row[1],
            "success": row[2]
        })

    return result