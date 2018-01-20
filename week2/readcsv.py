import csv

def main():
	with open('database01.csv') as csvfile:
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
		gpaCal(record)
		
def gpaCal(record):
	grade = {'A':4, 'B+':3.5, 'B':3, 'C+':2.5, 'C':2, 'D+':1.5, 'D':1, 'F':0}
	total_weight, total_point = 0, 0
	year_count, term_count = 1, 1
	for term in record:
		weight, point = 0, 0
		for subject in term:			# sum weight and point for each term
			weight += int(subject[1])
			point += int(subject[1])*grade[subject[3]]
		total_weight += weight
		total_point += point
		# display GPA
		print ("Year%d/%d GPA = %.2f GPAX = %.2f" 
			% (year_count, term_count, point/weight, total_point/total_weight))
		if term_count == 2 : year_count += 1
		term_count = 1 if term_count == 2 else term_count + 1 

main()