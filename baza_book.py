import sqlite3 

class Database():
	def __init__(self):
		self.conn = sqlite3.connect("books.db")
		self.cur = self.conn.cursor()

	def create_db(self):
		self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
			tel_id varchar(30),
			name varchar(50)
			)""")
	
	def select_users(self,id):
		self.cur.execute(f"SELECT * FROM users WHERE tel_id='{id}' ")
		self.cur.fetchone()
		if data is None:
			return False
		else:
			return True


	def insert_users(self,tel_id,name):
		self.cur.execute(f"INSERT into users values ('{tel_id}','{name}')")	
		return self.cur.commit()
	

    # books category
	def create_category(self):
		self.cur.execute("""CREATE TABLE IF NOT EXISTS category(
    		id integer PRIMARY KEY AUTOINCREMENT,
    		name varchar(20)
    		)""")

	def insert_category(self,name):
		self.cur.execute(f"INSERT into category(name) values('{name}')")
		return self.conn.commit()


	def select_category_id(self,id):
		self.cur.execute(f"SELECT * FROM category WHERE id = '{id}' ")
		data = self.cur.fetchone()
		return data

	def select_category_all(self):
		self.cur.execute("SELECT * FROM category")
		return self.cur.fetchall() 


	# Books Products
	def create_table_products(self):
		self.cur.execute("""CREATE TABLE IF NOT EXISTS products(
			id integer PRIMARY KEY AUTOINCREMENT,
			category_id integer,
			file_name varchar(250),
			file_des text NULL,
			file_muallif text NULL,
			file_yili text NULL,
			file_id text NULL,
			file_photo text NULL,
			FOREIGN KEY(category_id) references category(id)
			)""")



	def select_products_for_category_id(self,id):
		self.cur.execute(f"SELECT * FROM products WHERE category_id = '{id}' ")
		return self.cur.fetchall()

	

	def select_product_all(self):
		self.cur.execute("SELECT * FROM products")
		data = self.cur.fetchall()
		return data


	def select_product_id(self,id):
		self.cur.execute(f"SELECT * FROM products WHERE id = '{id}' ")
		return self.cur.fetchone()

	def insert_products(self,file_name,category_id,file_des,file_muallif,file_yili,file_id,file_photo):
		self.cur.execute(f"""INSERT INTO products(file_name,category_id,file_des,file_muallif,file_yili,file_id,file_photo) values("{file_name}",{category_id},"{file_des}","{file_muallif}","{file_yili}","{file_id}","{file_photo}")""")
		return self.conn.commit()

	def search_product(self,suz):
		self.cur.execute(f"""SELECT * FROM products WHERE file_name like "%{suz}%" """)
		data = self.cur.fetchall()
		return data








