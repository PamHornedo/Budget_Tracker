#!/usr/bin/env python3
"""
Category Model
Handles category data operations for organizing transactions

TODO: Complete the Category class with CRUD operations
"""

from database.connection import DatabaseConnection

class Category:
    """
    Represents a transaction category (e.g., Food, Transportation)
    """
    
    def __init__(self, name=None, category_type=None, description=None, category_id=None):
        """
        Initialize a category
        
        Args:
            name (str): Category name
            category_type (str): 'income' or 'expense'
            description (str): Category description
            category_id (int): Database ID (for existing categories)
        """
        self.id = category_id
        self.name = name
        self.type = category_type
        self.description = description
        self.db = DatabaseConnection()
    
    def save(self):
        """
        Save category to database
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.validate():
            return False
            
        self.db.connect()
        
        try:
            if self.id:
                query = """
                UPDATE categories 
                SET name = %s, 
                    type = %s, 
                    description = %s 
                WHERE id = %s
                """

                params = (
                    self.name,
                    self.type,
                    self.description,
                    self.id
                )

                self.db.execute_update(query, params)

            else:
                query = """
                INSERT INTO categories (name, type, description) VALUES (%s, %s, %s) RETURNING id
                """
                params = (self.name, self.type, self.description)
                result = self.db.execute_query(query, params)
                
                if result:
                    self.id = result[0]['id'] if isinstance(result[0], dict) else result[0][0]
                
        except Exception as e:
            print(f"❌ Error saving category: {e}")
            return False
        finally:
            self.db.disconnect()
        
        return True
    
    def validate(self):
        """
        Validate category data
        
        Returns:
            bool: True if valid, False otherwise
        """
        
        try:
            if not self.name or not self.name.strip():
                print("Name cannot be empty")
                return False
            
            if len(self.name) > 50:
                print("Name must be under 50 characters")
                return False
            
            if self.type not in ['income', 'expense']:
                print("Type must be 'income' or 'expense'")
                return False
            
            query = "SELECT id FROM categories WHERE name = %s"
            params = (self.name,)
            result = self.db.execute_query(query, params)
        
            if result:
                existing_id = result[0]['id'] if isinstance(result[0], dict) else result[0][0]

            if not self.id or existing_id != self.id:
                print("Category name must be unique")
                return False
        
            return True
    
        except Exception as e:
            print(f"Validation error: {e}")
            return False

        finally:
            self.db.disconnect()
            
    @staticmethod
    def get_all():
        """
        Get all categories from database
        
        Returns:
            list: List of Category objects
        """
        db = DatabaseConnection()
        db.connect()
        
        query = """
        SELECT id, name, type, description 
        FROM categories 
        ORDER BY type, name
        """
        
        results = db.execute_query(query)
        db.disconnect()
        
        categories = []

        for row in results:
            categories.append(Category(
            name=row['name'] if isinstance(row, dict) else row[1],
            category_type=row['type'] if isinstance(row, dict) else row[2],
            description=row['description'] if isinstance(row, dict) else row[3],
            category_id=row['id'] if isinstance(row, dict) else row[0]
        ))
        
        return categories
    
    @staticmethod
    def get_by_type(category_type):
        """
        Get categories by type
        
        Args:
            category_type (str): 'income' or 'expense'
            
        Returns:
            list: List of Category objects
        """
        db = DatabaseConnection()
        db.connect()

        query = """
            SELECT id, name, type, description
            FROM categories
            WHERE type = %s
            ORDER BY name
        """

        results = db.execute_query(query, (category_type,))
        db.disconnect()
        
        categories = []

        for row in results:
            categories.append(Category(
                name=row['name'] if isinstance(row, dict) else row[1],
                category_type=row['type'] if isinstance(row, dict) else row[2],
                description=row['description'] if isinstance(row, dict) else row[3],
                category_id=row['id'] if isinstance(row, dict) else row[0]
            ))

        return categories
    
    @staticmethod
    def get_by_id(category_id):
        """
        Get category by ID
        
        Args:
            category_id (int): Category ID
            
        Returns:
            Category: Category object or None if not found
        """
        db = DatabaseConnection()
        db.connect()
    
        query = """
            SELECT id, name, type, description
            FROM categories
            WHERE id = %s
        """

        result = db.execute_query(query, (category_id,))
        db.disconnect()
                
        if not result:
            return None
                
        row = result[0]

        return Category(
            name=row['name'] if isinstance(row, dict) else row[1],
            category_type=row['type'] if isinstance(row, dict) else row[2],
            description=row['description'] if isinstance(row, dict) else row[3],
            category_id=row['id'] if isinstance(row, dict) else row[0]
        )
    
    def get_transaction_count(self):
        """
        Get number of transactions in this category
        
        Returns:
            int: Number of transactions
        """
        if not self.id:
            return 0
            
        self.db.connect()
        
        # TODO: Count transactions in this category
        query = """
        -- TODO: COUNT transactions for this category
        -- SELECT COUNT(*) as count FROM transactions WHERE category_id = %s
        """
        
        result = self.db.execute_query(query, (self.id,))
        self.db.disconnect()
        
        return result[0]['count'] if result else 0
    
    def delete(self):
        """
        Delete category from database
        Note: This will set category_id to NULL in related transactions
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.id:
            print("❌ Cannot delete category without ID")
            return False
            
        # Check if category is in use
        transaction_count = self.get_transaction_count()
        if transaction_count > 0:
            print(f"⚠️  Category has {transaction_count} transactions. They will be uncategorized.")
            response = input("Continue? (y/N): ")
            if response.lower() != 'y':
                print("❌ Delete cancelled")
                return False
        
        # TODO: Implement delete
        # DELETE FROM categories WHERE id = %s
        
        pass
    
    def __str__(self):
        """
        String representation of category
        """
        return f"{self.name} ({self.type})"
    
    def __repr__(self):
        """
        Developer-friendly representation  
        """
        return f"Category(id={self.id}, name='{self.name}', type='{self.type}')"

def main():
    """
    Test the Category model
    """
    print("🏷️  Testing Category Model")
    print("=" * 30)
    
    # Test getting all categories
    print("📋 All categories:")
    all_categories = Category.get_all()
    
    for category in all_categories:
        count = category.get_transaction_count()
        print(f"  {category} - {count} transactions")
    
    print(f"\n📊 Found {len(all_categories)} total categories")
    
    # Test getting categories by type
    print("\n💰 Income categories:")
    income_categories = Category.get_by_type('income')
    for cat in income_categories:
        print(f"  {cat}")
    
    print("\n💸 Expense categories:")
    expense_categories = Category.get_by_type('expense')
    for cat in expense_categories:
        print(f"  {cat}")

if __name__ == "__main__":
    main()