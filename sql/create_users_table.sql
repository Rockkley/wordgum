CREATE TABLE IF NOT EXISTS users ( 
	id INTEGER  primary key AUTOINCREMENT,
	telegram_id INTEGER UNIQUE,
	username TEXT,
	first_name TEXT,
	second_name TEXT,
	'level' INTEGER,
	regdate DATE)
	
	