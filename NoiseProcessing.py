# coding: utf-8
'''
I have no clue what this does. :-(
'''
import json
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()



# Create table if it doesnt exist
try: c.execute('''CREATE TABLE stocks
							(date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
c.execute("SELECT * FROM stocks")
print c.fetchone() 

for row in c.execute("SELECT * FROM stocks"):
	print row

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

c.execute("SELECT * FROM stocks")
print c.fetchone() 

for row in c.execute("SELECT * FROM stocks"):
	print row
fp = open('data.json')

o = json.load(fp)


for key in o.keys():
	print key, type(o[key])
#print o.values()
