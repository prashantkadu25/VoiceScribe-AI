import sqlite3
from database.db import get_connection
from datetime import datetime


def save_transcript(transcript_text, language="en"):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO transcripts (transcript_text, language) VALUES (?, ?)",
        (transcript_text, language)
    )
    conn.commit()
    last_id = c.lastrowid
    conn.close()
    return last_id


def get_total_transcripts():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM transcripts")
    count = c.fetchone()[0]
    conn.close()
    return count


def get_todays_transcripts():
    conn = get_connection()
    c = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute(
        "SELECT COUNT(*) FROM transcripts WHERE DATE(created_at) = ?",
        (today,)
    )
    count = c.fetchone()[0]
    conn.close()
    return count


def get_all_transcripts(limit=100):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT id, transcript_text, language, created_at FROM transcripts ORDER BY created_at DESC LIMIT ?",
        (limit,)
    )
    rows = c.fetchall()
    conn.close()
    
    transcripts = []
    for row in rows:
        transcripts.append({
            "id": row[0],
            "text": row[1],
            "language": row[2],
            "created_at": row[3]
        })
    return transcripts


def get_transcript_by_id(transcript_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT id, transcript_text, language, created_at FROM transcripts WHERE id = ?",
        (transcript_id,)
    )
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            "id": row[0],
            "text": row[1],
            "language": row[2],
            "created_at": row[3]
        }
    return None


def update_transcript(transcript_id, new_text):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "UPDATE transcripts SET transcript_text = ? WHERE id = ?",
        (new_text, transcript_id)
    )
    conn.commit()
    updated = c.rowcount
    conn.close()
    return updated > 0


def delete_transcript(transcript_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM transcripts WHERE id = ?", (transcript_id,))
    conn.commit()
    deleted = c.rowcount
    conn.close()
    return deleted > 0


def search_transcripts(keyword):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT id, transcript_text, language, created_at FROM transcripts WHERE transcript_text LIKE ? ORDER BY created_at DESC",
        (f"%{keyword}%",)
    )
    rows = c.fetchall()
    conn.close()
    
    transcripts = []
    for row in rows:
        transcripts.append({
            "id": row[0],
            "text": row[1],
            "language": row[2],
            "created_at": row[3]
        })
    return transcripts

from datetime import date

def get_today_records():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM transcripts
        WHERE DATE(created_at)=DATE('now','localtime')
    """)

    total = cursor.fetchone()[0]

    conn.close()
    return total


def get_total_words():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT transcript_text
        FROM transcripts
        """)

    rows = cursor.fetchall()

    words = sum(len(row[0].split()) for row in rows)

    conn.close()

    return words


def get_total_characters():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT transcript_text
        FROM transcripts
        """)

    rows = cursor.fetchall()

    chars = sum(len(row[0]) for row in rows)

    conn.close()

    return chars