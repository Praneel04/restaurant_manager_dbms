-- Create Database
CREATE DATABASE IF NOT EXISTS newrest1;
USE newrest1;

-- Creating the Admin Table
CREATE TABLE IF NOT EXISTS admin (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);

-- Insert Sample Admin Data
INSERT INTO admin (username, password) VALUES ('admin', 'admin123');

-- Creating the Customer Table
CREATE TABLE Customer (
    Customer_id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    INDEX (Phone)
);

-- Creating the Tables Table for restaurant table reservations
CREATE TABLE Table (
    Table_id INT PRIMARY KEY AUTO_INCREMENT,
    Total_people INT NOT NULL,
    IsOccupied BOOLEAN DEFAULT FALSE
);
ALTER TABLE Tables
ADD COLUMN TableType VARCHAR(50);

-- Creating the Reservation Table
CREATE TABLE Reservation (
    Reservation_id INT PRIMARY KEY AUTO_INCREMENT,
    Table_id INT,
    Customer_id INT,
    Time DATETIME NOT NULL,
    Number_of_people INT,
    FOREIGN KEY (Table_id) REFERENCES Tables(Table_id),
    FOREIGN KEY (Customer_id) REFERENCES Customer(Customer_id)
);

-- Creating the Orders Table (Updated Schema)
CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT,
    TotalAmount DECIMAL(10, 2),
    OrderTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Status ENUM('Pending', 'Completed', 'Cancelled') DEFAULT 'Pending',
    Notes TEXT,
    StaffID INT,
    TableID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY (StaffID) REFERENCES Staff(Staff_id),
    FOREIGN KEY (TableID) REFERENCES Tables(Table_id)
);

-- Creating the Item Table
CREATE TABLE Item (
    Item_id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL
);

-- Creating the OrderDetails Table (Many-to-Many Relationship between Orders and Items)
CREATE TABLE OrderDetails (
    OrderID INT,
    ItemID INT,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10, 2),
    TotalPrice DECIMAL(10, 2),
    PRIMARY KEY (OrderID, ItemID),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ItemID) REFERENCES Item(Item_id)
);

-- Creating the Staff Table
CREATE TABLE Staff (
    Staff_id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    Staff_type VARCHAR(50),
    Rating FLOAT
);

-- Creating the Feedback Table
CREATE TABLE Feedback (
    Feedback_id INT PRIMARY KEY AUTO_INCREMENT,
    Customer_id INT,
    Staff_id INT,
    Item_id INT,
    Staff_rating FLOAT,
    Item_rating FLOAT,
    Feedback_text TEXT,
    FOREIGN KEY (Customer_id) REFERENCES Customer(Customer_id),
    FOREIGN KEY (Staff_id) REFERENCES Staff(Staff_id),
    FOREIGN KEY (Item_id) REFERENCES Item(Item_id)
);

-- Inserting Sample Customers
INSERT INTO Customer (Name, Email, Phone) VALUES
('Alice Smith', 'alice@example.com', '1234567890'),
('Bob Johnson', 'bob@example.com', '0987654321');

-- Inserting Sample Tables
INSERT INTO Tables (Total_people, IsOccupied) VALUES
(4, FALSE),
(6, FALSE),
(2, FALSE);

-- Inserting Sample Reservations
INSERT INTO Reservation (Table_id, Customer_id, Time, Number_of_people) VALUES
(1, 1, '2024-11-15 18:30:00', 3),
(2, 2, '2024-11-16 20:00:00', 5);

-- Inserting Sample Orders
INSERT INTO Orders (CustomerID, TotalAmount, OrderTime, Status, Notes, StaffID, TableID) VALUES
(1, 45.50, '2024-11-15 19:00:00', 'Pending', '', 1, 1),
(2, 30.00, '2024-11-16 20:30:00', 'Pending', '', 2, 2);

-- Inserting Sample Items
INSERT INTO Item (Name, Price) VALUES
('Pizza', 10.00),
('Burger', 8.50),
('Pasta', 12.00);

-- Inserting Sample Order-Item Relationships in OrderDetails
INSERT INTO OrderDetails (OrderID, ItemID, Quantity, UnitPrice, TotalPrice) VALUES
(1, 1, 2, 10.00, 20.00),
(1, 2, 1, 8.50, 8.50),
(2, 3, 1, 12.00, 12.00);

-- Inserting Sample Staff
INSERT INTO Staff (Name, Email, Phone, Staff_type, Rating) VALUES
('John Doe', 'john@example.com', '1122334455', 'Chef', 4.5),
('Jane Smith', 'jane@example.com', '2233445566', 'Waiter', 4.0);

-- Inserting Sample Feedback
INSERT INTO Feedback (Customer_id, Staff_id, Item_id, Staff_rating, Item_rating, Feedback_text) VALUES
(1, 1, 1, 4.0, 5.0, 'Great service and delicious pizza!'),
(2, 2, 2, 3.5, 4.0, 'The burger was good, but service was slow.');
