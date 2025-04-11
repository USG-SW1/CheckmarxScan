#!/usr/bin/env python3
import pandas as pd
import glob


tmp = pd.read_excel('temp.xlsx')
# 筛选出 Priority 列值为 "H" 的行
tmp = tmp[tmp['Priority'] == 'H']
tmp['Apps'] = tmp['Apps'].str.replace('./', '')
filtered_df = tmp.drop(columns=tmp.columns.difference(['Apps', 'Owner']))
# 打印筛选后的 DataFrame
#print(filtered_df)
result_array = filtered_df.set_index('Apps')['Owner'].to_dict()


# 获取所有CSV文件的文件路径
csv_files = glob.glob('checkmarx/Reports/*.csv')

# 创建一个空的DataFrame，用于存储合并后的数据

combined_df = pd.DataFrame()


# 逐个读取并合并每个CSV文件
for file in csv_files:
    df = pd.read_csv(file)
    line = file.rpartition('/')[2]
    print (line)
    line = line[:-4]
    print (line)
    df['Apps'] = df['SrcFileName'].str.split('/').str[1]
    df['Owner'] = df['Apps'].str.replace('./', '').map(result_array)
    df['QueryPath'] = df['QueryPath'].str.replace('版本', 'version', regex=False)
    combined_df = pd.concat([combined_df, df], ignore_index=True)
    # 新增列 'Check Result (Resolved / NAP)' 并初始化为空值
    combined_df['Result Severity'] = combined_df['Result Severity'].replace({
        '中風險': 'medium',
        '高風險': 'high',
        '低風險': 'low'
    })
    combined_df['Check Result (Resolved / NAP)'] = ''
    combined_df['Result Status'] = combined_df['Result Status'].replace({
        '新的': 'new',
        '舊的': 'old'
    })
    combined_df['Result State'] = combined_df['Result State'].replace({
        '校驗': 'check',
        '舊的': 'old'
    })
    
# 将合并后的DataFrame写入新的CSV文件
output_file = 'combined_file.csv'
combined_df.to_csv(output_file, index=False, encoding = 'big5')

# 打印合并后的DataFrame
print(combined_df)
