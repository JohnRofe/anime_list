'''This code allows to recommend an anime based on input about a
 liked anime and it shows the best ranked anime in the same category from the db
 
 1. Asks the user for the name of an anime
 2. Matches the input with the anime in the db using fuzzywuzzy and confirms the match with the user
 3. If the match is confirmed, it recommends the best ranked anime in the same category
 4. If the match is not confirmed, it asks the user to try again
 
 '''
# Importing the necessary libraries

import sqlite3
from fuzzywuzzy import fuzz
import pandas as pd
import sys

def get_anime_name():
    anime_name = input('Enter the name of an anime you liked: ')
    return anime_name

def tokenizer(anime_name):
    anime_tokenized = []
    for word in anime_name.split():
        word = word.lower()
        if word in ['the', 'of', 'and', 'in', 'a', 'an']:
            continue
        # check for latinized japanese words
        elif word in ['no', 'na', 'ni', 'de', 'to', 'wa', 'ka', 'ga', 'wo', 'he', 'mo', 'ya', 'yo', 'ne']:
            continue
        else:
            anime_tokenized.append(word)
    return anime_tokenized
    
def match_anime(anime_name):

    conn = sqlite3.connect('anime_list.db')
    cursor = conn.cursor()

    cursor.execute('SELECT title, title_2 FROM anime')
    data = cursor.fetchall()

    anime_name = tokenizer(anime_name)
    matches = []
    for anime in data:
        title = tokenizer(anime[0])
        title_2 = tokenizer(anime[1])
        match = fuzz.token_set_ratio(anime_name, title) + fuzz.token_set_ratio(anime_name, title_2)
        matches.append((anime[0], match))
    matches.sort(key=lambda x: x[1], reverse=True)
    conn.close()

    return matches

def confirm_match(matches):
    print('Did you mean:')
    for i, match in enumerate(matches[:5]):
        print(f'{i+1}. {match[0]}')
    choice = input('Enter the number of the anime you meant or 0 to try again: ')
    if choice == '0':
        return False
    else:
        return matches[int(choice)-1][0]
    
def get_recommendation(anime_name):
    conn = sqlite3.connect('anime_list.db')  
    cursor = conn.cursor()

    cursor.execute('''
        SELECT genre_1_id, genre_2_id, genre_3_id 
        FROM anime 
        WHERE title = ?
    ''', (anime_name,))

    genre_ids = cursor.fetchone()  

    cursor.execute('''
        SELECT title, normalized_rating,
        CASE 
            WHEN genre_1_id = ? AND genre_2_id = ? AND genre_3_id = ? THEN 3
            WHEN genre_2_id = ? AND genre_3_id = ? THEN 2
            WHEN genre_1_id = ? AND genre_3_id = ? THEN 2
            WHEN genre_1_id = ? AND genre_2_id = ? THEN 2
            WHEN genre_3_id = ? THEN 1
            WHEN genre_2_id = ? THEN 1
            WHEN genre_1_id = ? THEN 1
            ELSE 0
        END as match_score
    FROM anime
    ORDER BY match_score DESC, normalized_rating DESC 
    LIMIT 5
''', genre_ids * 4)

    recommendations = cursor.fetchall()

    conn.close()

    return recommendations

def main():
    while True:
        anime_name = get_anime_name()
        matches = match_anime(anime_name)
        anime_name = confirm_match(matches)
        if anime_name:
            recommendations = get_recommendation(anime_name)
            print(f'Here are some anime similar to {anime_name}:')
            for anime in recommendations:
                print(f'{anime[0]}: {anime[1]}')
            break

if __name__ == "__main__":
    main()










