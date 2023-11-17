#!/usr/bin/env python3
import argparse, csv, sys
import pandas as pd, numpy as np, matplotlib.pyplot as plt

# Purpose of program is to read a csv file and do stuff with it

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
    cnt = -1 # error flag
    try:
        with open(filename, 'r+', newline='') as fp:
            cnt = 0
            reader = csv.reader(fp, dialect)
            # do stuff with file
            for _ in reader:
                cnt += 1
            if cnt > 0: # if file is not empty
                stat_maker(filename)
    except FileNotFoundError as e:
        print("File {} not found: {}".format(filename, e))
    except IOError as e:
        print("Error handling file {}: {}".format(filename, e))
    finally:
        if fp: fp.close()
    return cnt

def stat_maker(filename):
    df = pd.read_csv(filename)
    # find numeric columns
    numeric_tracker=np.zeros((len(df.columns),), dtype=int)
    for i in range(len(df.columns)):
        if np.all([str(j).isnumeric() for j in df.iloc[:,i]]):
            numeric_tracker[i] = 1
    # plot numeric columns
    fig, axs = plt.subplots(np.sum(numeric_tracker), 1, figsize=(10, 10*np.sum(numeric_tracker)))
    fig.suptitle('Field Data for {}'.format(filename.split('/')[-1]))
    for i in range(len(df.columns)):
        if numeric_tracker[i]:
            mean = round(np.sum(df.iloc[1:,i].astype(float))/len(df.iloc[1:,i]), 3)
            median = np.median(df.iloc[1:,i].astype(float))
            std = round(np.std(df.iloc[1:,i].astype(float)), 3)
            range_min = np.min(df.iloc[1:,i].astype(float))
            range_max = np.max(df.iloc[1:,i].astype(float))
            axs[i].plot(range(1,len(df)), df.iloc[1:,i])
            axs[i].set_title(df.columns[i])
            axs[i].set_xlabel('Mean: {}\nMedian: {}\nSigma: {}\nRange: {} - {}'.format(mean, median, std, range_min, range_max))
    plt.tight_layout()
    plt.savefig("{}_analysis.png".format(filename.split('/')[-1].split('.')[0]))

if __name__ == "__main__" : 
    main()