#!/usr/bin/env python3
import argparse, csv, sys

# Purpose of program is to read a csv file
# with optional user defined dialect

def main():
    (file, dialect) = parse_args(sys.argv[1:])
    csv_tool(file, dialect)

def parse_args(input_args):
    parser = argparse.ArgumentParser(description='Check for csv file format')
    parser.add_argument('file', help='input csv file to check')
    parser.add_argument('-d', '--delimiter', help='Delimiter to use')
    parser.add_argument('-q', '--quotechar', help='Quote character to use')
    parser.add_argument('-e', '--escapechar', help='Escape character to use')
    parser.add_argument('-c', '--doublequote', action='store_false', help='Should \
                        doublequoting be used')
    parser.add_argument('-s', '--skipinitialspace', action='store_true', help='Should \
                        spaces be skipped after delimiter')
    parser.add_argument('-b', '--quoting', help='Quoting convention to use')
    args = parser.parse_args(input_args)
    # default dialect
    dialect = csv.excel
    setattr(dialect, 'escapechar', None) # excel dialect does not specify escapechar
    # set user defined dialect
    for arg in vars(args):
        if (arg != 'file' and getattr(args, arg) != None):
            setattr(dialect, arg, getattr(args, arg))
    return (args.file, dialect)
    

def csv_tool(filename, dialect):
    fp = None
    cnt = -1
    try:
        with open(filename, 'r+', newline='') as fp:
            reader = csv.reader(fp, dialect)
            # do stuff with file
            cnt = 0
            for row in reader:
                print(row)
                cnt += 1
    except FileNotFoundError as e:
        print("File {} not found: {}".format(filename, e))
    except IOError as e:
        print("Error handling file {}: {}".format(filename, e))
    finally:
        if fp: fp.close()
    return cnt

if __name__ == "__main__" : 
    main()