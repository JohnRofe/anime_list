import pandas as pd
import sqlite3

conn = sqlite3.connect('anime_list.db')

def insert_into_tables(cursor, df):
    cursor.executemany('INSERT INTO type_tv (type_name) VALUES (?)', [(i,) for i in df['type_tv'].unique()])
    cursor.execute("INSERT INTO genre (genre_name) SELECT 'Unknown' WHERE NOT EXISTS(SELECT 1 FROM genre WHERE genre_name = 'Unknown')")
    cursor.executemany('INSERT INTO genre (genre_name) VALUES (?)', [(i,) for i in pd.concat([df['genre_1'], df['genre_2'], df['genre_3']]).unique()])

def get_ids(cursor):
    type_tv_ids = pd.read_sql_query('SELECT * FROM type_tv', conn).set_index('type_name')['id'].to_dict()
    genre_ids = pd.read_sql_query('SELECT * FROM genre', conn).set_index('genre_name')['id'].to_dict()
    return type_tv_ids, genre_ids

def replace_values_with_ids(df, type_tv_ids, genre_ids):
    df['type_tv_id'] = df['type_tv'].map(type_tv_ids)
    df['genre_1_id'] = df['genre_1'].map(genre_ids)
    df['genre_2_id'] = df['genre_2'].map(genre_ids).fillna(genre_ids['Unknown'])
    df['genre_3_id'] = df['genre_3'].map(genre_ids).fillna(genre_ids['Unknown'])
    return df

def insert_into_anime_table(cursor, df):
    for i, row in df.iterrows():
        cursor.execute('''
            INSERT INTO anime (title, title_2, popularity, last_episode_number, normalized_rating, type_tv_id, genre_1_id, genre_2_id, genre_3_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['title'], row['title_2'], row['popularity'], row['last_episode_number'], row['normalized_rating'], row['type_tv_id'], row['genre_1_id'], row['genre_2_id'], row['genre_3_id']))
        if i % 500 == 0:
            print(f'Inserted {i} rows')

def main():
    df = pd.read_csv('anime_data_cleaned.csv')
    with sqlite3.connect('anime_list.db') as conn:
        c = conn.cursor()
        try:
            insert_into_tables(c, df)
            type_tv_ids, genre_ids = get_ids(c)
            df = replace_values_with_ids(df, type_tv_ids, genre_ids)
            insert_into_anime_table(c, df)
            conn.commit()
            print('Data insertion completed successfully')
        except Exception as e:
            print('An error occurred:', e)

if __name__ == "__main__":
    main()