'''Generate list of dataframes from the Heritage Economic Freedom Index'''

from Freedom.fnames import names
import pandas as pd
import os

gdp = pd.read_excel("http://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=excel", Sheet_name='Data',header=3)['Country Name']
table_xls = os.listdir('Freedom/Freedom')
freedom = pd.DataFrame(pd.read_excel('Freedom/Freedom/'+table_xls[0])[table_xls[0][5:9]+" Score"].append(pd.Series([0]), ignore_index=True).loc[:185], columns=[2013])
for k,i in enumerate(table_xls[1:]):
    freedom = freedom.join(pd.DataFrame(pd.read_excel('Freedom/Freedom/'+i)[i[5:9]+" Score"].append(pd.Series([0]), ignore_index=True).loc[:185], columns=[2014+k]), how="outer")
freedom.index = names
freedom = freedom.reindex(gdp).dropna(how='all')