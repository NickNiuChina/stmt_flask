import pymysql
import pymysql.cursors

conn = pymysql.connect(
            host='127.0.0.1',
            user='stmtflask',
            password='stmtflask',
            database='stmtflask',
            cursorclass=pymysql.cursors.DictCursor
        )

cursor = conn.cursor()
cursor.execute("SELECT * from tb_user")
users = cursor.fetchall()
print(users)
print("---------------------------------------------------------------")
cursor.execute("SELECT * FROM tb_user WHERE username = %s", ('sdfds',))
users = cursor.fetchall()
print(users)