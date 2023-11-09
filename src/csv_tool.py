#!/usr/bin/env python3
import argparse, csv

# Purpose of program is to read a csv file
# with optional user defined dialect

def main():
    parser = argparse.ArgumentParser(description='Check for csv file format')
    parser.add_argument('file', help='input csv file to check')
    parser.add_argument('-d', '--delimiter', help='Delimiter to use')
    parser.add_argument('-q', '--quotechar', help='Quote character to use')
    parser.add_argument('-e', '--escapechar', help='Escape character to use')
    parser.add_argument('-c', '--doublequote', action='store_true', help='Should \
                        doublequoting be used')
    parser.add_argument('-s', '--skipinitialspace', action='store_true', help='Should \
                        spaces be skipped after delimiter')
    parser.add_argument('-b', '--quoting', help='Quoting convention to use')
    args = parser.parse_args()
    # default dialect
    dialect = csv.excel
    # set user defined dialect
    for arg in vars(args):
        if getattr(args, arg) and arg != 'file':
            setattr(dialect, arg, getattr(args, arg))
    csv_formatter(args.file, dialect)

def csv_formatter(filename, dialect):
    fp = None
    try:
        with open(filename, 'r+', newline='') as fp:
            reader = csv.reader(fp, dialect)
            # do stuff with file
            for row in reader:
                print(row)
    except FileNotFoundError as e:
        print("File {} not found: {}".format(filename, e))
    except IOError as e:
        print("Error handling file {}: {}".format(filename, e))
    finally:
        if fp: fp.close()

if __name__ == "__main__" : 
    main()