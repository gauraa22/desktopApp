import sqlite3

conn = sqlite3.connect('arrayTest.db')  # you can create a new database by changing the name within the quotations (the database will be saved in the location where your 'py' file is saved)

c = conn.cursor()


# Create table - CLIENTS
c.execute("""CREATE TABLE arrays(name text PRIMARY KEY,mgmt text,spa text,spb text)
""")

conn.close()