import sqlite3

def get_item(item_id):
    """
    :param item_id: ID товара
    :return: все данные о товаре
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM item WHERE id = ?', (item_id,))
    results = cursor.fetchone()
    conn.close()

    return results


def get_name(item_id):
    """
    :param item_id: ID товара
    :return: название товара
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM item WHERE id = ?', (item_id,))
    results = cursor.fetchone()
    conn.close()

    return results[0]

