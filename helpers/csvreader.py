import csv

global input
global nr

def read_csv(self, inputfilecsv):
    #Read the input test cases from input.csv file and append each row/testcase to dictionary '''
    with open(inputfilecsv) as f:
        reader = csv.DictReader(f,delimiter='|',quoting=csv.QUOTE_NONE)
        input = [r for r in reader]
        return input