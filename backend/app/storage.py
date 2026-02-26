"""Lightweight SQLite-backed persistence used by the API routers."""

import os
from pathlib import Path
import sqlite3
import threading
from typing import Any

# Allow overriding the DB location (useful for containers / volume mounts)
DB_PATH = Path(
    os.getenv("TUTOROPS_DB_PATH", Path(__file__).resolve().parent / "tutorops.db")
).resolve()
lock = threading.Lock()

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.row_factory = sqlite3.Row


def _init_db() -> None:
    """Create tables if they don't already exist."""
    with lock:
        conn.executescript(
            """
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                subject TEXT,
                hourly_rate REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                duration_hours REAL NOT NULL,
                topic TEXT,
                notes TEXT,
                FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
            );
            """
        )
        conn.commit()


def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {k: row[k] for k in row.keys()}


def create_client(data: dict[str, Any]) -> dict[str, Any]:
    with lock:
        cur = conn.execute(
            """
            INSERT INTO clients (first_name, last_name, email, phone, subject, hourly_rate)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data["first_name"],
                data["last_name"],
                data["email"],
                data.get("phone"),
                data.get("subject"),
                data["hourly_rate"],
            ),
        )
        conn.commit()
        client_id = cur.lastrowid
    return get_client_by_id(client_id)  # type: ignore[arg-type]


def list_clients() -> list[dict[str, Any]]:
    with lock:
        rows = conn.execute("SELECT * FROM clients ORDER BY id").fetchall()
    return [_row_to_dict(r) for r in rows if r is not None]  # type: ignore[list-item]


def get_client_by_id(client_id: int) -> dict[str, Any] | None:
    with lock:
        row = conn.execute(
            "SELECT * FROM clients WHERE id = ?", (client_id,)
        ).fetchone()
    return _row_to_dict(row)


def create_session(data: dict[str, Any]) -> dict[str, Any]:
    with lock:
        cur = conn.execute(
            """
            INSERT INTO sessions (client_id, date, duration_hours, topic, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                data["client_id"],
                data["date"],
                data["duration_hours"],
                data.get("topic"),
                data.get("notes"),
            ),
        )
        conn.commit()
        session_id = cur.lastrowid
    return get_session_by_id(session_id)  # type: ignore[arg-type]


def list_sessions() -> list[dict[str, Any]]:
    with lock:
        rows = conn.execute("SELECT * FROM sessions ORDER BY id").fetchall()
    return [_row_to_dict(r) for r in rows if r is not None]  # type: ignore[list-item]


def get_session_by_id(session_id: int) -> dict[str, Any] | None:
    with lock:
        row = conn.execute(
            "SELECT * FROM sessions WHERE id = ?", (session_id,)
        ).fetchone()
    return _row_to_dict(row)


def list_sessions_for_client(client_id: int) -> list[dict[str, Any]]:
    with lock:
        rows = conn.execute(
            "SELECT * FROM sessions WHERE client_id = ? ORDER BY id",
            (client_id,),
        ).fetchall()
    return [_row_to_dict(r) for r in rows if r is not None]  # type: ignore[list-item]


def get_client_summary(client_id: int) -> dict[str, Any] | None:
    client = get_client_by_id(client_id)
    if client is None:
        return None

    with lock:
        row = conn.execute(
            """
            SELECT COUNT(*) AS total_sessions,
                   COALESCE(SUM(duration_hours), 0.0) AS total_hours
            FROM sessions
            WHERE client_id = ?
            """,
            (client_id,),
        ).fetchone()

    total_sessions = row["total_sessions"] if row is not None else 0
    total_hours = row["total_hours"] if row is not None else 0.0
    total_earnings = float(total_hours) * float(client["hourly_rate"])

    return {
        "client_id": client_id,
        "total_sessions": total_sessions,
        "total_hours": total_hours,
        "total_earnings": total_earnings,
    }


def get_global_summary() -> dict[str, Any]:
    with lock:
        clients = conn.execute("SELECT COUNT(*) AS total FROM clients").fetchone()
        sessions_row = conn.execute(
            """
            SELECT COUNT(*) AS total_sessions,
                   COALESCE(SUM(s.duration_hours), 0.0) AS total_hours,
                   COALESCE(SUM(s.duration_hours * c.hourly_rate), 0.0) AS total_earnings
            FROM sessions s
            JOIN clients c ON c.id = s.client_id
            """
        ).fetchone()

    return {
        "total_clients": clients["total"] if clients else 0,
        "total_sessions": sessions_row["total_sessions"] if sessions_row else 0,
        "total_hours": sessions_row["total_hours"] if sessions_row else 0.0,
        "total_earnings": sessions_row["total_earnings"] if sessions_row else 0.0,
    }


def reset_db() -> None:
    """Clear all data (useful for tests) and reset autoincrement counters."""
    with lock:
        conn.execute("DELETE FROM sessions")
        conn.execute("DELETE FROM clients")
        try:
            conn.execute(
                "DELETE FROM sqlite_sequence WHERE name IN ('clients', 'sessions')"
            )
        except sqlite3.OperationalError:
            # sqlite_sequence may not exist yet (fresh database)
            pass
        conn.commit()


_init_db()
