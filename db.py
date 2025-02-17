import sqlite3

def get_item(item_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM item WHERE id = ?', (item_id,))
    results = cursor.fetchone()
    conn.close()

    return results


def get_name(item_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM item WHERE id = ?', (item_id,))
    results = cursor.fetchone()
    conn.close()

    return results[0]

