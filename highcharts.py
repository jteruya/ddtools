import re
import os

def create_alias(string):
# Removes special characters and spaces from a string for a name alias, i.e. for directory names.q
  return re.sub('[^A-Za-z0-9 ]','',string).replace(' ','_').lower()

def csv_to_list(file_name):
# Reads the contents of a CSV into a a list whose elements are lists, mimicking the structure of the CSV contents.
  file = open(file_name)
  list = [[item.strip() for item in line.split(',')] for line in file.readlines()]
  file.close()
  return list

def pivot_csv(file_name):
# Pivots a CSV from this format...
# series_name,category_name,value

# ...into this format...
# series_name,category_1,category_2,...

# ...with correspoinding values at series_name/category_[x] intersections.
  
  csv = file_name

  columns = open(csv).readlines()[0].strip().split(',')

  data = [line.strip().split(',') for line in open(csv).readlines()[1:]]

  # for i in range(len(data)):
  #   for j in range(len(data[i])):
  #     if j == 1: 
  #       data[i][j] = int(data[i][j])
  #     if j == 2:
  #       data[i][j] = data[i][j].strip()

  series = []
  for d in data:
    if d[0] not in series:
      series.append(d[0])

  categories = []
  for d in data:
    if d[1] not in categories:
      categories.append(d[1])

  table = [['' for c in range(len(categories))] for s in range(len(series))]

  for s in series:
    for c in categories:
      for d in data:
        table[series.index(d[0])][categories.index(d[1])] = d[2]

  file = open(csv,'w')

  file.write(columns[1] + ',' + ','.join([str(c) for c in categories]) + '\n')
  for t in range(len(table)):
    file.write(series[t] + ',' + ','.join([str(t) for t in table[t]]) + '\n')

  file.close()

def proper_case_csv_header(file_name):
  column_headers = csv_to_list(file_name)[0]
  column_headers_proper = ','.join([column.replace('_',' ').title() for column in column_headers])
  file_name_old = file_name + '~'
  os.rename(file_name,file_name_old)
  old_csv = open(file_name_old)
  new_csv = open(file_name,'w')

  first_line = True
  for line in old_csv:
    if first_line:
      line = column_headers_proper + '\n'
      first_line = False
    new_csv.write(line)

  old_csv.close()
  new_csv.close()
  os.remove(file_name_old)

def remove_eof(file_name):
# Removes EOF of given file. Highcharts charts break when reading files that contain EOF.
  os.system("perl -i -pe 'chomp if eof' " + file_name)

def remove_trailing_char(file_name,char):
  file_name_old = file_name + '~'
  os.rename(file_name,file_name_old)

  file_old = open(file_name_old)
  line_old = file_old.readlines()
  file_old.close()

  line_new = [line.strip().rstrip(char) for line in line_old]

  file_new = open(file_name,'w')
  for line in line_new:
    file_new.write(line + '\n')

  file_old.close()
  file_new.close()
  os.remove(file_name_old)

def run_sql(file_name,conn_name):
# Executes a SQL script through the given connection.
  cmd = 'cat ' + file_name + ' | ' + conn_name
  os.system(cmd)

def string_replace(parameter_list,argument_list,template_name,instance_name):
# Replaces a list of parameters with a list of arguments with corresponding indices.
# Parameters in a template file are replaced with arguments and the results are written to an instance file.
  replace = []

  for i in range(len(parameter_list)):
    replace.append(".replace('" + str(parameter_list[i]) + "','" + str(argument_list[i]) + "')")

  template = open(template_name)
  instance = open(instance_name,'w')

  for line in template:
    cmd = 'instance.write(line' + ''.join(replace) + ')'
    exec cmd

  template.close()
  instance.close()

def transpose_list(original_list):
# Transposes a given list object and returns a transposed version of that list.
  return map(list,zip(*original_list))

def unique_list(list):
# Dedupes the elements of a list and returns a list of unique elements. The original ordering of the elements is retained.
  unique_list = []
  for item in list:
    if item not in unique_list:
      unique_list.append(item)
  return unique_list
