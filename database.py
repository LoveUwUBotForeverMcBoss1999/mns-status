import os
from typing import List, Dict, Optional
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                port=int(os.getenv('DB_PORT', 3306)),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )

            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("Database connection established successfully")
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            self.connection = None
            self.cursor = None

    def get_top_islands(self, limit: int = 10) -> List[Dict]:
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
            if not self._check_connection():
                return []

            self.cursor.execute(query, (limit,))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error retrieving top islands: {e}")
            return []

    def search_islands(self, search_term: str) -> List[Dict]:
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
            if not self._check_connection():
                return []

            self.cursor.execute(query, (search_pattern, search_pattern))
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error searching islands: {e}")
            return []

    def get_island_by_owner(self, owner: str) -> Optional[Dict]:
        """
        Get full details of an island by owner
        """
        query = """
        SELECT * FROM islands
        WHERE owner = %s
        """
        try:
            if not self._check_connection():
                return None

            self.cursor.execute(query, (owner,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error retrieving island by owner: {e}")
            return None

    def _check_connection(self) -> bool:
        """
        Check if database connection is established
        """
        if not self.cursor:
            print("Database connection not established")
            return False
        return True

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
