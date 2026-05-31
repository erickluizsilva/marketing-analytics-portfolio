
-- dim_products

SELECT
	ProductID,
	ProductName,
	Price,
	CASE
		WHEN Price < 50 THEN 'Low'
		WHEN Price < 199 THEN 'Medium'
		ELSE 'High'
	END AS CategoryPrice
FROM
	dbo.products;


-- dim_customers

SELECT
	t1.CustomerID,
	t1.CustomerName,
	t1.Email,
	t1.Gender,
	t1.Age,
	t2.Country,
	t2.City
FROM
	dbo.customers AS t1
LEFT JOIN dbo.geography AS t2
	ON t1.GeographyID = t2.GeographyID;


-- fat_customer_reviews

SELECT 
	ReviewID,
	CustomerID,
	ProductID,
	ReviewDate,
	Rating,
	REPLACE(ReviewText,'  ',' ') AS ReviewText
FROM
	dbo.customer_reviews;


-- fat_customer_journey

SELECT JourneyID,
	   CustomerID,
	   ProductID, 
	   VisitDate,
	   Stage,
	   Action,
	   COALESCE(Duration,avg_duration) AS Duration 
FROM (
	SELECT JourneyID,
		   CustomerID,
		   ProductID, 
		   VisitDate,
		   UPPER(Stage) AS Stage,
		   Action,
		   Duration,
		   AVG(Duration) OVER (
		   PARTITION BY VisitDate
		   ) AS avg_duration,
		   ROW_NUMBER() OVER (
		   PARTITION BY CustomerID, ProductID, VisitDate, UPPER(Stage), Action 
		   ORDER BY JourneyID
		   ) AS RowNumber
	FROM customer_journey
) AS subquery
WHERE RowNumber = 1;