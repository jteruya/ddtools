import csv
import sys

def csv_to_list(file_name):
# Reads the contents of a CSV into a a list whose elements are lists, mimicking the structure of the CSV contents.
  file = open(file_name)
  list = [[item.strip() for item in line.split(',')] for line in file.readlines()]
  file.close()
  return list

def transpose_list(original_list):
# Transposes a given list object and returns a transposed version of that list.
  return map(list,zip(*original_list))

def main():

  i = sys.argv[1]
  d = transpose_list(csv_to_list(i))
  o = open(i.split('.')[0]+'_transposed.csv','w')
  w = csv.writer(o)
  w.writerows(d)

if __name__ == '__main__':
  main()
