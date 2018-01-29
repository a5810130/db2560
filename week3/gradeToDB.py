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
    "  	`Subject` varchar(100) NOT NULL,"
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
	
	# get record from CSV file
	record = readCSV(csvPath)
	

	# connect to DB
	mariadb_connection = mariadb.connect(user='root', password='')
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
	term_count = 1
	for term in record:
		for subject in term:
			try:
				cursor.execute(
					"INSERT INTO Student_Records "
					"(Subject,Weight,Section,Grade,Term,Student_id) "
					"VALUES (%s,%s,%s,%s,%s,%s);", 
					(subject[0], subject[1], subject[2], subject[3], 
					term_count, studentId))
			except mariadb.Error as error:
				print("Error: {}".format(error))
		term_count += 1

	mariadb_connection.commit()

	mariadb_connection.close()

def readCSV(csvfile):
	with open(csvfile) as csvfile:
		next(csvfile)
		reader = csv.reader(csvfile)
		record, term = [], []
		for row in reader:
			if (row[0]): 				# add Subject to term
				term.append([row[0],row[1],row[2],row[3]])
			else :						# start next term if empty row
				if term == [] : break	# end adding when see two empty row
				record.append(term)
				term = []
	return record
		
main()