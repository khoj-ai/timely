import datasets as ds
import csv

#open gradients_test.csv file
gradient_file = open("csv/gradients_test.csv", "r")
#read the file
gradient_reader = csv.reader(gradient_file, delimiter="|")
#count the number of 1s in 3rd column
count_zero = 0
count_one = 0
count_other = 0
for row in gradient_reader:
    if row[2] == "0":
        count_zero += 1
    elif row[2] == "1":
        count_one += 1
    else:
        count_other += 1
print("Number of 0s: ", count_zero)
print("Number of 1s: ", count_one)
print("Number of other values: ", count_other)