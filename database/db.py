import sqlite3

from werkzeug.security import generate_password_hash

DATABASE = "expense_tracker.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT NOT NULL UNIQUE,
            email         TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            title      TEXT    NOT NULL,
            amount     REAL    NOT NULL,
            category   TEXT    NOT NULL,
            date       DATE    NOT NULL,
            notes      TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    conn.execute(
        "INSERT OR IGNORE INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        ("alice", "alice@example.com", generate_password_hash("password123")),
    )
    conn.execute(
        "INSERT OR IGNORE INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        ("bob", "bob@example.com", generate_password_hash("password123")),
    )
    if not conn.execute("SELECT 1 FROM expenses LIMIT 1").fetchone():
        conn.executemany(
            "INSERT INTO expenses (user_id, title, amount, category, date, notes) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (1, "Groceries",       52.30, "Food",          "2025-05-01", "Weekly shop"),
                (1, "Bus pass",        30.00, "Transport",     "2025-05-03", "Monthly top-up"),
                (2, "Electric bill",  110.50, "Utilities",     "2025-05-05", "May invoice"),
                (2, "Cinema tickets",  24.00, "Entertainment", "2025-05-10", "Weekend outing"),
            ],
        )
    conn.commit()
    conn.close()
