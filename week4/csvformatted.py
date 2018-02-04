import csv

def main():
	with open('database01.csv') as csvfile:
		next(csvfile)
		reader = csv.reader(csvfile)
		record, term = [], []
		for row in reader:
			if (row[0]):			# add Subject to term
				subject = row[0].split(' ',1)
				term.append([subject[0],subject[1],row[1],row[2],row[3]])
			else :						# start next term if empty row
				if term == [] : break	# end adding when see two empty row
				record.append(term)
				term = []
	with open('database01formatted.csv', 'wb') as csvfile:
		fieldnames = [
		'SubjectID','SubjectName','Weight','Section','Grade','Term']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		term_count = 1
		for term in record:
			for subject in term:
				writer.writerow({
					'SubjectID': subject[0], 
					'SubjectName': subject[1],
					'Weight': subject[2],
					'Section': subject[3],
					'Grade':  subject[4],
					'Term': term_count})
			term_count += 1
main()				