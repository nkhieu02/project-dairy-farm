import pandas as pd
import numpy as np


#File name
file_name = ".\project-dairy-farm\data\SampleData_for_Dairy_Farms.xls"
#Farms to csv
df_farm = pd.read_excel(file_name, sheet_name= "Farms", dtype = {"FarmID" : object})
df_farm.drop(["PostalCode", "Municipality"],axis = 1, inplace = True)
df_farm["IsOrganic"].replace({"N" : False, "Y": True}, inplace= True)
df_farm.rename(columns = {"Farm Name" : "name", "IsOrganic" : "organic", "Farm's address" : "address"}, inplace = True)
#print(df_farm.columns)
#df_farm.to_csv(r".\project-dairy-farm\data\DairyFarm.csv", index = False, header = df_farm.columns )
# Drivers to csv
df_drivers = pd.read_excel(file_name, sheet_name = "Drivers", dtype = {"FirstName" : object, "LastName" : object, "Address" : object, "Phone" : object })
df_drivers.rename(columns = {"DriverID" : "ID", "DateContractStarted" : "dateStarted"}, inplace = True)
df_drivers["dateStarted"] = pd.to_datetime(df_drivers["dateStarted"], errors= "coerce")
df_drivers = df_drivers[df_drivers["dateStarted"].notnull()]
df_drivers.to_csv(r".\project-dairy-farm\data\Driver.csv", index = False, header = df_drivers.columns )
#print(df_drivers.columns)
#Planned Milk Route to csv
df_route = pd.read_excel(file_name, sheet_name = "PlannedMIlkRoute",header = 3 )
df_route.dropna(axis = "columns", how = "all", inplace = True)
df_route = df_route.melt(id_vars= ["RouteID", ], value_name= "dairyFarmID", var_name= "position" )
df_route["position"] = [int(x[-1]) for x in df_route["position"]]
df_route = df_route[df_route["dairyFarmID"].notnull()]
df_stops = df_route.copy() 
df_stops_1 = df_stops.drop(columns = ["position"]) #Stops
df_stops["dairyFarmID"] = df_stops["dairyFarmID"].astype(dtype= int, copy = True)
df_stops = df_stops[["RouteID", "dairyFarmID", "position"]]
df_route.drop(columns = ["dairyFarmID", "position"], inplace = True)
df_route.drop_duplicates(inplace = True)
#df_route.to_csv(r".\project-dairy-farm\data\PlannedRoute.csv", index = False, header = df_route.columns )
#df_stops.to_csv(r".\project-dairy-farm\data\Stops.csv", index = False, header = df_stops.columns )
print(df_stops)
#print(df_route.columns)
#print(df_stops.columns)
#Daily Stop to csv
df_dailyStop = pd.read_excel(file_name, sheet_name = "MilkPickUp", header= 1)
df2_dailyStop = df_dailyStop[df_dailyStop["Milk"].notnull()]
df3_dailyStop = df2_dailyStop.melt(id_vars=["Date", "Milk"], var_name="farmID", value_name="farm")
df4_dailyStop = df3_dailyStop.pivot(index=["Date", "farmID"], columns="Milk", values="farm").reset_index()
df4_dailyStop["Date"] = pd.to_datetime(df4_dailyStop["Date"], errors= "coerce")
df4_dailyStop = df4_dailyStop[df4_dailyStop["Date"].notnull()]
#Create routeID
routes = df_stops_1.values
route_dict = {}
for route in routes:
    route_dict[route[1]] = route[0]
route_list = [route_dict[x] for x in df4_dailyStop["farmID"]]
df4_dailyStop["routeID"] = route_list
df4_dailyStop.rename(columns = {"Liters" : "amount", "farmID" : "dairyFarmID", "Mfat": "mfat", "Mprot" : "mprotot", "SCC" : "scc"}, inplace = True)
df4_dailyStop = df4_dailyStop[["Date", "amount", "mfat", "mprotot", "scc", "routeID", "dairyFarmID"]]
df4_dailyStop.to_csv(r".\project-dairy-farm\data\DailyStop.csv", index = False, header = df4_dailyStop.columns )
##df_dailyStop.info()
# Silos to csv
df_silo = pd.read_excel(file_name, sheet_name ="SiloLog", header = 2 )
df_silo.dropna(axis = "columns", how = "all",inplace = True)
df_silo.dropna(axis = "index", how = "all", inplace = True)
print(df_silo)
df_silo["Date"] = pd.to_datetime(df_silo["Date"], errors= "coerce")
df_silo = df_silo[df_silo["Date"].notnull()]
df_silo = df_silo.astype(dtype = {"Total Milk" : float, "MfatAvg": float,"MprotAvg" : float,"SCCAvg" : float })
df_silo = df_silo[["Date", "Silo", "MfatAvg", "MprotAvg", "SCCAvg", "Total Milk", "Milk Route", "Driver"]]
df_silo.rename(columns= {"Date" : "date_arrive", "MfatAvg": "mfat", "MprotAvg" : "mprot",\
                                "SCCAvg" : "scc", "Total Milk" : "totalAmount", "Milk Route" : "routeID", \
                                    "Driver" : "driverID"}, inplace = True)
#df_silo.to_csv(r".\project-dairy-farm\data\MilkRunInfo.csv", index = False, header = df_silo.columns )
#print(df_silo.columns)

#CSV_names = ["DailyStop", "DairyFarm", "Driver", "MilkRunInfo", "PlannedRoute", "Stops"]



