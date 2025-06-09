#!/usr/bin/env python3
import pandas as pd
import glob


tmp = pd.read_excel('temp.xlsx')
tmp_nap = pd.read_excel('checkmarx-nap.xlsx')
print("tmp_nap columns:", tmp_nap.columns.tolist())
# 列出 key='DestFileName' 的所有记录
if 'DestFileName' in tmp_nap.columns:
    print("All records with key 'DestFileName':")
    print(tmp_nap['DestFileName'])
else:
    print("'DestFileName' column not found in tmp_nap")
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
    df['Apps'] = df['SrcFileName'].str.split('/').str[0]
    df['Owner'] = df['Apps'].str.replace('./', '').map(result_array)
    df['QueryPath'] = df['QueryPath'].str.replace('版本', 'version', regex=False)
    df['QueryPath'] = df['QueryPath'].str.replace('公司', 'Company', regex=False)
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
        '反覆出現的問題': 'old'
    })
    combined_df['Result State'] = combined_df['Result State'].replace({
        '校驗': 'check',
        '舊的': 'old'
    })

    for idx, nap_row in tmp_nap.iterrows():
        # Exclude 'Check Result (Resolved / NAP)' from comparison
        nap_compare = nap_row.drop(labels=['Check Result (Resolved / NAP)'], errors='ignore')
        # Find matching rows in combined_df
        mask = pd.Series([True] * len(combined_df))
        for col in nap_compare.index:
            if col in combined_df.columns:
                mask &= combined_df[col] == nap_row[col]
            else:
                mask &= False
        matched_indices = combined_df[mask].index
        if len(matched_indices) > 0:
            combined_df.loc[matched_indices, 'Check Result (Resolved / NAP)'] = nap_row.get('Check Result (Resolved / NAP)', '')
            # Debug print: print the full matched record(s)
            #for idx in matched_indices:
            #    print("Matched record in combined_df:")
            #    print(combined_df.loc[idx].to_dict())
        else:
            print(f"tmp_nap record not found: {nap_row.to_dict()}")
    
# 将合并后的DataFrame写入新的CSV文件
output_file = 'combined_file.csv'
combined_df.to_csv(output_file, index=False, encoding = 'big5')
# 統計每個 'App' 中 'Result Severity' 的數量
severity_counts = combined_df.groupby('Apps')['Result Severity'].value_counts().unstack(fill_value=0)

# 印出每個 'App' 的 'high', 'medium', 'low' 數量
for app, counts in severity_counts.iterrows():
    print(f"App: {app}")
    print(f"  High: {counts.get('high', 0)}")
    print(f"  Medium: {counts.get('medium', 0)}")
    print(f"  Low: {counts.get('low', 0)}")
# 打印合并后的DataFrame
print(combined_df)
