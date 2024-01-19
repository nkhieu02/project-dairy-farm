-- Planned Route:
CREATE TABLE PlannedRoute (
                      ID VARCHAR PRIMARY KEY
                            );
-- Stops:
CREATE TABLE Stops (
            routeID VARCHAR NOT NULL,
            dairyFarmID VARCHAR NOT NULL,
            position INTEGER,
            PRIMARY KEY(routeID, dairyFarmID),
            FOREIGN KEY (routeID)  REFERENCES PlannedRoute(ID) ON DELETE SET NULL ON UPDATE CASCADE,
            FOREIGN KEY(dairyFarmID) REFERENCES DairyFarm(FarmID) ON DELETE SET NULL ON UPDATE CASCADE
                            );
--DailyStops
CREATE TABLE DailyStop (
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
--Drivers
CREATE TABLE Driver(
            ID VARCHAR PRIMARY KEY NOT NULL,
            gender CHAR NOT NULL CHECK (gender in ('F','M')),
            firstName VARCHAR, 
            lastName VARCHAR,
            address VARCHAR,
            phone NUMERIC,
            dateStarted DATE
                          );
--DairyFarm
CREATE TABLE DairyFarm (
            farmID VARCHAR PRIMARY KEY,
            name VARCHAR,
            organic BOOLEAN,
            address VARCHAR,
            latitude REAL,
            longitude REAL
                          );
--MilkRunInfo
CREATE TABLE MilkRunInfo (
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
