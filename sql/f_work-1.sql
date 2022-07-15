INSERT INTO Work (id, Name, EPC, EPC_NUM, StartDT, EndDT)
SELECT NULL, Name, EPC, 1, StartDT ,EndDT
FROM Input_Data
INNER JOIN Groups ON EPC = Groups.EPC1;