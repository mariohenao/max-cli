import gzip

def list_tables(tables):
    """
    This function prints the list of tables.
    
    Parameters
    ----------
    tables: 
        List of tables in the database

    Returns
    -------
    None
    """

    print("\nLIST OF TABLES: ")
    counter = 1
    for table in tables:
        row = f'{counter}. {table[0]}'
        print(row)
        counter+=1

def format_table(filepath):
    """
    This function formats the data to ingest in the database. (Input has to be a gzip file).
    
    Parameters
    ----------
    filepath: str
        Path to where the gzip file is. Specific format of the data is needed

    Returns
    -------
    column_names: list
        List of column names
    primary_key: tuple
        Tuple of columns that constitutes the primary key
    db_types: list
        List of types for each colunm
    rows_values: list
        List of rows of the table
    """
    if filepath.endswith('.gz'):
        with gzip.open(filepath, "rb") as f:
            #Split the data line by line and extract the metadata of th table
            rows = f.read().split(b'\x02\n')
            column_names = [el.decode('utf-8').replace('#', '') for el in rows[0].split(b'\x01')]
            primary_key = tuple([el.decode('utf-8').replace('#primaryKey:', '') for el in rows[1].split(b'\x01')])
            db_types = [el.decode('utf-8').replace('#dbTypes:', '') for el in rows[2].split(b'\x01')]
            rows_values = []
            for row in rows:
                if not row.startswith(b'#') and len(row)>0:
                    rows_values.append(tuple([el.decode('utf-8') for el in row.split(b'\x01')]))
        return column_names, primary_key, db_types, rows_values
    else:
        print("Error: Input file is not a gzip file.")

def create_table_query(column_names, db_types, table):
    """
    This function returns the sql query for creating a table.
    
    Parameters
    ----------
    column_names: list
        List of column names
    db_types: list
        List of types for each colunm
    table: str
        Name for the table to create in the database

    Returns
    -------
    full_query: list
        Sql query for creating the table
    """

    n_columns = len(column_names)
    columns_query = f'({column_names[0]} {db_types[0]}, '
    for ii in range(1, n_columns):
        columns_query = columns_query + column_names[ii] + ' ' + db_types[ii] + ', '
    columns_query = columns_query[:-2]+')'

    full_query = f"CREATE TABLE {table} {columns_query}"

    return full_query

def insert_rows_query(column_names, table):
    """
    This function returns the sql query for inserting rows to a table.
    
    Parameters
    ----------
    column_names: list
        List of column names
    table: str
        Name for the table to create in the database

    Returns
    -------
    full_query: list
        Sql query for inserting rows to the table
    """

    columns_query = "("
    for col in column_names:
        columns_query = columns_query + col + ", "
    columns_query = columns_query[:-2]+')'

    full_query = f"INSERT IGNORE INTO {table} " + columns_query + " VALUES (" + "%s, "*(len(column_names)-1) + "%s)"
    
    return full_query

def see_table(table_columns, table_preview):
    """
    This function prints a table.
    
    Parameters
    ----------
    table_columns: list
        List of column names
    table_preview: list
        Rows of the table to show

    Returns
    -------
    None
    """

    column_names = [str(el[0]) for el in table_columns]
    format_str = "|" + " {:^16} |"*len(column_names)
    print(format_str.format(*column_names))
    print("-"*len(format_str.format(*column_names)))
    for row in table_preview:
        print(format_str.format(*row))
