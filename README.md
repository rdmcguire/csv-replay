# EXMS CSV Data Replay Tool
This simple utility will replay saved CSV files by updating the start time and randomizing the duration for interest.
You must bring your own data (I don't want to sanitize customer data for the sake of hosting on git-hub)

## Configuration
I have provided column offsets for start/end ts for some basic feeds. Simply add a new tuple to the dict (x,y) where x = start ts column and y = end ts column).
```
types = dict()
types['COMMON']  = (2, 4)
types['MEDIA']   = (7, 9)
types['SIP']     = (2, 4)
types['SS7CALL'] = (2, 4)
```
*Default Values*
```
('-o', '--output-dir', help='Output location for data', default='./output')
('-i', '--input-dir', help='Input directory for data', default='./input')
('-p', '--pattern', help='Pattern to find input files', default='XMSCALL20*.csv')
('-r', '--replay-every', help='Interval at which to replay data', default=60, type=int)
('-s', '--skip-string', help='String in Col1 to skip if found (header)', default='db')
('--max-lines', help='Maximum lines to output per run', default=1000, type=int)
('--max-files', help='Maximum number of files in output directory', default=1000, type=int)
('--output-pattern', help='Pattern for output files, <TS> is timestamp', default='XMSCALL0_<TS>.csv')
```

## Command Synopsis
```
usage: csv_replay.py [-h] [-o OUTPUT_DIR] [-i INPUT_DIR] [-p PATTERN]
                     [-r REPLAY_EVERY] [-s SKIP_STRING]
                     [--max-lines MAX_LINES] [--max-files MAX_FILES]
                     [--output-pattern OUTPUT_PATTERN]

Replay XMS CSV Files

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output location for data
  -i INPUT_DIR, --input-dir INPUT_DIR
                        Input directory for data
  -p PATTERN, --pattern PATTERN
                        Pattern to find input files
  -r REPLAY_EVERY, --replay-every REPLAY_EVERY
                        Interval at which to replay data
  -s SKIP_STRING, --skip-string SKIP_STRING
                        String in Col1 to skip if found (header)
  --max-lines MAX_LINES
                        Maximum lines to output per run
  --max-files MAX_FILES
                        Maximum number of files in output directory
  --output-pattern OUTPUT_PATTERN
                        Pattern for output files, <TS> is timestamp
```

## Sample Usage
In the example below, the first 500 lines of each file provided will be replayed every 30 seonds until 100 files have accumulated.
```
$ mkdir input output
$ cp <some_file.csv> input/
$ nohup ./csv_replay.py -r 30 --max-files 100 --max-lines 500 -p '*.csv' &
```
