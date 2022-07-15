INSERT INTO Work
SELECT NULL, Name, EPC, 3, StartDT ,EndDT  
FROM Input_Data 
INNER JOIN Groups ON EPC = Groups.EPC3;