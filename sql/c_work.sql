CREATE TABLE Work (
 id INTEGER PRIMARY KEY,
 Group_id INTEGER NOT NULL,
 Name TEXT NOT NULL,
 EPC TEXT NOT NULL,
 EPC_Num INTEGER NOT NULL,
 StartDT NUMERIC NOT NULL,
 EndDT NUMERIC NOT NULL
);