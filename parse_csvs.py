import MySQLdb as mdb
import glob
import os

MYSQL_HOST = 'localhost'
MYSQL_USER = 'particle'
MYSQL_PASSWORD = 'particle'
MYSQL_DATABASE = 'particle'

try:
	con = mdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)
	cur = con.cursor()

	for filename in glob.glob("*.csv"):
		try:
			roomname = filename.split("calculated_activity_")[1].split(".csv")[0]
		except:
			roomname = filename.split("data_thresholded_")[1].split(".csv")[0]
		with open(filename, 'r') as file:
			header = file.readline().rstrip('\n')
			headers = header.split(",")
			for line in file:
				line = line.rstrip('\n')
				elems = line.split(',')
				timestamp = elems[headers.index('Timestamp')].split("+")[0]
				elems.pop(headers.index('Timestamp'))

				for idx, val in enumerate(elems):
					name = headers[idx + 1]
					if (val != "nan"):
						query = "INSERT INTO analyses (timestamp, room, name, value) VALUES ('" + timestamp + "', '" + roomname + "', '" + name + "', '" + val + "')"
						cur.execute(query)
						con.commit()
		os.remove(filename)
	

except mdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])

finally:
	if con:
		con.close()
