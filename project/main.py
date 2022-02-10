from DB.connection import DAO
import functions

def option_menu():
    """
    This function runs the CLI for the user, it shows the user the available options from this client
    and asks for an action to make on the database.
    """

    continue_menu = True
    while continue_menu:
        is_valid_option=False
        while not is_valid_option:
            #Printing the options
            print("\n====OPTION MENU====")
            print("1. List tables")
            print("2. Add new tables from file")
            print("3. See table")
            print("4. See artists starting with ___")
            print("5. See genres containing letter ___")
            print("6. See the most popular genres (among artists)")
            print("7. See artists for some genre")
            print("8. Quit")
            print("===================")

            #Asks for an action to make on the database
            option = int(input("Select one option: "))

            #Validation of the user's input 
            if option < 1 or option > 8:
                print("Incorrect option, please enter a valid option...\n")
            elif option == 8:
                continue_menu = False
                print("Bye!")
                break
            #If is correct it exectute the actions listed in "execute_option()"
            else:
                is_valid_option = True
                execute_option(option)

def execute_option(option):
    """
    This function executes the action the user wants to make on the database.
    """

    dao = DAO()

    #List tables
    if option == 1:
        try:
            tables = dao.list_tables()
            if len(tables)>0:
                functions.list_tables(tables)
            else:
                print("\nThere are no tables to list in the database.\n")
        except Exception as e:
            print("Error (Option 1): ", e)
    
    #Add table from file
    elif option == 2:
        try:
            filepath = input("Enter the path to the gzip file to inmport to the database: ")
            column_names, _, db_types, rows_values = functions.format_table(filepath)
            table_name = input("Please name the new table: ")
            
            create_table_query = functions.create_table_query(column_names, db_types, table_name)
            add_values_query = functions.insert_rows_query(column_names, table_name)

            dao.add_table_from_file(table_name, create_table_query, add_values_query, rows_values)

            print(f"Table '{table_name}' added succesfully!")
            execute_option(1)
        except Exception as e:
            print("Error (Option 2): ", e)
    
    #See table
    elif option == 3:
        try:
            valid_tables = dao.list_tables()
            valid_tables = [table[0] for table in valid_tables]
            is_valid_table=False
            while not is_valid_table:
                execute_option(1)
                table_name = input("Enter the name of the table you want to see: ")
                if table_name not in valid_tables:
                    print(f"Table '{table_name}' is not in the database, please enter a valid name...\n")
                else:
                    is_valid_table=True
                    table_columns, table_preview = dao.see_table(table_name)
                    functions.see_table(table_columns, table_preview)

        except Exception as e:
            print("Error (Option 3): ", e)
    
    #List artists starting with ...
    elif option == 4:
        try:
            valid_tables = dao.list_tables()
            valid_tables = [table[0] for table in valid_tables]
            table_exists=False
            while not table_exists:
                if 'artist' not in valid_tables:
                    print(f"Table 'artist' is not in the database, please comeback when the table is created...\n")
                    break
                else:
                    table_exists=True
                    starts_with = input("Enter the letter(s) you want to search (ex: the, V, Mr.): ")
                    table_columns, artists_preview = dao.get_artists_starting_with(starts_with)
                    functions.see_table(table_columns, artists_preview)

        except Exception as e:
            print("Error (Option 4): ", e)
    
    #List genres containing ...
    elif option == 5:
        try:
            valid_tables = dao.list_tables()
            valid_tables = [table[0] for table in valid_tables]
            table_exists=False
            while not table_exists:
                if 'genre' not in valid_tables:
                    print(f"Table 'genre' is not in the database, please comeback when the table is created...\n")
                    break
                else:
                    table_exists=True
                    contains = input("Enter the letter(s) you want to search (ex: punk, sur, &): ")
                    table_columns, genres_preview = dao.get_genres_conaining(contains)
                    functions.see_table(table_columns, genres_preview)
        except Exception as e:
            print("Error (Option 5): ", e)
    
    #List the most popular genres among artists
    elif option == 6:
        try:
            valid_tables = dao.list_tables()
            valid_tables = [table[0] for table in valid_tables]
            tables_exists=False
            while not tables_exists:
                if 'genre' not in valid_tables or 'genre_artist' not in valid_tables:
                    print(f"Tables 'genre' and 'genre_artist' are needed for this analysis, please comeback when both tables are created...\n")
                    break
                else:
                    tables_exists=True
                    table_columns, genres_preview = dao.most_popular_genres()
                    functions.see_table(table_columns, genres_preview)
        except Exception as e:
            print("Error (Option 6): ", e)
    
    #List random artists corresponding to a genre
    elif option == 7:
        try:
            valid_tables = dao.list_tables()
            valid_tables = [table[0] for table in valid_tables]
            tables_exists=False
            while not tables_exists:
                if 'artist' not in valid_tables or 'genre_artist' not in valid_tables:
                    print(f"Tables 'artist', 'genre' and 'genre_artist' are needed for this analysis, please comeback when the three tables are created...\n")
                    break
                else:
                    tables_exists=True
                    genre = input("Enter the genre (ex: punk, pop, rap, bachata): ")
                    table_columns, genres_preview = dao.artists_of_genre(genre)
                    functions.see_table(table_columns, genres_preview)
        except Exception as e:
            print("Error (Option 7): ", e)

option_menu()
