DELIMITER $$

USE `testdb`$$

DROP PROCEDURE IF EXISTS `sp_get_transaction_details`$$

CREATE DEFINER=`root`@`%` PROCEDURE `sp_get_transaction_details`(
	p_contact_number VARCHAR(15),
	p_offset INT,
	p_total_count INT,
	OUT p_Msg TEXT
)
BEGIN
	IF EXISTS(SELECT 1 FROM tblusers WHERE contact_number = p_contact_number)
	THEN
		SELECT DATE_FORMAT(tt.tran_date,'%Y-%M-%d %H:%i:%S') 'Transaction Date',
			amount 'Amount', 
			CASE 	WHEN tran_type = 'A' THEN 'Credit'
				WHEN tran_type = 'D' THEN 'Debit'
			END 'Transaction Type'
		FROM tblusers tu 
		INNER JOIN tbltransactions tt ON tt.contact_number = tu.contact_number
		WHERE tu.contact_number = p_contact_number
		ORDER BY tran_date DESC
		LIMIT p_offset,p_total_count;
	ELSE
		SET p_Msg = "User Details doesn't exist."; 
	END IF;
END$$

DELIMITER ;