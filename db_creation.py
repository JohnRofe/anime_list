import sqlite3

def create_type_tv_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS type_tv (
            id INTEGER PRIMARY KEY,
            type_name TEXT
        )
    ''')

def create_genre_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS genre (
            id INTEGER PRIMARY KEY,
            genre_name TEXT
        )
    ''')

def create_anime_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anime (
            id INTEGER PRIMARY KEY,
            title TEXT,
            title_2 TEXT,
            popularity INTEGER,
            last_episode_number INTEGER,
            normalized_rating REAL,
            type_tv_id INTEGER,
            genre_1_id INTEGER,
            genre_2_id INTEGER,
            genre_3_id INTEGER,
            FOREIGN KEY (type_tv_id) REFERENCES type_tv(id),
            FOREIGN KEY (genre_1_id) REFERENCES genre(id),
            FOREIGN KEY (genre_2_id) REFERENCES genre(id),
            FOREIGN KEY (genre_3_id) REFERENCES genre(id)
        )
    ''')

def main():
    with sqlite3.connect('anime_list.db') as conn:
        c = conn.cursor()
        create_type_tv_table(c)
        create_genre_table(c)
        create_anime_table(c)

if __name__ == "__main__":
    main()