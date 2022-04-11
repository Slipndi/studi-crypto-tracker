DROP TABLE IF EXISTS crypto_value;
DROP TABLE IF EXISTS evolution_gain;

CREATE TABLE crypto_value (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crypto_id INTEGER NOT NULL, 
    name TEXT NOT NULL,
    price FLOAT NOT NULL,
    quantity INT NOT NULL,
    date DATETIME NOT NULL
);

CREATE TABLE evolution_gain (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value FLOAT NOT NULL,
    date DATETIME NOT NULL
);

/** a mettre dans gitignore **/