from advanced_user_operations import AdvancedUserOperations
import unittest

class TestAdvancedUserOperations(unittest.TestCase):
    def setUp(self):
        self.advanced_user_ops = AdvancedUserOperations()
    
    # reset the database
    def tearDown(self):
        self.advanced_user_ops.cursor.execute("DELETE FROM users")
        self.advanced_user_ops.conn.commit()

    def test_create_user_with_profile(self):
        print("Creating a new user...")
        result_create = self.advanced_user_ops.create_user_with_profile('Peter Parker', 'john.doe@one.com', 'test123', age=30, gender='Male', address='123 Main St')
        self.assertTrue(result_create)

        print("user result", result_create)
        
        users = self.advanced_user_ops.retrieve_users_by_criteria(min_age=30, max_age=30, gender='Male')
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0][2], 'john.doe@one.com')

    def test_retrieve_users_by_criteria(self):
        print("\nRetrieving users...")
        self.advanced_user_ops.create_user_with_profile('Mary Jane', 'mary.jane@one.com', 'test456', age=25, gender='Female', address='456 Oak St')
        users = self.advanced_user_ops.retrieve_users_by_criteria(min_age=25, max_age=25, gender='Female')
        self.assertEqual(len(users), 1)
        for user in users:
            print(f"Users Retrieved: ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, Age: {user['age']}, Gender: {user['gender']}, Address: {user['address']}")
        
        self.assertEqual(users[0][2], 'mary.jane@one.com')

    def test_update_user_profile(self):
        print("\nUpdating user profile...")
        self.advanced_user_ops.create_user_with_profile('Peter Parker', 'john.doe@one.com', 'test123', age=30, gender='Male', address='123 Main St')
        result_update = self.advanced_user_ops.update_user_profile('john.doe@one.com', age=35, address='456 Oak St')
        self.assertTrue(result_update)
        print("User profile update result:", result_update )
        
        users = self.advanced_user_ops.retrieve_users_by_criteria(gender='Male')
        updated_user = [user for user in users if user['email'] == 'john.doe@one.com'][0]  
        self.assertEqual(updated_user['address'], '456 Oak St')



    def test_delete_users_by_criteria(self):
        print("\nDeleting users...")
        self.advanced_user_ops.create_user_with_profile('Mary Jane', 'mary.jane@one.com', 'test456', age=25, gender='Female', address='456 Oak St')
        result_delete = self.advanced_user_ops.delete_users_by_criteria(gender='Female')
        self.assertEqual(result_delete, 1)
        print("User deletion result:", result_delete)
        
        users = self.advanced_user_ops.retrieve_users_by_criteria(gender='Female')
        self.assertEqual(len(users), 0)

if __name__ == '__main__':
    unittest.main()
