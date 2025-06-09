import argparse
import re



parser = argparse.ArgumentParser(description='程式描述')

def process_string(s):
#    print(s)
    first_slash_index = s.find("/")
#    print(first_slash_index)
#    second_slash_index = s.find("\\", first_slash_index + 1)
#    print(second_slash_index)
    return s[0:first_slash_index]


parser.add_argument('-f', '--file', type=str, help='CSV 檔案的路徑')
args = parser.parse_args()
csv_file = args.file
#設定 CSV 檔案的參數

import pandas as pd

# 讀取 CSV 檔案
with open("r.txt", "r")as file:
    line = file.readline()
    while line:
        line = line.strip()
        line = 'Checkmarx/Reports/' + line + '.csv'
        line = 'combined_file.csv'
        print(line)
        df = pd.read_csv(line)

# 進行相應的操作，例如顯示前幾行資料
#print(df.columns)
        ab = df[['SrcFileName', 'Result Severity']].copy()
#print(ab)
        ab['SrcFileName'] =  ab['SrcFileName'].apply(process_string)
#print(ab)

        with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
            count = ab.groupby('Result Severity')['Result Severity'].value_counts()
    #count = ab.sort_values(by=['SrcFileName', 'Result Severity']).value_counts()
            print(count)
        line = file.readline()
