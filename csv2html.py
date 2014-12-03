#!/usr/bin/python

import sys
import os
import csv
import string

def is_float(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def is_int(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

if len(sys.argv) < 3:
  sys.stderr.write(sys.argv[0] + ': usage - ' + sys.argv[0] + ' [.csv file name] [.html file name]\n')
  sys.exit()

if not os.path.exists(sys.argv[1]):
  sys.stderr.write(sys.argv[1] + ' not found \n')
  sys.exit()

with open(sys.argv[2], 'w') as htmlfile:
  with open(sys.argv[1], 'r') as csvfile:
    table_string = ''
    reader = csv.reader(csvfile)
    htmlfile.write('<table border="1" cellpadding="0" cellspacing="0">')
    headers = [header.strip() for header in csvfile.readline().split(',')]
    line = []
    for header in headers:
      line.append('<th align="center">' + header + '</th>')
    htmlfile.write('<tr>' + ''.join(line) + '</tr>')
    for row in reader:
      line = []
      for col in row:
        if is_float(col):
            if is_int(col):
              line.append('<td align="right">' + '{:,.0f}'.format(float(col)) + '</td>')
            else:
              line.append('<td align="right">' + '{:,.2f}'.format(float(col)) + '</td>')
        else:
          line.append('<td align="left">' + col + '</td>\n')
      htmlfile.write('<tr>' + ''.join(line) + '</tr>')
    htmlfile.write('</table>\n')
