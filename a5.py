import pymysql
import csv


# Finds the average budget of all movies
def query1(cur):
    sql = "SELECT AVG(budget) FROM movie"
    cur.execute(sql)
    result = cur.fetchone()
    print(result[0])


# Finds movies produced in the United States
def query2(cur):
    sql = """SELECT m.title, pc.name
            FROM movie m
            JOIN movie_production_company mpc ON m.id = mpc.movie_id
            JOIN production_company pc ON mpc.production_company_id = pc.id
            JOIN movie_production_country mpcn ON m.id = mpcn.movie_id
            JOIN production_country pcn ON mpcn.production_country_id = pcn.iso_3166_1
            WHERE pcn.name = 'United States of America'
          """
    
    cur.execute(sql)
    results = cur.fetchall()
    for row in results:
        print(row[0] + ", " + row[1])

# Finds the top 5 movies that made the most revenue
def query3(cur):
    sql = """SELECT title, revenue
            FROM movie
            ORDER BY revenue DESC
            LIMIT 5
           """
    
    cur.execute(sql)
    results = cur.fetchall()
    for result in results:
        print(f"{result[0]}, {result[1]}")



# Finds what movies have both the genre Science Fiction and Mystery
def query4(cur):
    sql = """SELECT m.title, GROUP_CONCAT(DISTINCT g.name) AS genres
            FROM movie AS m
            INNER JOIN movie_genre AS mg ON m.id = mg.movie_id
            INNER JOIN genre AS g ON mg.genre_id = g.id
            WHERE g.name IN ('Science Fiction', 'Mystery')
            GROUP BY m.title
            HAVING COUNT(DISTINCT g.name) = 2
            """
    
    cur.execute(sql)
    results = cur.fetchall()
    for row in results:
        print(row[0] + ",", row[1])



# Finds movies that have a popularity > average popularity
def query5(cur):
    sql = """SELECT title, popularity
            FROM movie
            WHERE popularity > (SELECT AVG(popularity) FROM movie)
            ORDER BY popularity DESC
            """
    
    cur.execute(sql)
    results = cur.fetchall()
    for row in results:
        print(row[0] + ",", row[1])




def insertData(conn, cur, filename):
    # Open the CSV file
    with open(filename, newline='', encoding='utf-8') as csvfile:

        # Read the CSV file into a dictionary
        reader = csv.DictReader(csvfile)

        # Iterate over each row in the CSV file
        for row in reader:
            # Replace empty strings with NULL
            for key, value in row.items():
                if value == '':
                    row[key] = None

            # Insert data into the movies table
            movie_data = (
                row['budget'], row['homepage'], row['id'],
                row['original_language'], row['original_title'], row['overview'],
                row['popularity'], row['release_date'], row['revenue'],
                row['runtime'], row['status'], row['tagline'],
                row['title'], row['vote_average'], row['vote_count']
            )
            cur.execute("""INSERT INTO movie (budget, homepage, id, original_language, 
                                              original_title, overview, popularity, 
                                              release_date, revenue, runtime, 
                                              status, tagline, title, vote_average, vote_count) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", movie_data)

            # Insert data into the "genre" and "movie_genre" tables
            genre_data = eval(row['genres'])
            for item in genre_data:
                cur.execute("INSERT IGNORE INTO genre (id, name) VALUES (%s, %s)", (item['id'], item['name']))

                # row['id'] is the movie id         
                # item['id'] is the genre id
                cur.execute("INSERT INTO movie_genre (movie_id, genre_id) VALUES (%s, %s)", (row['id'], item['id']))

            # Insert data into the "keyword" and "movie_keyword" tables
            keyword_data = eval(row['keywords'])
            for item in keyword_data:
                cur.execute("INSERT IGNORE INTO keyword (id, name) VALUES (%s, %s)", (item['id'], item['name']))

                # row['id'] is the movie id         
                # item['id'] is the keyword id
                cur.execute("INSERT INTO movie_keyword (movie_id, keyword_id) VALUES (%s, %s)", (row['id'], item['id']))

            # Insert data into the "production_company" and "movie_production_company" tables
            company_data = eval(row['production_companies'])
            for item in company_data:
                cur.execute("INSERT IGNORE INTO production_company (id, name) VALUES (%s, %s)", (item['id'], item['name']))

                # row['id'] is the movie id         
                # item['id'] is the company id
                cur.execute("INSERT INTO movie_production_company (movie_id, production_company_id) VALUES (%s, %s)", (row['id'], item['id']))
                
            # Insert data into the "production_country" and "movie_production_country" tables
            country_data = eval(row['production_countries'])
            for item in country_data:
                cur.execute("INSERT IGNORE INTO production_country (iso_3166_1, name) VALUES (%s, %s)", (item['iso_3166_1'], item['name']))

                # row['id'] is the movie id         
                # item['id'] is the country id
                cur.execute("INSERT INTO movie_production_country (movie_id, production_country_id) VALUES (%s, %s)", (row['id'], item['iso_3166_1']))

            # Insert data into the "spoken_language" and "movie_spoken_language" tables
            language_data = eval(row['spoken_languages'])
            for item in language_data:
                cur.execute("INSERT IGNORE INTO spoken_language (iso_639_1, name) VALUES (%s, %s)", (item['iso_639_1'], item['name']))

                # row['id'] is the movie id         
                # item['id'] is the language id
                cur.execute("INSERT INTO movie_spoken_language (movie_id, spoken_language_id) VALUES (%s, %s)", (row['id'], item['iso_639_1']))

        # Save changes
        conn.commit()


# This function drops the corresponding tables in the mysql database before creating them
def createTables(conn, cur):
    
    # Table: movie
    sqlDrop = "DROP TABLE IF EXISTS movie"
    cur.execute(sqlDrop)
    sqlCreate = """CREATE TABLE IF NOT EXISTS movie (
                    budget INT,
                    homepage VARCHAR(255),
                    id INT PRIMARY KEY,
                    original_language CHAR(2),
                    original_title VARCHAR(255),
                    overview TEXT,
                    popularity FLOAT,
                    release_date DATE,
                    revenue BIGINT,
                    runtime BIGINT,
                    status VARCHAR(255),
                    tagline TEXT,
                    title VARCHAR(255),
                    vote_average FLOAT,
                    vote_count INT)
                """
    cur.execute(sqlCreate)

    # Table: genre 
    sqlDrop = "DROP TABLE IF EXISTS genre"
    cur.execute(sqlDrop)
    sqlCreate = """CREATE TABLE IF NOT EXISTS genre (
                    id INT PRIMARY KEY,
                    name VARCHAR(255))
                """
    cur.execute(sqlCreate)


    # Table: movie_genre 
    sqlDrop = "DROP TABLE IF EXISTS movie_genre"
    cur.execute(sqlDrop)
    sqlCreate = """CREATE TABLE IF NOT EXISTS movie_genre (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    movie_id INT,
                    genre_id INT,
                    FOREIGN KEY (movie_id) REFERENCES movie (id),
                    FOREIGN KEY (genre_id) REFERENCES genre (id))
                """
    cur.execute(sqlCreate)

    # Table: keyword
    sqlDrop = "DROP TABLE IF EXISTS keyword"
    cur.execute(sqlDrop)
    sqlCreate = """CREATE TABLE IF NOT EXISTS keyword (
                    id INT PRIMARY KEY,
                    name VARCHAR(255))
                """
    cur.execute(sqlCreate)

    # Table: movie_keyword
    sqlDrop = "DROP TABLE IF EXISTS movie_keyword"
    cur.execute(sqlDrop)
    sqlCreate = """CREATE TABLE IF NOT EXISTS movie_keyword (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    movie_id INT,
                    keyword_id INT,
                    FOREIGN KEY (movie_id) REFERENCES movie (id),
                    FOREIGN KEY (keyword_id) REFERENCES keyword (id))
                """
    cur.execute(sqlCreate)

    # Table: production_company
    sqlDrop = "DROP TABLE IF EXISTS production_company"
    cur.execute(sqlDrop)
    sqlCreate = """CREATE TABLE IF NOT EXISTS production_company (
                    id INT PRIMARY KEY,
                    name VARCHAR(255))
                """
    cur.execute(sqlCreate)

    # Table: movie_production_company
    sqlDrop = "DROP TABLE IF EXISTS movie_production_company"
    cur.execute(sqlDrop)
    sqlCreate = """CREATE TABLE IF NOT EXISTS movie_production_company (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    movie_id INT,
                    production_company_id INT,
                    FOREIGN KEY (movie_id) REFERENCES movie (id),
                    FOREIGN KEY (production_company_id) REFERENCES production_company (id))
                """
    cur.execute(sqlCreate)

    # Table: production_country 
    sqlDrop = "DROP TABLE IF EXISTS production_country"
    cur.execute(sqlDrop)
    sqlCreate = """CREATE TABLE IF NOT EXISTS production_country (
                    iso_3166_1 VARCHAR(2) PRIMARY KEY,
                    name VARCHAR(255))
                """
    cur.execute(sqlCreate)

    # Table: movie_production_country 
    sqlDrop = "DROP TABLE IF EXISTS movie_production_country"
    cur.execute(sqlDrop)
    sqlCreate = """CREATE TABLE IF NOT EXISTS movie_production_country (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    movie_id INT,
                    production_country_id VARCHAR(2),
                    FOREIGN KEY (movie_id) REFERENCES movie (id),
                    FOREIGN KEY (production_country_id) REFERENCES production_country (iso_3166_1))
                """
    cur.execute(sqlCreate)

    # Table: spoken_language 
    sqlDrop = "DROP TABLE IF EXISTS spoken_language"
    cur.execute(sqlDrop)
    sqlCreate = """CREATE TABLE IF NOT EXISTS spoken_language (
                    iso_639_1 VARCHAR(2) PRIMARY KEY,
                    name VARCHAR(255))
                """
    cur.execute(sqlCreate)

   # Table: movie_spoken_language
    sqlDrop = "DROP TABLE IF EXISTS movie_spoken_language"
    cur.execute(sqlDrop)
    sqlCreate = """CREATE TABLE IF NOT EXISTS movie_spoken_language (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    movie_id INT,
                    spoken_language_id VARCHAR(2),
                    FOREIGN KEY (movie_id) REFERENCES movie (id),
                    FOREIGN KEY (spoken_language_id) REFERENCES spoken_language (iso_639_1))
                """
    cur.execute(sqlCreate)

    # Save changes
    conn.commit()


def main():
    # Configure mysql info here
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234')
    cur = conn.cursor()
    
    # The file used for this program
    fileName = "tmdb_5000_movies.csv"

    # Check if the database exists
    # Comment these 2 commands out after running the program the first time
    sql = "DROP DATABASE IF EXISTS tmdb_movies"
    cur.execute(sql)

    # If not, then create it
    sql = "CREATE DATABASE IF NOT EXISTS tmdb_movies"
    cur.execute(sql)

    # In the following function calls, we'll be using the database we just made
    sql = "USE tmdb_movies"
    cur.execute(sql)


    # Comment these 2 function calls out after running the program the first time
    createTables(conn, cur)
    insertData(conn, cur, fileName)

    # Uncomment these query function calls to run them
    #query1(cur) # Finds the average budget of all movies
    #query2(cur) # Finds movies produced in the United States
    #query3(cur) # Finds the top 5 movies that made the most revenue
    #query4(cur) # Finds what movies have both the genre Science Fiction and Mystery
    #query5(cur) # Finds movies that have a popularity > average popularity


    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
