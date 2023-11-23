#!/usr/bin/env python3
import argparse, csv, sys
import pandas as pd, numpy as np, matplotlib.pyplot as plt

# Purpose of program is to read a csv file and do stuff with it

def main():
    """Get user input, then call csv_tool."""
    (file, dialect) = parse_args(sys.argv[1:])
    csv_tool(file, dialect)

def parse_args(input_args):
    """Parse command line arguments, return tuple of file and dialect."""
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
    """Attempt to open file and call stat_maker, return error code.
    
    Return codes:
    -1: Error opening file
    0: File is empty
    >=1: Number of lines in file"""
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
                # check for header
                fp.seek(0)
                head = csv.Sniffer().has_header(fp.read(1024))
                df = pd.read_csv(filename, header=0 if head else None)
                # ask user what they want to do
                actions = input("What anaylsis would you like done? Field plots (1); SVD (2); Both (3)\n")
                if actions == '1':
                    stat_maker(df, filename)
                elif actions == '2':
                    svd(df, filename)
                else:
                    stat_maker(df, filename)
                    svd(df, filename)
    except FileNotFoundError as e:
        print("File {} not found: {}".format(filename, e))
    except IOError as e:
        print("Error handling file {}: {}".format(filename, e))
    finally:
        if fp: fp.close()
    return cnt

def stat_maker(df, filename):
    """Read csv file, save plots and stats of numeric columns in a pdf."""
    # find numeric columns
    col_types = df.dtypes
    numeric_tracker = [True if i in ['int64', 'float64', 'complex128'] else False for i in col_types]
    # plot numeric columns
    fig, axs = plt.subplots(np.sum(numeric_tracker), 1, figsize=(10, 10*np.sum(numeric_tracker)))
    axs_cnt=0
    for i in range(len(df.columns)):
        if numeric_tracker[i]:
            mean = round(np.sum(df.iloc[:,i].astype(float))/len(df.iloc[1:,i]), 3)
            median = round(np.median(df.iloc[:,i].astype(float)), 3)
            std = round(np.std(df.iloc[:,i].astype(float)), 3)
            range_min = round(np.min(df.iloc[:,i].astype(float)), 3)
            range_max = round(np.max(df.iloc[:,i].astype(float)), 3)
            axs[axs_cnt].plot(range(0,len(df)), df.iloc[:,i])
            axs[axs_cnt].set_title(df.columns[i])
            x = 'x'
            axs[axs_cnt].set_xlabel(f'Mean: {mean}\nStandard Deviation: {std}\n Median: {median}\nRange: [{range_min}, {range_max}]')
            #f'$\\bar{x}$: {mean}\n$\\sigma$: {std}\n Median: {median}\nRange: [{range_min}, {range_max}]'
            axs_cnt+=1
    plt.tight_layout()
    plt.savefig("{}_analysis.pdf".format(filename.split('/')[-1].split('.')[0]))

def svd(df, filename):
    """Perform SVD on dataframe, save U, D, V^T matrices in csv files."""
    U, D, Vt = np.linalg.svd(np.array(df))
    np.savetxt("{}_U.csv".format(filename.split('/')[-1].split('.')[0]), U, delimiter=",")
    np.savetxt("{}_D.csv".format(filename.split('/')[-1].split('.')[0]), D, delimiter=",")
    np.savetxt("{}_Vt.csv".format(filename.split('/')[-1].split('.')[0]), Vt, delimiter=",")
    
if __name__ == "__main__" : 
    main()