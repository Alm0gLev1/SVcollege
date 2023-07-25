print('Welcome to Python Project by Almog Levi.\n')


class Supermarket:
    def __init__(self):
        self.categories = {}
        self.shopping_cart = []

    def add_category_check(self):
        existing_categories = list(self.categories.keys())
        if existing_categories:
            print("Existing Categories:")
            for category in existing_categories:
                print(f"- {category}")

    def add_category(self, category_name):
        category_name_lower = category_name.lower()
        if category_name_lower in (name.lower() for name in self.categories):
            print(f"Category '{category_name}' already exists.")
            return

        self.categories[category_name_lower] = []
        print(f"Category '{category_name}' added successfully.")

    def add_product(self, category_name, product_id, product_name, calories, proteins, price):
        category_name_lower = category_name.lower()
        if category_name_lower not in self.categories:
            print(f"Category '{category_name}' does not exist. Please create the category first.")
            return

        product_name_lower = product_name.lower()

        for product in self.categories[category_name_lower]:
            if product['id'] == product_id:
                print(f"Product with ID '{product_id}' already exists. Please use a unique ID.")
                return
            if product['name'].lower() == product_name_lower:
                print(f"Product with name '{product_name}' already exists in category '{category_name}'. "
                      f"Please use a unique name.")
                return

        new_product = {
            'id': product_id,
            'name': product_name,
            'calories': calories,
            'proteins': proteins,
            'price': price
        }
        self.categories[category_name_lower].append(new_product)
        print(f"Product '{product_name}' added successfully to category '{category_name}'.")

    def remove_product_by_id(self):
        self.show_categories()
        category_name = input("Enter the category name where the product is located: ")
        category_name_lower = category_name.lower()
        if category_name_lower not in self.categories:
            print(f"Category '{category_name}' does not exist. Please enter a valid category.")
            return

        print(f"Current products in category '{category_name}':")
        for product in self.categories[category_name_lower]:
            print(f"ID: {product['id']} - Name: {product['name']}")

        try:
            product_id = int(input("Enter the ID of the product to remove: "))
            for product in self.categories[category_name_lower]:
                if product['id'] == product_id:
                    self.categories[category_name_lower].remove(product)
                    print(f"Product with ID '{product_id}' removed successfully from category '{category_name}'.")
                    return

            print(f"Product with ID '{product_id}' not found in category '{category_name}'.")
        except ValueError:
            print("Invalid input for product ID. Please enter a valid integer.")

    def change_product_name(self):
        print("Existing Categories:")
        for category in self.categories:
            print(f"- {category}")

        category_name = input("Enter the category name where the product is located: ")
        category_name_lower = category_name.lower()
        if category_name_lower not in self.categories:
            print(f"Category '{category_name}' does not exist. Please enter a valid category.")
            return

        print(f"Current products in category '{category_name}':")
        for product in self.categories[category_name_lower]:
            print(f"- {product['name']}")

        product_name = input("Enter the current product name: ")
        product_name_lower = product_name.lower()

        for product in self.categories[category_name_lower]:
            if product['name'].lower() == product_name_lower:
                new_name = input("Enter the new product name: ")
                product['name'] = new_name
                print(f"Product name changed successfully to '{new_name}'.")
                return

        print(f"Product with name '{product_name}' not found in category '{category_name}'.")

    def add_to_cart(self, product_id):
        for category_products in self.categories.values():
            for product in category_products:
                if product['id'] == product_id:
                    amount = int(input(f"Enter the amount of '{product['name']}' to add to the cart: "))
                    if amount <= 0:
                        print("Invalid amount. Please enter a positive number.")
                        return

                    product_copy = product.copy()
                    product_copy['amount'] = amount
                    self.shopping_cart.append(product_copy)
                    print("Current Shopping Cart:")
                    for item in self.shopping_cart:
                        print(f"- {item['amount']} Amount for {item['name']}")
                    return
        print(f"Product with ID '{product_id}' not found.")

    def calculate_total_price(self):
        total_price = sum(product['price'] * product['amount'] for product in self.shopping_cart)
        total_price_with_vat = total_price * 1.17
        return total_price_with_vat

    def show_categories(self):
        if not self.categories:
            print("None found.")
        else:
            print("Existing Categories:")
            for category in self.categories:
                print(f"- {category}")

    def show_products_in_category(self):
        print("Existing Categories:")
        for category in self.categories:
            print(f"- {category}")

        category_name = input("Enter the category name: ")
        category_name_lower = category_name.lower()
        if category_name_lower not in self.categories:
            print(f"Category '{category_name}' does not exist. Please enter a valid category.")
            return

        print(f"Current products in category '{category_name}':")
        for product in self.categories[category_name_lower]:
            print(f"ID: {product['id']} - Name: {product['name']}")


def display_menu():
    print("Supermarket Database Menu:")
    print("1. Add Category")
    print("2. Add Product to Category")
    print("3. Remove Product by ID")
    print("4. Change Product Name")
    print("5. Add Product to Shopping Cart")
    print("6. Calculate Total Price with VAT")
    print("7. Show Existing Categories")
    print("8. Show Existing Products in Specific Category")
    print("9. Exit")

    while True:
        try:
            choice = int(input("Enter your choice (1-9): "))
            if 1 <= choice <= 9:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a valid number between 1 and 9.")


supermarket = Supermarket()

while True:
    choice = display_menu()

    if choice == 1:
        supermarket.add_category_check()
        category_name = input("Enter the category name: ")
        supermarket.add_category(category_name)

    elif choice == 2:
        supermarket.add_category_check()
        category_name = input("Enter the category name: ")
        category_name_lower = category_name.lower()
        if category_name_lower not in supermarket.categories:
            print(f"Category '{category_name}' does not exist. Please create the category first.")
            continue

        if supermarket.categories[category_name_lower]:
            print(f"Existing products in category '{category_name}':")
        for product in supermarket.categories[category_name_lower]:
            print(f"ID: {product['id']} - Name: {product['name']}")

        try:
            product_id = int(input("Enter the product ID: "))
            product_name = input("Enter the product name: ")
            calories = float(input("Enter the calories: "))
            proteins = float(input("Enter the proteins: "))
            price = float(input("Enter the price: "))
            supermarket.add_product(category_name, product_id, product_name, calories, proteins, price)
        except ValueError:
            print("Invalid input for product ID. Please enter a valid integer.")

    elif choice == 3:
        supermarket.remove_product_by_id()

    elif choice == 4:
        supermarket.change_product_name()

    elif choice == 5:
        print("Existing Categories:")
        for category in supermarket.categories:
            print(f"- {category}")

        category_name = input("Enter the category name: ")
        category_name_lower = category_name.lower()
        if category_name_lower not in supermarket.categories:
            print(f"Category '{category_name}' does not exist. Please enter a valid category.")
            continue

        print(f"Current products in category '{category_name}':")
        for product in supermarket.categories[category_name_lower]:
            print(f"- {product['id']} {product['name']}")

        try:
            product_id = int(input("Enter the product ID to add to the cart: "))
            supermarket.add_to_cart(product_id)
        except ValueError:
            print("Invalid input for product ID. Please enter a valid integer.")

    elif choice == 6:
        total_price = supermarket.calculate_total_price()
        print(f"Total price with VAT: {total_price:.2f}")

    elif choice == 7:
        supermarket.show_categories()

    elif choice == 8:
        supermarket.show_products_in_category()

    elif choice == 9:
        print("Exiting the program. Thank you for using the Supermarket Database!")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 9.")
