import sqlite3

class AdvancedUserOperations:
    def __init__(self):
        self.conn = sqlite3.connect('user_database.db')
        self.conn.row_factory = sqlite3.Row 
        self.cursor = self.conn.cursor()
        self.migrate_schema()

    def migrate_schema(self):
        # create the database schema if it doesnt already exist
        with self.conn:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    address TEXT
                )
            """)

    def create_user_with_profile(self, name, email, password, age=None, gender=None, address=None):
        try:
            with self.conn:
                self.cursor.execute("""
                    INSERT INTO users (name, email, password, age, gender, address)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (name, email, password, age, gender, address))
            return True
        except sqlite3.IntegrityError as e:
            raise e

    def retrieve_users_by_criteria(self, min_age=None, max_age=None, gender=None):
        query = "SELECT * FROM users WHERE 1=1"
        params = []
        if min_age is not None:
            query += " AND age >= ?"
            params.append(min_age)
        if max_age is not None:
            query += " AND age <= ?"
            params.append(max_age)
        if gender is not None:
            query += " AND gender = ?"
            params.append(gender)
        with self.conn:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()

    def update_user_profile(self, email, age=None, gender=None, address=None):
        try:
            query = "UPDATE users SET"
            params = []
            if age is not None:
                query += " age = ?,"
                params.append(age)
            if gender is not None:
                query += " gender = ?,"
                params.append(gender)
            if address is not None:
                query += " address = ?,"
                params.append(address)
            query = query.rstrip(",") + " WHERE email = ?"
            params.append(email)
            with self.conn:
                self.cursor.execute(query, params)
            return True
        except sqlite3.Error:
            return False

    def delete_users_by_criteria(self, gender=None):
        query = "DELETE FROM users WHERE 1=1"
        params = []
        if gender is not None:
            query += " AND gender = ?"
            params.append(gender)
        with self.conn:
            self.cursor.execute(query, params)
            return self.cursor.rowcount

    def __del__(self):
        self.conn.close()
def main():
    
    user_ops = AdvancedUserOperations()

    user_ops.create_user_with_profile("Ulises", "one@two.com", "password", 32, "male", "123 Main Ave")
    user_ops.create_user_with_profile("Jessica", "two@three.com", "password", 32, "female", "123 Main Ave")
    users = user_ops.retrieve_users_by_criteria(None, None, "male")

    for user in users:
        print(f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, Age: {user['age']}, Gender: {user['gender']}, Address: {user['address']}")

    user_ops.update_user_profile()

    

if __name__ == "__main__":
    main()