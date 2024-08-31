import os
from datetime import datetime

class Product:
    ids_file = "ids_file.txt"
    data_file = "data_file.txt"
    
    def __init__(self, name, description, quantity, price, created_at, updated_at="Not yet updated"):
        self.__id = self.generateID()
        self.name = name
        self.description = description
        self.quantity = quantity
        self.price = price
        self.created_at = created_at
        self.updated_at = updated_at
    
    def get_id(self):
        return self.__id
    
    def __str__(self):
        return f"{self.__id}, {self.name}, {self.description}, {self.quantity}, {self.price}, {self.created_at}, {self.updated_at}"
    
    @staticmethod
    def generateID():
        last_id = Product.get_last_id()
        if last_id:
            number_part = int(last_id.split('-')[1])
            new_number_part = number_part + 1
        else:
            new_number_part = 1
        
        new_id = f"Prod-{str(new_number_part).zfill(3)}"
        Product.save_last_id(new_id)
        return new_id
    
    @staticmethod
    def get_last_id():
        if os.path.exists(Product.ids_file):
            with open(Product.ids_file, 'r') as file:
                lines = file.readlines()
                if lines:
                    return lines[-1].strip()
        return None
    
    @staticmethod
    def save_last_id(new_id):
        with open(Product.ids_file, 'w') as file:
            file.write(new_id + '\n')
    
    @staticmethod
    def save_product(product):
        try:
            with open(Product.data_file, 'a') as file:
                file.write(str(product) + '\n')
            return True  # Successfully saved
        except IOError as e:
            print(f"Error saving product: {e}")
            return False  # Failed to save
    
    @staticmethod
    def load_products():
        products = []
        if os.path.exists(Product.data_file):
            with open(Product.data_file, 'r') as file:
                for line in file:
                    product = Product.from_string(line.strip())
                    if product:
                        products.append(product)
        return products
    
    @staticmethod
    def from_string(data):
        try:
            id, name, description, quantity, price, created_at, updated_at = data.split(', ')
            product = Product(name, description, int(quantity), float(price), created_at, updated_at)
            product.__id = id
            return product
        except ValueError as e:
            print(f"Error parsing data: {e}")
            return None

def create_divider(char='-', length=50):
    print(char * length)

def Create_Product():
    try:
        is_Correct = False
        while not is_Correct:
            create_divider()
            print("Create Product")
            create_divider()
            name = input("Enter name            : ")
            desc = input("Enter description     : ")
            quantity = int(input("Enter quantity        : "))
            price_input = float(input("Enter price           : "))
            formatted_price = f"{price_input:.2f}"
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Preview inputs
            create_divider()
            print("Preview Product")
            create_divider()
            print(f"Name       : {name}")
            print(f"Description: {desc}")
            print(f"Quantity   : {quantity}")
            print(f"Price      : {formatted_price}")
            print(f"Created At : {created_at}")
            create_divider()

            user_input = input("Is this right? [Y/N]: ").strip().lower()

            if user_input == 'y':
                is_Correct = True
                product = Product(name, desc, quantity, formatted_price, created_at, "Not yet updated")
                if Product.save_product(product):
                    print("Product created successfully!")
                else:
                    print("Failed to add the product.")   
            elif user_input == 'n':
                print("Please re-enter the details.")
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")
    except ValueError as e:
        print(f"Error: Invalid input. Please enter a valid number for quantity and price. ({e})")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def Read_Product():
    create_divider()
    print("Read Products")
    create_divider()
    products = Product.load_products()
    
    if products:
        # Calculate column widths
        max_id_len = max(len(p.get_id()) for p in products)
        max_name_len = max(len(p.name) for p in products)
        max_desc_len = max(len(p.description) for p in products)
        max_qty_len = max(len(str(p.quantity)) for p in products)
        max_price_len = max(len(f"{p.price:.2f}") for p in products)
        max_created_at_len = max(len(p.created_at) for p in products)
        max_updated_at_len = max(len(p.updated_at) for p in products)

        # Print header
        header = (f"{'ID':<{max_id_len}} | {'Name':<{max_name_len}} | {'Description':<{max_desc_len}} | "
                  f"{'Quantity':<{max_qty_len}} | {'Price':<{max_price_len}} | {'Created At':<{max_created_at_len}} | "
                  f"{'Updated At':<{max_updated_at_len}}")
        print(header)
        create_divider()

        # Print each product
        for product in products:
            print(f"{product.get_id():<{max_id_len}} | {product.name:<{max_name_len}} | {product.description:<{max_desc_len}} | "
                  f"{product.quantity:<{max_qty_len}} | {product.price:<{max_price_len}.2f} | {product.created_at:<{max_created_at_len}} | "
                  f"{product.updated_at:<{max_updated_at_len}}")

    else:
        print("No products found.")
    create_divider()
    
def Update_Product(product_id):
    create_divider()
    print(f"Update Product with ID: {product_id}")
    create_divider()
    
    products = Product.load_products()
    product_to_update = next((p for p in products if p.get_id() == product_id), None)
    
    if product_to_update:
        # Ask for new details
        print("Current details:")
        print(product_to_update)
        
        name = input("Enter new name (leave blank to keep current): ") or product_to_update.name
        desc = input("Enter new description (leave blank to keep current): ") or product_to_update.description
        quantity = input(f"Enter new quantity (current: {product_to_update.quantity}): ")
        price = input(f"Enter new price (current: {product_to_update.price}): ")
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update values
        if quantity:
            product_to_update.quantity = int(quantity)
        if price:
            product_to_update.price = float(price)
        product_to_update.name = name
        product_to_update.description = desc
        product_to_update.updated_at = updated_at
        
        # Save updated products
        with open(Product.data_file, 'w') as file:
            for product in products:
                file.write(str(product) + '\n')
        
        print("Product updated successfully!")
    else:
        print("Product not found.")
    create_divider()

def Delete_Product(product_id):
    create_divider()
    print(f"Delete Product with ID: {product_id}")
    create_divider()
    
    products = Product.load_products()
    updated_products = [p for p in products if p.get_id() != product_id]
    
    if len(updated_products) < len(products):
        # Save updated products
        with open(Product.data_file, 'w') as file:
            for product in updated_products:
                file.write(str(product) + '\n')
        
        print("Product deleted successfully!")
    else:
        print("Product not found.")
    create_divider()

def main():
    while True:
        try:
            create_divider()
            print("Welcome to Product Inventory System")
            create_divider()
            print("[1] Create product")
            print("[2] Read products")
            print("[3] Update product")
            print("[4] Delete product")
            print("[0] Exit")
            create_divider()

            user_input = int(input("Select: "))

            if user_input == 1:
                Create_Product()
            elif user_input == 2:
                Read_Product()
            elif user_input == 3:
                product_id = input("Enter product ID to update: ")
                Update_Product(product_id)
            elif user_input == 4:
                product_id = input("Enter product ID to delete: ")
                Delete_Product(product_id)
            elif user_input == 0:
                print("Exiting the system.")
                break
            else:
                print("Invalid selection. Please choose a valid option.")
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
