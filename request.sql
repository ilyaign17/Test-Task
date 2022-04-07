
GO

-- Задача 1 (создание)

CREATE FUNCTION select_orders_by_item_name(@name_thing nvarchar(30))  
RETURNS TABLE  
AS    
RETURN
(
	SELECT Orders.row_id, Customers.name, COUNT(Orders.row_id) AS 'Count Things'
	FROM Orders 
	JOIN OrderItems ON OrderItems.order_id = Orders.row_id 
	JOIN Customers ON Orders.customer_id = Customers.row_id
	WHERE OrderItems.name = @name_thing
	GROUP BY Orders.row_id, Customers.name
);


GO

-- Задача 2 (создание)


CREATE FUNCTION calculate_total_price_for_orders_group(@row_id int)
RETURNS int   
AS
BEGIN 
    DECLARE @group_name nvarchar(30), @total_price int;
    SET @group_name = 
	(
		SELECT group_name
		FROM Orders 
		WHERE row_id = @row_id
	);

	IF @group_name IS NULL
        SELECT @total_price = SUM(OrderItems.price)
        FROM OrderItems
        WHERE OrderItems.order_id = @row_id;
    ELSE
        WITH
		Item(row_id, parent_id, group_name) 
		AS 
		(
            SELECT row_id, parent_id, group_name
            FROM Orders
            WHERE parent_id = @row_id
            UNION ALL
            SELECT d.row_id, d.parent_id, d.group_name
            FROM orders d
            JOIN Item ON Item.row_id = d.parent_id
		)

        SELECT @total_price = SUM(price)
		FROM Item
        JOIN OrderItems ON OrderItems.order_id = Item.row_id
        WHERE Item.group_name IS NULL;
        RETURN @total_price;
END; 


GO

-- Задача 1 (вызов)

SELECT * FROM select_orders_by_item_name(N'Факс');
SELECT * FROM select_orders_by_item_name(N'Кассовый аппарат');
SELECT * FROM select_orders_by_item_name(N'Стулья');

-- Задача 2 (вызов)

SELECT dbo.calculate_total_price_for_orders_group(1) AS total_price;
SELECT dbo.calculate_total_price_for_orders_group(2) AS total_price;
SELECT dbo.calculate_total_price_for_orders_group(3) AS total_price;
SELECT dbo.calculate_total_price_for_orders_group(12) AS total_price;
SELECT dbo.calculate_total_price_for_orders_group(13) AS total_price;

-- Задача 3 (создание и вызов)

SELECT Customers.name
FROM Customers
JOIN Orders ON Orders.customer_id = Customers.row_id
JOIN OrderItems ON Orders.row_id = OrderItems.order_id
WHERE YEAR (Orders.registered_at) = 2020
GROUP BY Customers.name, Customers.row_id
HAVING COUNT(DISTINCT OrderItems.order_id) = COUNT(DISTINCT CASE WHEN OrderItems.name = 'Кассовый аппарат' THEN OrderItems.order_id END);