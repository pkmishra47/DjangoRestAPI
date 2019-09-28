DELIMITER $$

USE `testdb`$$

DROP PROCEDURE IF EXISTS `sp_set_balance`$$

CREATE DEFINER=`root`@`%` PROCEDURE `sp_set_balance`(
	p_contact_number VARCHAR(15),
	p_amount DECIMAL(12,2),
	p_TranType VARCHAR(1),
	OUT p_Msg TEXT
)
BEGIN
	DECLARE p_current_balance DECIMAL(12,2) DEFAULT 0;
	IF EXISTS(SELECT 1 FROM tblusers WHERE contact_number = p_contact_number)
	THEN
		START TRANSACTION;
			SELECT balance INTO p_current_balance FROM tblusers WHERE contact_number = p_contact_number FOR UPDATE;
			
			IF (p_TranType = 'A')
			THEN
				UPDATE tblusers SET balance = balance + p_amount WHERE contact_number = p_contact_number;
				
				INSERT INTO tbltransactions(tran_type,contact_number,amount,tran_date)
				VALUES(p_TranType,p_contact_number,p_amount,CURRENT_TIMESTAMP());
				SET p_Msg = "Transaction Successful.";
				
			ELSEIF p_TranType = 'D'
			THEN
				IF (p_current_balance - p_amount) < 0
				THEN
					SET p_Msg = "Your balance is low. Please enter other amount.";
				ELSE
					UPDATE tblusers SET balance = balance - p_amount WHERE contact_number = p_contact_number;
					
					INSERT INTO tbltransactions(tran_type,contact_number,amount,tran_date)
					VALUES(p_TranType,p_contact_number,p_amount,CURRENT_TIMESTAMP());					
					SET p_Msg = "Transaction Successful.";
				END IF;
			END IF;
		COMMIT;
	ELSE
		SET p_Msg = "User Details doesn't exist."; 
	END IF;
END$$

DELIMITER ;