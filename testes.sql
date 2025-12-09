
CREATE TABLE IF NOT EXISTS passageiros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    empresa TEXT NOT NULL,
    email TEXT UNIQUE,
    data_cadastro TEXT DEFAULT (DATE('now'))
);

def insert_seed_data():
    """Insere alguns registros de exemplo (só se quiser popular)."""
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.cursor()
        # Para evitar erro de UNIQUE, só insere se a tabela estiver vazia
        cur.execute("SELECT COUNT(*) FROM passageiros;")
        count = cur.fetchone()[0]
        if count == 0:
            cur.executescript("""
                INSERT INTO passageiros (nome, empresa, email, data_cadastro) VALUES
                    ('Simão Pedro', 'IBM', 'simao@ibm.com', '2025-12-09'),
                    ('André', 'IBM', 'andre@ibm.com', '2025-12-09'),
                    ('Tiago, filho de Zebedeu', 'IBM', 'tiago.zebedeu@ibm.com', '2025-12-09'),
                    ('João', 'IBM', 'joao@ibm.com', '2025-12-09'),
                    ('Filipe', 'IBM', 'filipe@ibm.com', '2025-12-09'),
                    ('Bartolomeu (Natanael)', 'IBM', 'bartolomeu@ibm.com', '2025-12-09'),
                    ('Mateus (Levi)', 'IBM', 'mateus@ibm.com', '2025-12-09'),
                    ('Tomé', 'IBM', 'tome@ibm.com', '2025-12-09'),
                    ('Tiago, filho de Alfeu', 'IBM', 'tiago.alfeu@ibm.com', '2025-12-09'),
                    ('Tadeu (Judas, filho de Tiago)', 'IBM', 'tadeu@ibm.com', '2025-12-09'),
                    ('Simão, o Zelote', 'IBM', 'simao.zelote@ibm.com', '2025-12-09'),
                    ('Judas Iscariotes', 'IBM', 'judas@ibm.com', '2025-12-09');
            """)
            con.commit()
    finally:
        con.close()