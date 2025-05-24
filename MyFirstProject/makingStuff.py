import sqlite3

cnt=sqlite3.connect('samanehShop.db')

#-------------create users table----------
# sqlUsers='''
#             CREATE TABLE users(
#                 id INTEGER PRIMARY KEY,
#                 username VARCHAR(30) NOT NULL,
#                 password VARCHAR(30) NOT NULL,
#                 address TEXT,
#                 grade REAL
#             )

# '''

# cnt.execute(sqlUsers)

#-------------------filling users table--------------
# userIn=input('enter your username: ')
# pasIn=input('enter your password: ')
# addrIn=input('enter your address: ')

# sqlFil=f''' INSERT INTO users (username,password,address,grade)
#            VALUES ("{userIn}","{pasIn}","{addrIn}",0)           
# '''

# cnt.execute(sqlFil)
# cnt.commit()

#---------------deleting if needed-------------
# user=input('enter a username: ')
# sqlDel=f'''
#             DELETE FROM users WHERE username="{user}"
# '''
# cnt.execute(sqlDel)
# cnt.commit()

#--------------create products table-------------

# sqlProduct='''
#             CREATE TABLE products(
#             id INTEGER PRIMARY KEY,
#             productname VARCHAR(30) NOT NULL,
#             numbers INTEGER NOT NULL,
#             price INTEGER NOT NULL,
#             edate VARCHAR(30)
#             )
# '''

# cnt.execute(sqlProduct)

#---------------filling products table-------------

# sqlFil=''' 
#         INSERT INTO products(productname,numbers,price)
#         VALUES("speaker",79,899)
# '''
# cnt.execute(sqlFil)
# cnt.commit()

#--------------create cart table------------

# sql='''
#         CREATE TABLE cart(
#             id INTEGER PRIMARY KEY,
#             Userid INTEGER NOT NULL,
#             Productid INTEGER NOT NULL,
#             purchaseNum INTEGER NOT NULL,
#             date VARCHAR(30)
#         )
# '''

# cnt.execute(sql)

#--------------edditing my table if needed-----------

# sqlE='''
#         UPDATE products
#         SET numbers=29
#         WHERE productname="samsung led"
# '''

# cnt.execute(sqlE)
# cnt.commit()
