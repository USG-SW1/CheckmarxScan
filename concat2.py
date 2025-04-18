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
#csv_files = glob.glob('checkmarx/Reports/*.csv')
tmp_files = [
'zyxel-gui-1.0.0',
'sr2txtd',
]


csv_files = [f'./Checkmarx/Reports/{name}.csv' for name in tmp_files]

# 创建一个空的DataFrame，用于存储合并后的数据

combined_df = pd.DataFrame()



# 逐个读取并合并每个CSV文件
for file in csv_files:
    df = pd.read_csv(file)
    line = file.rpartition('/')[2]
    print (line)
    line = line[:-4]
    print (line)
    df['Apps'] = line
    df['Owner'] = result_array[line]
    combined_df = pd.concat([combined_df, df], ignore_index=True)

# 将合并后的DataFrame写入新的CSV文件
output_file = 'combined_file_new.csv'
combined_df.to_csv(output_file, index=False, encoding = 'big5')

# 打印合并后的DataFrame
print(combined_df)
