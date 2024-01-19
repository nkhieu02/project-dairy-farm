-- For those drivers who collected milk on 14 Oct 2019, display the driverID, 
-- the visited DairyID and its name, along with the information (‘Y’ or ‘N’)
--  on whether or not the visited dairy was organic.
-- Query 1

SELECT MilkRunInfo.driverID, DairyFarm.farmID, DairyFarm.name, DairyFarm.organic 
FROM DairyFarm, Stops, MilkRunInfo
WHERE (MilkRunInfo.date_arrive = Date '2019-10-14')
	AND (MilkRunInfo.routeID = Stops.routeID)
	AND (Stops.dairyFarmID = DairyFarm.farmID) ;
				
-- Display the day on which no milk was pumped into silo S2.
-- Query 2
SELECT DISTINCT date_arrive
FROM MilkRunInfo
WHERE date_arrive NOT IN(
SELECT date_arrive FROM MilkRunInfo WHERE silo = 'S2');

-- Display, for each of the planned (three) routes, the farm ID that is visited last on the route. Hint: use a multiple-column subquery.
-- Query 3

SELECT routeID, dairyfarmID  FROM stops, (SELECT routeID AS routeID1, MAX(position) FROM stops GROUP BY routeID) AS second WHERE (routeID = routeID1) AND (position = max); 

-- Display the driverID, name and phone no of those drivers who are either female or who have (at some point) picked up milk from an organic farm. 
-- Sort according to the driver’s last name.
-- Query 4

(SELECT Driver.ID, firstName, lastName, phone 
FROM Driver
WHERE (gender = 'F'))
UNION 
(SELECT Driver.ID, firstName, lastName, phone 
FROM Driver, MilkRunInfo, Stops, DairyFarm
WHERE ((Driver.ID = MilkRunInfo.driverID) 
AND (MilkRunInfo.routeID = Stops.routeID)
AND (Stops.dairyFarmID = DairyFarm.farmID)
AND (DairyFarm.organic = TRUE)))
ORDER BY lastName DESC ;
 							
-- Drivers’ log: for the period of five days 14-18 Oct., display, for each driver, the route used along with the following aggregated info: the total no of dairy farms visited, 
-- the total amount of milk collected, the average Milk protein% and the highest SCC value encountered in the route. 
-- Query 5

SELECT Driver.ID AS DriverID, MilkRunInfo.routeID AS Route, COUNT(DailyStop.dairyFarmID) AS totalNoOfDairyFarms, SUM(DailyStop.amount) AS totalMilk, AVG(mprotot) AS averageMilkProteinPER, MAX(DailyStop.scc) AS highestSCC
FROM Driver, DailyStop, MilkRunInfo
WHERE (DailyStop.date >=  Date '2019-10-14' AND DailyStop.date <= Date '2019-10-18')
	AND (Driver.ID = MilkRunInfo.driverID)
	AND (MilkRunInfo.routeID = DailyStop.routeID)
	AND (DailyStop.date = MilkRunInfo.date_arrive)
GROUP BY Driver.ID, MilkRunInfo.routeID ;
						
-- Assume that we consider milk in a silo with a SCC value of 173000 as the threshold value beyond which the milk ceases to be of premium quality for cheese making.
-- In an effort to identify those dairy farms who may have contributed to such milk, find all silos with a SCC level higher than the threshold value (on any day). 
-- Display, for those silos, the date (that the milk was pumped into the silo), the SCC in the silo, and each dairy farm ID where the SCC has exceeded the threshold value, 
-- along with the actual SCC value found in the sample collected at the displayed dairy farm.
-- Query 6

SELECT MilkRunInfo.Date_arrive AS Date, MilkRunInfo.scc AS sccAtSilo, DailyStop.dairyFarmID AS Farm, dailyStop.scc AS sccAtFarm
FROM MilkRunInfo, DailyStop, Stops
WHERE MilkRunInfo.scc>173000
	AND (MilkRunInfo.routeID = Stops.routeID)
	AND (Stops.dairyFarmID = DailyStop.dairyFarmID)
           AND (DailyStop.date = MilkRunInfo.Date_arrive)
ORDER BY MilkRunInfo.date_arrive; 
 						 	
-- Produce an SQL ‘quality report’ showing for each farm, the average amount of milk produced in Kgs1, 
-- the maximum SCC value, and the info on whether the farm is organic or not. 
-- Query 7

SELECT DairyFarm.farmID, AVG(DailyStop.amount*1.035) AS avergeMilkKgs, MAX(DailyStop.scc) AS maxSCC, DairyFarm.organic AS isOrganic
FROM DailyStop, DairyFarm
WHERE DailyStop.dairyFarmID = DairyFarm.farmID
GROUP BY DairyFarm.farmID;
