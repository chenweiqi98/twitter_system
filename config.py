from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Myran199927!'
app.config['MYSQL_DATABASE_DB'] = 'mysql'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# cur = mysql.connector

# query = ("SELECT * FROM emp")

# cur.execute(query)