import sqlite3

# The user will input an anime name 
anime_name = input("Enter an anime name: ")

conn = sqlite3.connect('anime_list.db')
c = conn.cursor()

# This will search for the anime name in the database
c.execute("SELECT * FROM anime WHERE title = ?", (anime_name,))
anime = c.fetchone()

if anime is None:
    print("No anime found with that name.")
else:
    # This will get the genre of the anime
    genre_id = anime[6]  # assuming genre_1_id is the 6th column

    # This will get the top 5 anime with the same genre
    c.execute('''
        SELECT anime.title 
        FROM anime 
        JOIN genre ON anime.genre_1_id = genre.id 
        WHERE genre.id = ? 
        ORDER BY anime.normalized_rating DESC 
        LIMIT 5
    ''', (genre_id,))
    recommendations = c.fetchall()

    # This will print the recommendations
    print("Recommendations: ")
    for rec in recommendations:
        print(rec[0])

conn.close()



