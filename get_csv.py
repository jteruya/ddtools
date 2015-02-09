import codecs
import csv as CSV
import os
import pymssql
import sys
from time import gmtime, strftime

def run_sql(host,user,password,database,script):
  # Set working direcotry and alias
  dir = os.getcwd() + '/' if len(sys.argv[1].split('/')) == 1 else '/'.join(sys.argv[1].split('/')[:-1]) + '/'
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
  dir = os.getcwd() + '/' if len(sys.argv[1].split('/')) == 1 else '/'.join(sys.argv[1].split('/')[:-1]) + '/'
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
  csv = dir + alias + '.csv'
  out = codecs.open(csv,'w',encoding)
  writer = CSV.writer(out, delimiter=',')
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

  # Write some of the results to console
  os.system('dos2unix ' + csv)
  print '\n'
  os.system('column -s, -t <  ' + csv + ' | head -n 1000')
  os.system('echo \'(First 1000 lines or less only)\'')

def main():
  # Set connection parameters
  # h = r'172.24.16.100\TIMEMACHINE' 
  h = r'172.24.16.100:49207'
  u = 'sa'
  p = 'us$eu$as$2'
  d = 'ReportingDB'
  s = sys.argv[1]

  print '\n' + strftime('%Y-%m-%d %H:%M:%S', gmtime()) + ' Starting script ...\n'

  # Ensure VPN connection
  os.system('sh $HOME/tools/autovpncscript.sh')  

  # Run script
  if len(sys.argv) == 3:
    print '\nRunning SQL without generating output file ...\n'
    run_sql(h,u,p,d,s)
  else:
    print '\nRunning SQL and generating output file ...\n'
    get_csv(h,u,p,d,s)

  print '\n' + strftime('%Y-%m-%d %H:%M:%S', gmtime()) + ' Finished script ...\n'

if __name__ == '__main__':
  main()
