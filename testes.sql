
CREATE TABLE IF NOT EXISTS passageiros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    empresa TEXT NOT NULL,
    email TEXT UNIQUE,
    data_cadastro TEXT DEFAULT (DATE('now'))
);

INSERT INTO TABLE passageiros (nome, empresa, email, data_cadastro) VALUES (
    Simão Pedro, IBM, simao@ibm.com
    André
    Tiago, filho de Zebedeu
    João
    Filipe
    Bartolomeu (Natanael)
    Mateus (Levi)
    Tomé
    Tiago, filho de Alfeu
    Tadeu (Judas, filho de Tiago)
    Simão, o Zelote
    Judas Iscariotes
)