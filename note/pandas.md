## pandas

####pandas安装
* pip install pandas

####打开pandas
import pandas as pd
df =pd.read_csv('problemPlat.csv',parse_dates=True)
1. df.head() 查看头部行
2. df.tail() 查看尾部行
3. df.index 显示索引
4. df.columns 显示列名
5. df.values 显示numpy底层数据
