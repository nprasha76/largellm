import sqlite3

def create_sqlite_database(db_name="tview.db"):
    """Creates an SQLite database and a 'txn' table.

    Args:
        db_name (str, optional): The name of the database file. Defaults to "transactions.db".

    Returns:
        sqlite3.Connection: The connection object to the database.  Returns None on error.
    """
    try:
        print('creating')
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Create the 'txn' table if it doesn't exist.  Using parameterized queries
        # to prevent SQL injection vulnerabilities.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS txn (
                i_entity INTEGER,
                i_teller TEXT,
                n_cash_box INTEGER,
                d_business DATE,
                c_txn_type INTEGER,
                n_branch_au TEXT,
                a_start_cash INTEGER,
                a_end_cash INTEGER
            )
        """)
        conn.commit()
        # Create the 'cash_advance' table if it doesn't exist.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cash_advance (
                i_entity INTEGER,
                i_teller TEXT,
                f_amt_confirm INTEGER,
                d_business DATE,
                c_txn_type INTEGER,
                n_branch_au TEXT,
                c_term_id INTEGER,
                c_pinpad_status TEXT
            )
        """)

       



        conn.commit()  # Important to save the table creation
        print('created')
        print(f"Database '{db_name}' and tables  created successfully.")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
            target_type TEXT CHECK (target_type IN ('table', 'column')),
            target_name TEXT,
            metadata_key TEXT,
            metadata_value TEXT,
            PRIMARY KEY (target_type, target_name, metadata_key)
            )
        """)
        conn.commit() 
        #Add metadata for the 'txn' table columns
        sql_script ="""
            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'txn.i_entity', 'description', 'Unique identifier for the entity.');

            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'txn.i_teller', 'description', 'Identifier or name of the teller.');

            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'txn.n_cash_box', 'description', 'Number of the cash box used.');

            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'txn.d_business', 'description', 'Date of the business transaction.');

            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'txn.c_txn_type', 'description', 'Code representing the type of transaction.');

            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'txn.n_branch_au', 'description', 'Branch or AU.');

            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'txn.a_start_cash', 'description', 'Amount of cash at the start of the transaction.');

            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'txn.a_end_cash', 'description', 'Amount of cash at the end of the transaction.');

                    
            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'cash_advance.i_entity', 'description', 'Unique identifier for the entity.');

            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'cash_advance.i_teller', 'description', 'Identifier or name of the teller.');

            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'cash_advance.f_amt_confirm', 'description', 'Confirmed amount of the cash advance.');

            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'cash_advance.d_business', 'description', 'Date of the business transaction.');

            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'cash_advance.c_txn_type', 'description', 'Code representing the type of transaction.');

            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'cash_advance.n_branch_au', 'description', 'Branch or AU');

            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'cash_advance.c_term_id', 'description', 'Terminal identifier.');

            INSERT INTO metadata (target_type, target_name, metadata_key, metadata_value)
            VALUES ('column', 'cash_advance.c_pinpad_status', 'description', 'Status of the PIN pad.');

            """
        print(sql_script)    
        cursor.executescript(sql_script)
        conn.commit()  # Important to save the table creation
        print('Metadata created')

        return conn



    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        if conn:  # Ensure connection is closed even if error occurs
            conn.close()
        return None


if __name__ == "__main__":

            print('start')
            conn = create_sqlite_database()

            if conn:
                conn.close()  # Close the connection when done.  No data insertion in this example.
            