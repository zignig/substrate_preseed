PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE machines (name TEXT,mac TEXT PRIMARY KEY,type TEXT,distribution TEXT,status INT,stamp NUMBER);
COMMIT;
