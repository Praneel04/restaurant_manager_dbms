use newrest1;
DELIMITER $$
CREATE PROCEDURE AddMenuItem(IN itemName VARCHAR(100), IN itemPrice DECIMAL(10, 2))
BEGIN
    INSERT INTO Item (Name, Price) VALUES (itemName, itemPrice);
END $$
DELIMITER ;
DELIMITER $$
CREATE PROCEDURE RemoveMenuItem(IN itemId INT)
BEGIN
    DELETE FROM Item WHERE Item_id = itemId;
END $$
DELIMITER ;
DELIMITER $$

DELIMITER ;
DELIMITER $$
CREATE PROCEDURE PlaceOrder(
    IN customerID INT,
    IN totalAmount DECIMAL(10, 2),
    IN staffID INT,
    IN tableID INT,
    OUT newOrderID INT
)
BEGIN
    -- Insert a new order
    INSERT INTO Orders (CustomerID, TotalAmount, OrderTime, Status, Notes, StaffID, TableID)
    VALUES (customerID, totalAmount, NOW(), 'Pending', '', staffID, tableID);
    
    -- Get the last inserted OrderID
    SET newOrderID = LAST_INSERT_ID();
    
    -- Mark the table as occupied
    UPDATE `Tables` SET IsOccupied = TRUE WHERE Table_id = tableID;
END $$
DELIMITER ;
DELIMITER $$
CREATE PROCEDURE AddOrderDetails(
    IN orderID INT,
    IN itemID INT,
    IN quantity INT,
    IN unitPrice DECIMAL(10, 2),
    IN totalPrice DECIMAL(10, 2)
)
BEGIN
    INSERT INTO OrderDetails (OrderID, ItemID, Quantity, UnitPrice, TotalPrice)
    VALUES (orderID, itemID, quantity, unitPrice, totalPrice);
END $$
DELIMITER ;
DELIMITER $$
CREATE PROCEDURE `MakeReservation`(
    IN p_table_id INT,
    IN p_customer_id INT,
    IN p_reservation_time DATETIME,
    IN p_num_people INT
)
BEGIN
    DECLARE max_capacity INT;

    -- Check the table capacity
    SELECT Total_people INTO max_capacity FROM `Tables` WHERE Table_id = p_table_id;

    -- If the number of people exceeds the table's capacity, signal an error
    IF p_num_people > max_capacity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'The selected table cannot accommodate the specified number of people.';
    ELSE
        -- Insert a new reservation
        INSERT INTO Reservation (Table_id, Customer_id, Time, Number_of_people)
        VALUES (p_table_id, p_customer_id, p_reservation_time, p_num_people);

        -- Mark the table as occupied
        UPDATE `Tables` SET IsOccupied = TRUE WHERE Table_id = p_table_id;
    END IF;
END$$
DELIMITER ;
