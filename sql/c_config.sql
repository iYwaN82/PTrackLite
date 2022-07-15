CREATE TABLE if not exists Config (
 id INTEGER PRIMARY KEY,
 farm_name TEXT NOT NULL,
 address TEXT NOT NULL,
 email TEXT NOT NULL UNIQUE,
 traktor_num INTEGER NOT NULL,
 operator_num INTEGER NOT NULL,
 groups_num INTEGER NOT NULL
);