# ----------------------------------------------------------------------------------------------------------------
# Time Machine to Postgres
# Specify a Table in Time Machine and copy that contents to a pre-built table in Postgres on PA.
#
# PARAMETERS:
# 1 - SQL file to call
# 2 - PA Postgres Username
# 3 - PA Postgres Table (Schemaname.Tablename)
# ----------------------------------------------------------------------------------------------------------------

import codecs
import csv as CSV
import os
import pymssql
import psycopg2
import sys
import StringIO
from time import gmtime, strftime

def get_data(host,user,password,database,script,sdir,tdir):
  # Set working directory and alias
  dir = tdir
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
  file = open(sdir + '/' + s)
  sql = file.read()
  file.close()
  cur.execute(sql)

  # Write results to file
  encoding = 'ascii'
  csv = tdir + '/' +  alias + '.out'
  out = codecs.open(csv,'w',encoding)
  writer = CSV.writer(out, delimiter='~')
  # writer = csv.writer(out, delimiter=',', quoting=csv.QUOTE_ALL)

  # Header
  line = [col.encode(encoding,'ignore').replace(',','').strip() if type(col) is unicode else str(col[0]).replace(',','').strip() for col in cur.description]
  writer.writerow(line)

  # Records
  row = cur.fetchone()

  while row:
    line = [col.encode(encoding,'ignore') if type(col) is unicode else str(col) for col in row]

    writer.writerow(line)
    row = cur.fetchone()

  out.close()
  conn.close()

def main():
  # Set connection parameters
  # h = r'172.24.16.100\TIMEMACHINE' 
  h = r'172.24.16.100:49207'
  u = 'sa'
  p = 'us$eu$as$2'
  d = 'ReportingDB'
  sdir = sys.argv[1]
  tdir = sys.argv[2]
  s = sys.argv[3]

  pg_user = sys.argv[4]
  pg_schema_table = sys.argv[5]

  alias = s.split('/')[-1].split('.')[0]
  alias_file = tdir + '/' + alias + '.out'

  print "Landed file will be saved to: " + alias_file + "\n"

  print '\n' + strftime('%Y-%m-%d %H:%M:%S', gmtime()) + ' Starting script ...\n'

  # Ensure VPN connection
  os.system('sh $HOME/tools/autovpncscript.sh')  

  # --------------------------------------------
  # Run script
  # --------------------------------------------
  print '\nRunning SQL and generating output file ...\n'

  # Get the Data
  get_data(h,u,p,d,s,sdir,tdir)

  # Open the landed file
  f = open(alias_file, 'r')
  f.readline()

  # Open the Postgres connection
  conn = psycopg2.connect("dbname='dev' user='" + pg_user + "' host='10.223.176.60' port='5432'")

  # Copy from file to Postgres Table
  conn.cursor().copy_from(f,pg_schema_table,sep='~',null='None')
  conn.commit()

  # Close the landed file
  f.close()

  print '\n' + strftime('%Y-%m-%d %H:%M:%S', gmtime()) + ' Finished script ...\n'

if __name__ == '__main__':
  main()