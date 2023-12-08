import sqlite3

con = sqlite3.connect('TEST.db')
cur = con.cursor()

dictionary = {'item_3': 3, 'item_2': 2, 'item_1': 1}

query = """CREATE TABLE IF NOT EXISTS test(item_1, item_2, item_3)"""

cur.execute(query)
con.commit()

q = """INSERT INTO test(item_3, item_1, item_2) VALUES (:item_3, :item_1, :item_2)"""
cur.execute(q, dictionary)
con.commit()


# item_1	item_2	item_3
# 3	        1	    2