import mysql.connector
from mysql.connector import Error

class DAO():

    def __init__(self):
        """
        This method connects with the database.
        """
        
        try:
            self.connection = mysql.connector.connect(
                host='max-mysql',
                port='3306',
                user='root',
                password='password',
                database='max-db' 
            )
        except Error as e:
            print(f'Connection Error: {e}')

    def list_tables(self):
        """
        This method exectutes the sql query to list the tables in the database.

        Parameters
        ----------

        Returns
        -------
        tables: list
            The list of tables in the database
        """

        #Check if it is connected to the database
        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                return tables
            except Error as e:
                print(f'Error: {e}')
        else:
            print("Not connected to the database.")

    def add_table_from_file(self, table_name, create_table_query, add_values_query, rows_values):
        """
        This method exectutes the sql queries create a table.

        Parameters
        ----------
        table_name: str
            Name for the table
        create_table_query: str
            Sql query to create the table
        add_values_query:
            Sql query to add the values
        rows_values: list
            List of tuples with the values for the table

        Returns
        -------
        None
        """

        #Check if it is connected to the database
        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                #Deletes table if already exists and then creates it
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                cursor.execute(create_table_query)
                
                #Add the values for the table just created
                cursor.executemany(add_values_query, rows_values)
                self.connection.commit()
            except Error as e:
                print(f'Error: {e}')
        else:
            print("Not connected to the database.")

    def see_table(self, table_name):
        """
        This method exectutes the sql queries get a preview of the table to show.

        Parameters
        ----------
        table_name: str
            Name for the table

        Returns
        -------
        table_columns: list
            List of column names
        table_preview: list
            List of tuples with the values of the table
        """

        #Check if it is connected to the database
        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                #Get the column names
                cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                table_columns = cursor.fetchall()

                #Get the 10 first rows of the table
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")
                table_preview = cursor.fetchall()
                return table_columns, table_preview
            except Error as e:
                print(f'Error: {e}')
        else:
            print("Not connected to the database.")

    def get_artists_starting_with(self, starts_with):
        """
        This method exectutes the sql query that searches in the database for artists starting 
        with 'starts_with' parameter.

        Parameters
        ----------
        starts_with: str
            Letter(s) to search artitsts starting with

        Returns
        -------
        table_columns: list
            List of column names
        artists_preview: list
            List of tuples with the values of the table
        """

        #Check if it is connected to the database
        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                #Get the column names
                cursor.execute(f"SHOW COLUMNS FROM artist")
                table_columns = cursor.fetchall()

                #Get the 10 first rows of the table
                cursor = self.connection.cursor()
                cursor.execute(f"SELECT * FROM artist WHERE name LIKE '{starts_with}%' LIMIT 30")
                artists_preview = cursor.fetchall()

                return table_columns, artists_preview
            except Error as e:
                print(f'Error: {e}')
        else:
            print("Not connected to the database.")

    def get_genres_conaining(self, contains):
        #Check if it is connected to the database
        """
        This method exectutes the sql query that searches in the database for genres containing 
        the 'contains' parameter.

        Parameters
        ----------
        contains: str
            Letter(s) to search artitsts containing

        Returns
        -------
        table_columns: list
            List of column names
        genres_preview: list
            List of tuples with the values of the table
        """

        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                #Get the column names
                cursor.execute(f"SHOW COLUMNS FROM genre")
                table_columns = cursor.fetchall()

                #Get the 10 first rows of the table
                cursor = self.connection.cursor()
                cursor.execute(f"SELECT * FROM genre WHERE name LIKE '%{contains}%' LIMIT 30")
                genres_preview = cursor.fetchall()

                return table_columns, genres_preview
            except Error as e:
                print(f'Error: {e}')
        else:
            print("Not connected to the database.")

    def most_popular_genres(self):
        """
        This method exectutes the sql query that searches in the database for most
        popular genres among the artists.

        Parameters
        ----------

        Returns
        -------
        table_columns: list
            List of column names
        genres_preview: list
            List of tuples with the values of the table
        """

        #Check if it is connected to the database
        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                query = """
                SELECT genre_id, name, COUNT(*) 
                FROM genre_artist 
                    INNER JOIN genre
                    USING (genre_id)
                WHERE is_primary=1 
                GROUP BY genre_id, name
                ORDER BY COUNT(*) DESC
                LIMIT 10
                """
                #Column names
                table_columns = [['genre_id'], ['name'], ['number of artists']]
                
                #Get the 10 first rows of the table
                cursor.execute(query)
                genres_preview = cursor.fetchall()

                return table_columns, genres_preview
            except Error as e:
                print(f'Error: {e}')
        else:
            print("Not connected to the database.")

    def artists_of_genre(self, genre):
        """
        This method exectutes the sql query that searches in the database for 10 random
        artists corresponding to an specific genre.

        Parameters
        ----------
        genre: str
            Genre to look for artists

        Returns
        -------
        table_columns: list
            List of column names
        artists_preview: list
            List of tuples with the values of the table
        """

        #Check if it is connected to the database
        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                query = f"""
                SELECT artist_id, genre, name AS artist 
                FROM 
                    (SELECT genre_id, artist_id, name AS genre
                    FROM genre_artist 
                        INNER JOIN genre
                        USING (genre_id)
                    WHERE LOWER(name)=LOWER('{genre}')
                    ) genres
                        INNER JOIN artist
                        USING (artist_id)
                ORDER BY RAND()
                LIMIT 10;
                """
                #Column names
                table_columns = [['genre_id'], ['genre'], ['artist']]
                
                #Get the 10 first rows of the table
                cursor.execute(query)
                artists_preview = cursor.fetchall()

                return table_columns, artists_preview
            except Error as e:
                print(f'Error: {e}')
        else:
            print("Not connected to the database.")
        