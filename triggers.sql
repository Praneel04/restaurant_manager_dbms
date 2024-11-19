CREATE TRIGGER after_reservation_insert
AFTER INSERT ON Reservation
FOR EACH ROW
BEGIN
  UPDATE `Tables`
  SET IsOccupied = TRUE
  WHERE Table_id = NEW.Table_id;
END;

CREATE TRIGGER after_reservation_delete
AFTER DELETE ON Reservation
FOR EACH ROW
BEGIN
  UPDATE `Tables`
  SET IsOccupied = FALSE
  WHERE Table_id = OLD.Table_id;
END;

CREATE TRIGGER before_order_insert
BEFORE INSERT ON Orders
FOR EACH ROW
BEGIN
  IF NEW.Status IS NULL THEN
    SET NEW.Status = 'Pending';
  END IF;
  UPDATE `Tables`
  SET IsOccupied = TRUE
  WHERE Table_id = NEW.TableID;
END;
