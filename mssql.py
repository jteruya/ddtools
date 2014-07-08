import codecs
import csv
import os
import pymssql

def run_sql(host,user,password,database,script):
  # Set working direcotry and alias
  dir = '/'.join(script.split('/')[:-1]) + '/'
  alias = script.split('/')[-1].split('.')[0]

  # Set connection parameters
  h = host
  u = user
  p = password
  d = database
  s = script

  # Connect to database
  conn = pymssql.connect(host=h,user=u,password=p,database=d)
  cur = conn.cursor()

  # Get script, run it
  file = open(s)
  sql = file.read()
  file.close()
  cur.execute(sql)

  conn.commit()
  conn.close()

def get_csv(host,user,password,database,script):
  # Set working directory and alias
  dir = '/'.join(script.split('/')[:-1]) + '/'
  alias = script.split('/')[-1].split('.')[0]

  # Set connection parameters
  h = host
  u = user
  p = password
  d = database
  s = script

  # Connect to database
  conn = pymssql.connect(host=h,user=u,password=p,database=d)
  cur = conn.cursor()

  # Get script, run it
  file = open(s)
  sql = file.read()
  file.close()
  cur.execute(sql)

  # Write results to file
  encoding = 'ascii'
  out = codecs.open(dir + alias + '.csv','w',encoding)
  writer = csv.writer(out, delimiter=',')
  # writer = csv.writer(out, delimiter=',', quoting=csv.QUOTE_ALL)

  line = [col.encode(encoding,'ignore').replace(',','').strip() if type(col) is unicode else str(col[0]).replace(',','').strip() for col in cur.description]
  writer.writerow(line)
  row = cur.fetchone()

  while row:
    line = [col.encode(encoding,'ignore') if type(col) is unicode else str(col) for col in row]
    writer.writerow(line)
    row = cur.fetchone()

  out.close()
  conn.close()
