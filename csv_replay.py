#!/usr/bin/python
import argparse
import csv
import sys
import random
from glob import glob
from time import time, sleep
from datetime import datetime

random.seed()
types = dict()
types['COMMON']  = (2, 4)
types['MEDIA']   = (7, 9)
types['SIP']     = (2, 4)
types['SS7CALL'] = (2, 4)

parser = argparse.ArgumentParser(description='Replay XMS CSV Files')
parser.add_argument('-o', '--output-dir', help='Output location for data', default='./output')
parser.add_argument('-i', '--input-dir', help='Input directory for data', default='./input')
parser.add_argument('-p', '--pattern', help='Pattern to find input files', default='XMSCALL20*.csv')
parser.add_argument('-r', '--replay-every', help='Interval at which to replay data', default=60, type=int)
parser.add_argument('-s', '--skip-string', help='String in Col1 to skip if found (header)', default='db')
parser.add_argument('--max-lines', help='Maximum lines to output per run', default=1000, type=int)
parser.add_argument('--max-files', help='Maximum number of files in output directory', default=1000, type=int)
parser.add_argument('--output-pattern', help='Pattern for output files, <TS> is timestamp', default='XMSCALL0_<TS>.csv')

args = parser.parse_args()

def print_log(msg):
  dt = datetime.now()
  print('{} - {}'.format(dt, msg))

while True:
  in_files = glob(args.input_dir.rstrip('/')+'/'+args.pattern)
  out_files = glob(args.output_dir.rstrip('/')+'/'+args.output_pattern.replace('<TS>','*'))
  if len(out_files) >= args.max_files:
    print_log('Too many files in output ({}), sleeping'.format(len(out_files)))
    sleep(args.replay_every)
  print_log('Found {} files to replay'.format(len(in_files)))
  if len(in_files) < 1:
    print_log('Nothing to do, sleeping')
  else:
    for f in in_files:
      start_time = time()
      headers = list()
      data = list()
      file_ts = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'_'+str(time()).replace('.','')[-3:]
      file_name = '{}/{}'.format(args.output_dir.rstrip('/'),args.output_pattern).replace('<TS>',file_ts)
    # Read Data
      with open(f, 'rb') as csvfile:
	csvdata = csv.reader(csvfile)
	for row in csvdata:
	  if args.skip_string in row[1]:
	    headers.append(row)
	    continue
	  if types.get(row[0]) is None:
	    #print('Unknown Type {}'.format(row[0]))
	    continue
	  start, end = types.get(row[0])
	  # Replace start and end time
	  row[start] = int(time())
	  row[end] = row[start] + random.randint(12,300)
	  data.append(row)
	  if len(data) == args.max_lines:
	    break
    # Write data
      with open(file_name, 'wb') as csvout:
	writer = csv.writer(csvout,lineterminator='\n')
	writer.writerows(headers)
	writer.writerows(data)
      print_log('Wrote {} rows from {} to {} in {} seconds'.format(len(data),f,file_name,format(time()-start_time,'.4f')))
      sys.stdout.flush()
      sleep(.1)
  sleep(args.replay_every)
