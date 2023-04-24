import csv
import heapq
import itertools
import math
import textwrap
from difflib import SequenceMatcher

def load_movies_db(filename):
    movies_db = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movies_db.append(row)
    return movies_db

def get_similar_movies(movie_name, movies_db):
    # Search algorithm 1: Exact match
    #exact_match = [movie for movie in movies_db if movie["title"] == movie_name]
    
    # Search algorithm 2: Partial match
    state_space = [movie for movie in movies_db if movie_name.lower() in movie["title"].lower()]
    
    # Search algorithm 3: Levenshtein distance
    generate_and_test = heapq.nsmallest(6, movies_db, key=lambda movie: SequenceMatcher(None, movie["title"].lower(), movie_name.lower()).ratio())
    
    # Search algorithm 4: Jaccard similarity
    def hill_climbing(movie1, movie2):
        words1 = set(movie1["title"].lower().split())
        words2 = set(movie2["title"].lower().split())
        intersection = words1 & words2
        union = words1 | words2
        if len(union) == 0:
            return 0
        else:
            return len(intersection) / len(union)
    
    hill_climbing = heapq.nlargest(6, movies_db, key=lambda movie: hill_climbing(movie, {"title": movie_name}))
    
    # Search algorithm 5: Cosine similarity
    def best_first(movie1, movie2):
        common_words = set(movie1["title"].lower().split()) & set(movie2["title"].lower().split())
        freq1 = [movie1["title"].lower().count(word) for word in common_words]
        freq2 = [movie2["title"].lower().count(word) for word in common_words]
        dot_product = sum(f1 * f2 for f1, f2 in zip(freq1, freq2))
        magnitude1 = math.sqrt(sum(f ** 2 for f in freq1))
        magnitude2 = math.sqrt(sum(f ** 2 for f in freq2))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        else:
            return dot_product / (magnitude1 * magnitude2)
    
    best_first = heapq.nlargest(6, movies_db, key=lambda movie: best_first(movie, {"title": movie_name}))
    
    def problem_reduction(movie1, movie2):
        words1 = set(movie1["title"].lower().split())
        words2 = set(movie2["title"].lower().split())
        return len(words1 & words2)
    
    problem_reduction = heapq.nlargest(10, movies_db, key=lambda movie: problem_reduction(movie, {"title": movie_name}))

    # Combine results from all search algorithms
    #results = list(itertools.chain(state_space))
    #results = list(itertools.chain(generate_and_test))
    #results = list(itertools.chain(hill_climbing))
    results = list(itertools.chain(best_first))
    #results = list(itertools.chain(problem_reduction))
    # Remove duplicates
    #results = [dict(t) for t in {tuple(d.items()) for d in results}]
    
    return results

# Load movie database from CSV file
movies_db = load_movies_db('tmdb_5000_movies.csv')

movie= input('Enter Movie Name  ')

# Find similar movies
similar_movies = get_similar_movies(movie, movies_db)

wrapper = textwrap.TextWrapper(width=140)
# Print results
for movie in similar_movies:
    print("\n")
    
    print("Recommended Movie:", movie['title'],"\nRating: ", movie['vote_average'])
    
    
    word_list = wrapper.wrap(text = movie['overview'])
    for element in word_list:
      print(element)
    
