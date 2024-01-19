import psycopg2
from psycopg2 import Error

try:
   # Connect to an test database 
   # NOTE: 
   # 1. NEVER store credential like this in practice. This is only for testing purpose
   # 2. Replace your "database" name, "user" and "password" that we provide to test the connection to your database 
   connection = psycopg2.connect(
   database="grp2_dairyfarm",  # TO BE REPLACED
   user='grp02',    # TO BE REPLACED
   password='!XxIy#YG', # TO BE REPLACED
   host='dbcourse2022.cs.aalto.fi', 
   port= '5432'
   )

   # Create a cursor to perform database operations
   cursor = connection.cursor()
   creat_table = """CREATE TABLE PlannedRoute (
                      ID VARCHAR PRIMARY KEY
                            );
                 """
   create_table_stop = """CREATE TABLE Stops (
            routeID VARCHAR NOT NULL,
            dairyFarmID VARCHAR NOT NULL,
            position INTEGER,
            PRIMARY KEY(routeID, dairyFarmID),
            FOREIGN KEY (routeID)  REFERENCES PlannedRoute(ID) ON DELETE SET NULL ON UPDATE CASCADE,
            FOREIGN KEY(dairyFarmID) REFERENCES DairyFarm(FarmID) ON DELETE SET NULL ON UPDATE CASCADE
                            );
                """
   crete_table_dailyStop = """CREATE TABLE DailyStop (
            date DATE,
            amount REAL,
            mfat REAL,  
            mprotot REAL,
            scc REAL,
            routeID VARCHAR NOT NULL,
            dairyFarmID VARCHAR NOT NULL,
            PRIMARY KEY (date, routeID, dairyFarmID),
            FOREIGN KEY(routeID) REFERENCES PlannedRoute(ID) ON DELETE SET NULL ON UPDATE CASCADE,
            FOREIGN KEY(dairyFarmID) REFERENCES DairyFarm(FarmID) ON DELETE SET NULL ON UPDATE CASCADE
                          );
                 """
   create_table_driver  = """CREATE TABLE Driver(
            ID VARCHAR PRIMARY KEY NOT NULL,
            gender CHAR NOT NULL CHECK (gender in ('F','M')),
            firstName VARCHAR, 
            lastName VARCHAR,
            address VARCHAR,
            phone NUMERIC,
            dateStarted DATE
                          );
                """
   create_dairy_farm = """CREATE TABLE DairyFarm (
            farmID VARCHAR PRIMARY KEY,
            name VARCHAR,
            organic BOOLEAN,
            address VARCHAR,
            latitude REAL,
            longitude REAL
                          );
                """
   create_table_milkRunInfo = """CREATE TABLE MilkRunInfo (
            date_arrive DATE,
            silo VARCHAR CHECK (silo in ('S1', 'S2', 'S3')),
            mfat REAL,
            mprot REAL,
            scc REAL,
            totalAmount REAL,
            routeID VARCHAR NOT NULL,
            driverID VARCHAR NOT NULL,
            PRIMARY KEY (date_arrive, routeID, driverID),
            FOREIGN KEY (routeID) REFERENCES PlannedRoute(ID) ON DELETE SET NULL ON UPDATE CASCADE,
            FOREIGN KEY (driverID) REFERENCES Driver(ID) ON DELETE SET NULL ON UPDATE CASCADE
                                     );
                """
   #cursor.execute(creat_table)
   #cursor.execute(create_table_stop)
   #cursor.execute(creat_table_dailyStop)
   #cursor.execute(creat_table_driver)
   #cursor.execute(create_table_dairyFarm)
   #cursor.execute(creat_table_milkRunInfo)
   connection.commit()

except (Exception, Error) as error:
   print("Error while connecting to PostgreSQL", error)
finally:
   if (connection):
      cursor.close()
      connection.close()
      print("PostgreSQL connection is closed")