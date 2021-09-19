
-- Activities 
SELECT distinct target_user_id FROM `activities` ORDER BY target_user_id DESC;

SELECT distinct target_user_name FROM `activities` ORDER BY target_user_name DESC;


-- Links
SELECT acc_id_1,acc_id_2,acc_code_2,COUNT(acc_id_1) 

FROM account_links acl1

group by acc_id_2;