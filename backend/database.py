import mysql.connector

mydb = mysql.connector.connect(host="192.168.1.109", user="ias")

print(mydb)