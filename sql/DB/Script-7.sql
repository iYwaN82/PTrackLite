INSERT INTO Work (Group_id , Name, EPC, EPC_NUM, StartDT, EndDT)
    SELECT Groups.id , Groups.Name, Input_Data.EPC, 1, Input_Data.StartDT ,Input_Data.EndDT
    FROM Input_Data
    INNER JOIN Groups ON EPC = Groups.EPC1;

INSERT INTO Work (Group_id , Name, EPC, EPC_NUM, StartDT, EndDT)
    SELECT Groups.id , Groups.Name, Input_Data.EPC, 2, Input_Data.StartDT ,Input_Data.EndDT
    FROM Input_Data
    INNER JOIN Groups ON EPC = Groups.EPC2;

INSERT INTO Work (Group_id , Name, EPC, EPC_NUM, StartDT, EndDT)
    SELECT Groups.id , Groups.Name, Input_Data.EPC, 3, Input_Data.StartDT ,Input_Data.EndDT
    FROM Input_Data
    INNER JOIN Groups ON EPC = Groups.EPC3;