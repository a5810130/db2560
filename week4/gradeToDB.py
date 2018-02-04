#!/usr/bin/python
from __future__ import print_function
import mysql.connector as mariadb
from mysql.connector import errorcode
import tkFileDialog, csv, sys


def main():
	# mock
	#studentFName = 'Fname'
	#studentLName = 'Lname'
	#studentId = '6001011110001'
	#record = readCSV('database01.csv')
	
	# define DB detail
	dbName = "StudentRecords"
	tables = {}
	tables['Students'] = (
    "CREATE TABLE `Students` ("
    "	`Student_id` varchar(13) NOT NULL,	"
    "	`First_name` varchar(100) NOT NULL,"
    " 	`Last_name` varchar(100) NOT NULL,"
    " 	PRIMARY KEY (`Student_id`))")
	#"	UNIQUE (Student_id))")
	tables['Student_Records'] = (
    "CREATE TABLE `Student_Records` ("
    "  	`PK` int(11) NOT NULL AUTO_INCREMENT,"
	"	`SubjectID` varchar(10) NOT NULL,"
    "  	`SubjectName` varchar(100),"
    "  	`Weight` int(1) NOT NULL,"
    "  	`Section` int(3) NOT NULL,"
	"  	`Grade` varchar(2) NOT NULL,"
	"	`Term`	int(2)	NOT NULL,"
	"	`Student_id` varchar(13) NOT NULL,"
	"  	PRIMARY KEY (`pk`),"
	"	FOREIGN KEY (Student_id) REFERENCES Students(Student_id))")
	
	# get student detail
	studentFName = raw_input("First Name: ")
	studentLName = raw_input("Last Name: ")
	studentId = raw_input("Student ID: ")
	
	# get CSV file
	askopenfile = {
		'title':"Select CSV file",
		'filetypes':(("CSV files","*.csv"),("all files","*.*")),
	} 
	csvPath = tkFileDialog.askopenfilename(**askopenfile)
	if not (csvPath.endswith('.csv')): sys.exit("Error: Can't read file")
	

	# connect to DB
	mariadb_connection = mariadb.connect(user='mariadbUser')
	cursor = mariadb_connection.cursor()
	
	# try to use or create DATABASE
	try:
		cursor.execute("USE {}".format(dbName))
	except:
		cursor.execute("CREATE DATABASE {}".format(dbName))
		cursor.execute("USE {}".format(dbName))
	
	# try to create tables
	for name, ddl in tables.iteritems():
		try:
			print ("Creating table {}: ".format(name), end='')
			cursor.execute(ddl)
		except mariadb.Error as err:
			if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
				print ("already exists.")
			else:
				print (err.msg)
		else:
			print ("OK")
	
	# try to insert student data
	try:
		cursor.execute(
			"INSERT INTO Students (Student_id,First_name,Last_name)"
			"VALUES (%s,%s,%s);", (studentId,studentFName,studentLName))
	except mariadb.Error as error:
		print("Error: {}".format(error))
	
	# try to insert transcript
	with open(csvPath) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			try:
				cursor.execute(
					"INSERT INTO Student_Records "
					"(SubjectID,SubjectName,Weight,Section,Grade,Term,Student_id)"
					"VALUES (%s,%s,%s,%s,%s,%s,%s);", 
					(row['SubjectID'], row['SubjectName'], row['Weight'], 
					row['Section'], row['Grade'], row['Term'], studentId))
			except mariadb.Error as error:
				print("Error: {}".format(error))

	mariadb_connection.commit()

	mariadb_connection.close()
		
main()