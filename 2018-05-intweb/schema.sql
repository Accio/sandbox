DROP TABLE IF EXISTS todoTbl;

CREATE TABLE todoTbl (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	date DATETIME,
	name TEXT,
	deadline DATETIME
);
