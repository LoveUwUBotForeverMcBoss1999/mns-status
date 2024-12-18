import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='in.leoxstudios.com',
                port=3306,
                database='s3_mns',
                user='u3_0D7sIfqUWW',
                password='Z.SJrRzT8+i@+MI!U01.4cdf'
            )

            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            self.connection = None
            self.cursor = None

    def get_top_islands(self, limit=10):
        """
        Retrieve top islands based on levels and worth
        """
        query = """
        SELECT 
            name, 
            owner, 
            island_type, 
            levels_bonus, 
            worth_bonus, 
            generated_schematics
        FROM islands
        WHERE levels_bonus IS NOT NULL
        ORDER BY CAST(REPLACE(levels_bonus, ',', '') AS DECIMAL) DESC
        LIMIT %s
        """
        try:
            if not self.cursor:
                raise Error("Database connection not established")

            self.cursor.execute(query, (limit,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error retrieving top islands: {e}")
            return []

    def search_islands(self, search_term):
        """
        Search islands by name or owner
        """
        query = """
        SELECT 
            name, 
            owner, 
            island_type, 
            levels_bonus, 
            worth_bonus, 
            generated_schematics
        FROM islands
        WHERE name LIKE %s OR owner LIKE %s
        """
        search_pattern = f"%{search_term}%"
        try:
            if not self.cursor:
                raise Error("Database connection not established")

            self.cursor.execute(query, (search_pattern, search_pattern))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error searching islands: {e}")
            return []

    def get_island_by_owner(self, owner):
        """
        Get full details of an island by owner
        """
        query = """
        SELECT * FROM islands
        WHERE owner = %s
        """
        try:
            if not self.cursor:
                raise Error("Database connection not established")

            self.cursor.execute(query, (owner,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error retrieving island by owner: {e}")
            return None

    def close(self):
        """
        Close database connection
        """
        try:
            if self.connection and self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")
        except Error as e:
            print(f"Error closing database connection: {e}")
