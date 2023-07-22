This code includes several query functions, and 2 functions to create tables and insert data into a mysql database.


Instructions to run the program (main): 
- You can configure the pymsql.connect information at the top of main. Make sure to have the correct information 
configured for your mysql account before running the program.

- You can also change the file name to the desired file (the variable, fileName), however it is recommeneded to use  the file that the program starts with.

- After running the program for the first time (to setup and populate the database), 
comment out the DROP DATABASE IF EXISTS line and the cur.execute line following it. (lines 300 and 301)
comment out the createTables and insertData function calls if you don't want to wait for the population every run. (lines 313 and 314)

- Then, you can uncomment the query function calls 1 at a time to see the results of said queries.

- To run this program via a terminal, type: python a5.py




What the Functions do:

createTables:
- This function creates the tables in the mysql database. It checks to see if a table of the same name currently exists, then drops it and makes a new one.

insertData:
- This functions inserts data from the csv file into the tables made by createTables.

query1:
- Finds the average budget of all movies

query2:
- Finds movies produced in the United States

query3: 
- Finds the top 5 movies that made the most revenue

query4:
- Finds what movies have both the genre Science Fiction and Mystery

query5:
- Finds movies that have a popularity > average popularity