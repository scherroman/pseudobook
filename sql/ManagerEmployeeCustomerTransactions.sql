-- Manager-Level Transactions
-- The manager should be able to:
-- Add, Edit and Delete information for an employee
-- INSERT INTO `Employee`(`userID`,`SSN`,`startDate`,`hourlyRate`)
-- VALUES(?,?,?,?);

-- UPDATE Employee
-- SET `hourlyRate` = ?
-- WHERE `userID` = ?;

-- DELETE FROM Employee
-- WHERE `userID` = ?;

-- Obtain a sales report for a particular month
DROP VIEW SalesReport;

CREATE VIEW SalesReport AS
SELECT A.itemName AS ItemName, A.adType AS ItemType, A.adID AS ItemID, A.company AS Company, A.unitPrice AS Price, CONCAT(E.firstName,' ',E.lastName) AS CustomerRepName, E.userID AS CustomerRepID, CONCAT(B.firstName,' ',B.lastName) AS CustomerName, B.userID AS CustomerID, B.email AS CustomerEmail, S.buyerAccount AS CustomerAccountNumber, S.numberOfUnits AS UnitsSold, S.transactionDateTime AS TransactionDateTime
FROM Sales S
JOIN Advertisement A ON S.adID = A.adID
JOIN `User` E ON A.employeeID = E.userID
JOIN `User` B ON S.buyerID = B.userID;

SELECT ItemName, ItemType, Company, CustomerRepName, CustomerName, UnitsSold, Price, TransactionDateTime
FROM SalesReport
WHERE TransactionDateTime >= '2015-12-10T00:00:00' AND TransactionDateTime <= '2016-1-1T00:00:00';

-- Produce a comprehensive listing of all items being advertised on the site
SELECT A.itemName AS ItemName, A.company AS Company, A.adType AS AdType, A.datePosted AS DatePosted, CONCAT(E.firstName,' ',E.lastName) AS EmployeePoster, A.unitPrice AS UnitPrice, A.numberAvailableUnits AS AvailableUnits
FROM Advertisement A
JOIN `User` E ON A.employeeID = E.userID;

-- Produce a list of transactions by item name or by user name
SELECT ItemName, ItemType, Company, CustomerRepName, CustomerName, UnitsSold, Price, TransactionDateTime
FROM SalesReport
WHERE ItemName = 'quis lectus. Nullam';

SELECT ItemName, ItemType, Company, CustomerRepName, CustomerName, UnitsSold, Price, TransactionDateTime
FROM SalesReport
WHERE CustomerName = 'Moses Kramer';

-- Produce a summary listing of revenue generated by a particular item, item type, or customer
SELECT SUM(Price * UnitsSold)
FROM SalesReport
WHERE ItemName = 'quis lectus. Nullam';

SELECT SUM(Price * UnitsSold)
FROM SalesReport
WHERE ItemType = 5;

SELECT SUM(Price * UnitsSold)
FROM SalesReport
WHERE CustomerName = 'Josiah Gates';

-- Determine which customer representative generated most total revenue
SELECT CustomerRepName, Revenue FROM (
	SELECT CustomerRepName, SUM(Price * UnitsSold) AS Revenue
	FROM SalesReport
	GROUP BY CustomerRepID
    ORDER BY SUM(Price * UnitsSold) DESC
    LIMIT 1
) R;

-- Determine which customer generated most total revenue
SELECT CustomerName, Revenue FROM (
	SELECT CustomerName, SUM(Price * UnitsSold) AS Revenue
	FROM SalesReport
	GROUP BY CustomerID
    ORDER BY SUM(Price * UnitsSold) DESC
    LIMIT 1
) R;

-- Produce a list of most active items
SELECT ItemName, ItemType, Company, SUM(UnitsSold) AS TotalUnitsSold
From SalesReport
GROUP BY ItemID
ORDER BY SUM(UnitsSold) DESC;

-- Produce a list of all customers who have purchased a particular item
SELECT CustomerName
FROM SalesReport
WHERE ItemID = 7;

-- Produce a list of all items for a given company
SELECT itemName, adType
FROM Advertisement
WHERE company = 'Orci LLP';
 
 
-- Customer-Representative-Level Transactions
-- Customer Representatives should be thought of as sales agents and should be able to:
-- Create an advertisement
-- INSERT INTO Advertisement (`employeeID`,`adType`,`datePosted`,`company`,`itemName`,`content`,`unitPrice`,`numberAvailableUnits`)
-- VALUES(?,?,?,?,?,?,?,?);

-- Delete an advertisement
-- DELETE FROM Advertisement
-- WHERE adID = ?;

-- Record a transaction
-- UPDATE Sales
-- SET approved = 1
-- WHERE transactionID = ?;

-- Add, Edit and Delete information for a customer


-- Produce customer mailing lists
SELECT CustomerName
FROM SalesReport
WHERE Company = 'Orci LLP';

-- Produce a list of item suggestions for a given customer (based on that customer's past transactions)
SELECT A.adID AS AdID, A.itemName AS ItemName, A.unitPrice AS UnitPrice, S.Company
FROM Advertisement A
JOIN SalesReport S ON A.company = S.Company
WHERE S.CustomerID = 1;
 
-- Customers should also be able to perform the following transactions with regard to advertisements:
-- Purchase one or more copies of an advertised item
-- INSERT INTO ` (`adID`,`buyerID`,`transactionDateTime`,`numberOfUnits`,`approved`)
-- VALUES (?,?,?,?,?);
 
-- While customers (users) will not be permitted to access the database directly, they should be able to retrieve the following information:
-- A customer's current groups
SELECT G.groupID, G.groupName, G.groupType
FROM `Group` G
JOIN GroupUsers GU ON GU.groupID = G.groupID
WHERE GU.userID = 10;

-- For each of a customer's accounts, the account history
SELECT UA.creditCardNumber, UA.accountNumber, S.ItemName, S.Price, S.UnitsSold AS ItemsPurchased, S.Price * S.UnitsSold AS AmountSpent
FROM SalesReport S
JOIN UserAccounts UA ON S.CustomerID = UA.userID AND UA.accountNumber = S.CustomerAccountNumber
WHERE S.CustomerID = 1;

-- Best-Seller list of items
SELECT ItemName, ItemType, Company, SUM(UnitsSold) AS TotalUnitsSold
FROM SalesReport
GROUP BY ItemID
ORDER BY Sum(UnitsSold) DESC;

-- Personalized item suggestion list (same as a sales rep producing a list of suggestions for a customer)
SELECT A.adID AS AdID, A.itemName AS ItemName, A.unitPrice AS UnitPrice, S.Company
FROM Advertisement A
JOIN SalesReport S ON A.company = S.Company
WHERE S.CustomerID = 1;