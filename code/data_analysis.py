from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

database="grp2_dairyfarm" # TO BE REPLACED
user='grp02'   # TO BE REPLACED
password='!XxIy#YG' # TO BE REPLACED
host='dbcourse2022.cs.aalto.fi' 
port= '5432'

# postgres URL
postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}' \
               .format(username=user,
                       password=password,
                       ipaddress=host,
                       port=port,
                       dbname=database))

#Create engine
cnx = create_engine(postgres_str)
 
# Query
query_for_df =  """SELECT farmID, organic, sum, A1, A2,min, max   FROM DairyFarm
INNER JOIN (  SELECT dairyFarmID, SUM(amount) , avg(mfat) as A1, avg(mprotot) as A2, min(scc) , max(scc) 
                         FROM DailyStop 
                         GROUP BY dairyFarmID) as vals 
ON DairyFarm.farmID = vals.dairyFarmID ; """
# Read the query to dataframe
df_DFarms = pd.read_sql_query(query_for_df, con = cnx)
#Columns' name
columns = ['Farm ID', 'Organic', 'Total Amount', 'Avg. MFat', 'Avg. Mprot', 'Min. SCC', 'Max. SCC'] 
df_DFarms.columns = columns

#Transfer dataframe to PSQL table
with cnx.connect() as connection : 
    df_DFarms.to_sql(name = "DFarms", con = connection, if_exists = 'replace', index=True)

# two new dataframes, df DFarms A and df DFarms B for non-organic and
# organic farms respectively
df_DFarms_A = df_DFarms[df_DFarms["Organic"] != True]
df_DFarms_B = df_DFarms[df_DFarms["Organic"] == True]

# Rank by Max. SCC
df_DFarms_A_ranked = df_DFarms_A.sort_values(by = "Max. SCC")
df_DFarms_B_ranked = df_DFarms_B.sort_values(by = "Max. SCC")
print(df_DFarms_A_ranked)
print(df_DFarms_B_ranked)
# Qlty = MFat% + MProt%.
df_DFarms_A["Qlty"] = df_DFarms_A['Avg. MFat'] + df_DFarms_A['Avg. Mprot']
print(df_DFarms_A)

# Select values of FarmID as columns
df_DFarms_A_1 = df_DFarms_A.pivot(index = None, columns = "Farm ID", values = "Qlty" )
print(df_DFarms_A_1)

#Mapping for each scc
def cal_scc_index(scc):
    if scc < 140000:
        return 1
    elif scc < 173000:
        return (0.8 -1) / (173000 - 140000) * (scc - 173000) + 0.8
    elif scc < 200000:
        return (-0.8)/ (200000 - 173000) * (scc - 200000)
    else:
        return 0

#Plot the function above:
x = np.arange(130000, 220000, 0.01)
y = [cal_scc_index(scc) for scc in x]
plt.plot(x,y)
plt.xlabel("Max SCC value")
plt.ylabel("SCC Index")

# Create nex SCCIndex column
df_DFarms_A["SCCIndex"] = df_DFarms_A["Max. SCC"].apply(cal_scc_index)
print(df_DFarms_A["SCCIndex"])

# Farms ranked by two kind of values
farms_ranked_by_sccindex = df_DFarms_A.sort_values(by = ["SCCIndex"])["Farm ID"] 
farms_ranked_by_maxscc = df_DFarms_A.sort_values(ascending = False, by = ["Max. SCC"])["Farm ID"]

# Rank of farms 1001 - 1010

rank_maxscc = farms_ranked_by_maxscc.reset_index().sort_values(by = ["Farm ID"]).index
rank_sccindex = farms_ranked_by_sccindex.reset_index().sort_values(by = ["Farm ID"]).index
print(rank_maxscc)
print(rank_sccindex)
#corr matrix
corr = np.corrcoef(rank_maxscc, rank_sccindex)[0,1]
print(corr)