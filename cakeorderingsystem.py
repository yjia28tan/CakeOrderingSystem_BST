import random
import re
from tabulate import tabulate


class Cake:
    def __init__(self, code, flavour, weight, unit_price):
        self.code = code
        self.flavour = flavour
        self.weight = weight
        self.unit_price = unit_price


class Customer:
    cus_id_counter = 1  # Auto-increasing variable for generating unique customer IDs

    def __init__(self, name, address, contact):
        self.customer_id = Customer.cus_id_counter
        Customer.cus_id_counter += 1
        self.name = name
        self.address = address
        self.contact_number = contact


class Order:
    def __init__(self, customer):
        self.order_id = None  # initialise the order_id to None
        self.customer = customer
        self.cake_items = []  # list to add multiple cakes into the order

    def set_order_id(self, order_id):  # mutator method to set the order id (initially None)
        self.order_id = order_id

    def add_cake(self, cake, weight, quantity):
        # Function to add cake into the list in constructor
        self.cake_items.append((cake, weight, quantity))

    def calculate_total_amount(self):
        total_amount = 0.0
        for cake, weight, quantity in self.cake_items:
            cake_price = cake.unit_price
            cake_weight = weight
            cake_quantity = quantity
            subtotal = cake_price * cake_weight * cake_quantity
            total_amount += subtotal
        return total_amount


class Node:
    def __init__(self, order):
        self.order = order
        self.left = None
        self.right = None


class OrderBST:
    def __init__(self):
        self.root = None

    def insert_order(self, order):
        if self.root is None:  # if BST empty
            self.root = Node(order)  # insert the node as root
        else:  # if not empty
            self._insert_order(self.root, order)

    def _insert_order(self, node, order):
        # recursive method to insert data
        if order.order_id < node.order.order_id:  # if the value is smaller than the current node
            if node.left is None:  # the left side of the node is empty
                node.left = Node(order)  # insert the order to left subtree as a leaf
            else:  # if the node have left subtree
                self._insert_order(node.left, order)  # traverse the node to the left until find the position
        elif order.order_id > node.order.order_id:  # if the value is bigger than the current node
            if node.right is None:
                node.right = Node(order)
            else:
                self._insert_order(node.right, order)

    def search_order(self, order_id):
        return self._search_order(self.root, order_id)

    def _search_order(self, node, order_id):
        # recursive method to search order
        if node is None or node.order.order_id == order_id:  # Return None if empty or don't have the order ID
            return node.order if node else None  # Return node.order if the order ID is found
        if order_id < node.order.order_id:  # if the order ID is smaller than the node order ID
            return self._search_order(node.left, order_id)  # move the node to left and check again
        else:  # if the order ID is larger than the node order ID
            return self._search_order(node.right, order_id)  # move the node to right and check again

    def display_all_order_ids(self):
        if self.root is None:  # if the BST is empty
            print("There are no orders.")
            return
        self._display_all_order_ids(self.root)

    def _display_all_order_ids(self, node):
        if node is not None:  # print the order IDs that are in the BST using in-order traversal
            self._display_all_order_ids(node.left)
            order = node.order
            print(f"Order ID: {order.order_id}\tCustomer Name: {order.customer.name}\t"
                  f"Total Amount: RM {order.calculate_total_amount():.2f}")
            self._display_all_order_ids(node.right)

    def view_orders_details(self, current_node, order):
        # display all the order details for selected order ID using in-order traversal
        if current_node is not None:  # if the current node is not empty
            self.view_orders_details(current_node.left, order)
            # the current node traversal from the left child to search on the order id
            if current_node.order.order_id == order.order_id:  # when the order id is matched, print the order details
                print("\n----------------------------------------------------------------------------------------------")
                print(f"Order ID: {current_node.order.order_id}")
                print("--- Customer Details ---")
                print(f"Customer ID: {current_node.order.customer.customer_id}")
                print(f"Name: {current_node.order.customer.name}")
                print(f"Address: {current_node.order.customer.address}")
                print(f"Contact Number: {current_node.order.customer.contact_number}")
                print("\n--- Cake Order Details ---")
                for cake, weight, quantity in current_node.order.cake_items:
                    print(f"Cake Code: {cake.code}")
                    print(f"Flavour: {cake.flavour}")
                    print(f"Weight: {weight} kg")
                    print(f"Quantity: {quantity}")
                    print("")
                print(f"Total Amount: RM {current_node.order.calculate_total_amount():.2f}")
                print("----------------------------------------------------------------------------------------------")
            self.view_orders_details(current_node.right, order)
            # the current node traversal from the right child to search on the order id

    def modify_order(self, order_id, new_cake_code, new_flavour, new_weight, new_quantity, new_unit_price,
                     new_customer_name, new_customer_address, new_contact):
        # modify the details of a specific order
        self._modify_recursive(self.root, order_id, new_cake_code, new_flavour, new_weight, new_quantity,
                               new_unit_price, new_customer_name, new_customer_address, new_contact)

    def _modify_recursive(self, current_node, order_id, new_cake_code, new_flavour, new_weight, new_quantity,
                          new_unit_price, new_customer_name, new_customer_address, new_contact):
        # private helper method
        if current_node.order.order_id == order_id:  # when the order ID is found
            total_amount = 0.0  # assign the total amount to 0 so that can recalculate the total
            for i, (cake, weight, quantity) in enumerate(current_node.order.cake_items):
                # to update the cake lists in the order by assigning the new value
                if cake.code == new_cake_code:
                    # Update cake details base on the cake code
                    cake.code = new_cake_code
                    cake.flavour = new_flavour
                    cake.unit_price = new_unit_price
                    current_node.order.cake_items[i] = (cake, new_weight, new_quantity)
                    # update the order cake details based on new value into the tuple list
                subtotal = cake.unit_price * new_weight * new_quantity
                total_amount += subtotal
            current_node.order.total_amount = total_amount
            current_node.order.customer_name = new_customer_name
            current_node.order.customer_address = new_customer_address
            current_node.order.customer.contact_number = new_contact

        elif order_id < current_node.order.order_id:
            self._modify_recursive(current_node.left, order_id, new_cake_code, new_flavour, new_weight, new_quantity,
                                   new_unit_price, new_customer_name, new_customer_address, new_contact)
        else:
            self._modify_recursive(current_node.right, order_id, new_cake_code, new_flavour, new_weight, new_quantity,
                                   new_unit_price, new_customer_name, new_customer_address, new_contact)

    def delete_order(self, order_id):
        self.root = self._delete_order(self.root, order_id)

    def _delete_order(self, node, order_id):
        # To find the target node
        if node is None:  # if the order ID not found
            return node
        if order_id < node.order.order_id:
            node.left = self._delete_order(node.left, order_id)
        elif order_id > node.order.order_id:
            node.right = self._delete_order(node.right, order_id)
        else:  # Target found
            # Node with no child or only one child
            if node.left is None:  # The node does not have left child ( 1 right child )
                temp = node.right  # temp (pointer in C++) point to the right child
                node = None  # delete the node
                return temp  # the right child become the new node
            elif node.right is None:  # The node does not have right child ( 1 left child )
                temp = node.left
                node = None
                return temp
            # The target node has two children
            temp = self._min_value_node(node.right)  # Find the successor node (smallest in the right subtree)
            node.order = temp.order  # replaces the target node's content with the order of the successor node
            node.right = self._delete_order(node.right, temp.order.order_id)  # Delete the inorder successor
        return node

    @staticmethod  # does not depend on any instance-specific data and does not modify the state of the object
    def _min_value_node(node):
        # to find the smallest value of order ID
        current = node
        while current.left is not None:  # loop down to find the smallest value leaf
            current = current.left
        return current


class CakeOrderingSystem:
    def __init__(self):
        self.bst = OrderBST()
        self.cake_lists = []  # List to store available cake objects

    @staticmethod
    def display_menu():
        print(" Hi~ o(*￣▽￣*)ブ  Le Grande Cake Ordering System ")
        print("1. View Cake Lists")
        print("2. Place an Order")
        print("3. View All Order IDs, Customer Names and Total Amount")
        print("4. View Selected Order Details")
        print("5. Modify an Order")
        print("6. Delete an Order")
        print("7. Exit")

    def generate_order_id(self):
        while True:
            order_id = random.randint(100, 10000)
            if not self.bst.search_order(order_id):  # so that the order ID does not duplicate
                return order_id

    def available_cake_list(self):
        # Create cake objects and add them to the cake list
        cake1 = ["1", "Belgium Chocolate Cheesecake", 1.0, 115.00]
        cake2 = ["2", "Burnt Cheesecake", 1.0, 95.00]
        cake3 = ["3", "Strawberry Shortcake", 1.0, 120.00]
        cake4 = ["4", "French Earl Grey", 1.0, 98.50]
        cake5 = ["5", "Lemon Tart", 1.0, 100.50]
        cake6 = ["6", "Lemon Poppy Seed", 1.0, 97.80]
        cake7 = ["7", "Black Forest", 1.0, 96.70]
        cake8 = ["8", "White Forest", 1.0, 96.70]
        cake9 = ["9", "Matchamisu", 1.0, 130.00]
        cake10 = ["10", "Tiramisu (contain alcohol)", 1.0, 135.00]
        cake11 = ["11", "Red Velvet", 1.0, 89.00]
        cake12 = ["12", "Blueberry Cheesecake", 1.0, 128.50]

        self.cake_lists = [cake1, cake2, cake3, cake4, cake5, cake6, cake7, cake8, cake9, cake10, cake11, cake12]

    def view_cake_list(self):
        # print the cake lists in table
        # print("")
        self.available_cake_list()
        headers = ["Cake Code", "Flavour", "Weight (kg)", "Unit Price (RM/kg)"]
        table = tabulate(self.cake_lists, headers=headers, tablefmt="grid")
        print(table)

    def get_cake_info(self, cake_code):
        # to get the cake details for specific cake code (use in modify cake order)
        for cake in self.cake_lists:
            if cake[0] == cake_code:
                flavour = cake[1]
                unit_price = cake[3]
                return flavour, unit_price
        return None

    def place_order(self):
        print("\n~~~~~ Place an Order ~~~~~")
        print("--- Customer Details ---")
        customer_name = input("Enter Customer Name: ")
        customer_address = input("Enter Customer Address: ")
        customer_contact = None

        # Validate customer details input must be filled
        while not customer_name or not customer_address:
            print("Customer details cannot be empty. Please try again.")
            customer_name = input("Enter Customer Name: ")
            customer_address = input("Enter Customer Address: ")

        while customer_contact is None:
            customer_contact = input("Contact number: ")

            # Validate contact number format
            if not re.match(r'^0\d{9,10}$', customer_contact):
                print("Invalid contact number. Please try again. "
                      "Contact number must start with '0' and have 10-11 digits.")
                customer_contact = None

        # create an object called new_customer for Customer class and pass the user input attributes to the class
        new_customer = Customer(customer_name, customer_address, customer_contact)
        # create new_order object and pass it into Order class
        new_order = Order(new_customer)

        new_order.set_order_id(self.generate_order_id())  # set the order id using random generated id
        # by calling the set_order_id function in the Order class

        print("")
        self.view_cake_list()  # display the cake lists
        print("\n--- Cake Order Details ---")

        while True:
            cake_code = input("\nEnter Cake Code: ")
            cake = None  # initialise the cake to None
            for c in self.cake_lists:
                if c[0] == cake_code:  # the cake code entered is exists
                    cake = Cake(c[0], c[1], c[2], c[3])  # create an object cake and pass it into the Cake class
                    break

            if cake is None:  # not selecting any cake or invalid cake code
                print("Invalid Cake Code. Please try again.")
                continue

            weight = None  # initialise the weight to None
            print("\nAvailable Weight (kg): 0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0 \n")
            while weight is None:
                try:
                    weight = float(input("Enter Weight (in kg): "))
                    if weight not in [0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
                        raise ValueError
                except ValueError:
                    print("Invalid Weight. Please enter a valid weight from the options.\n")
                    weight = None

            quantity = None
            while quantity is None:
                try:
                    quantity = int(input("Enter Quantity: "))
                    if quantity <= 0:  # validate the quantity do not get the negative value or 0
                        raise ValueError
                except ValueError:
                    print("Invalid Quantity. Please enter a positive integer.")
                    quantity = None

            new_order.add_cake(cake, weight, quantity)  # add the cake into the list that declare in the Order class

            choice = input("\nDo you want to add another cake? (Press 'y' if yes): ")
            if choice.lower() != "y":  # any input beside of y will exit the loop to add multiple cake
                break

        # Calculate and display total amount
        total_amount = new_order.calculate_total_amount()
        print(f"Total Amount: RM {total_amount:.2f}")

        # Insert order to BST
        self.bst.insert_order(new_order)
        print("Order Placed Successfully!\n")
        self.bst.view_orders_details(self.bst.root, new_order)
        input("\nPress Enter to continue...")

    def view_all_ordersID(self):
        # display all orders in BST
        print("\n~~~~~ All Orders ~~~~~")
        self.bst.display_all_order_ids()
        input("\nPress Enter to continue...")

    def view_order_details(self):
        # display selected order in the BST
        print("\n~~~~~ Order Details ~~~~~")

        if self.bst.root is None:  # if the BST is empty
            print("There are no orders.")
            input("\nPress Enter to continue...")
            return

        while True:
            try:
                order_id = int(input("\nEnter Order ID (Press 0 to cancel): "))
                if order_id < 0:  # if negative number
                    raise ValueError
                if order_id == 0:
                    return  # Exit the function or method
            except ValueError:
                print("Invalid Order ID. Please enter a positive integer.")
                continue

            # Search the order in BST
            order = self.bst.search_order(order_id)
            if order is not None:
                # Order found
                self.bst.view_orders_details(self.bst.root, order)  # print order details
                break
            else:
                print("Order not found. Please try again.")

        input("\nPress Enter to continue...")

    def modify_order(self):
        # modify the value in the order
        print("~~~~~ Modify an Order ~~~~~")

        if self.bst.root is None:  # if the BST is empty
            print("There are no orders.")
            input("\nPress Enter to continue...")
            return

        while True:
            try:
                order_id = int(input("\nEnter Order ID (Press 0 to cancel): "))
                if order_id < 0:  # if negative number
                    raise ValueError
                if order_id == 0:
                    return  # Exit the function2
            except ValueError:
                print("Invalid Order ID. Please enter a positive integer.")
                continue

            # Search the order in BST
            order = self.bst.search_order(order_id)
            if order is not None:  # Order found
                self.bst.view_orders_details(self.bst.root, order)  # print order details

                # Prompt the user for the new details
                print("\n--- Modify Customer's Details ---")
                new_name = input("Enter new customer name (leave blank to keep current): ")
                new_address = input("Enter new customer address (leave blank to keep current): ")
                new_contact = input("Enter new customer contact number (leave blank to keep current): ")

                if new_contact != "":
                    while not re.match(r'^0\d{9,10}$', new_contact):
                        print("Invalid contact number. Please try again. "
                              "Contact number must start with '0' and have 10-11 digits.")
                        new_contact = input("\nEnter new customer contact number (leave blank to keep current): ")
                    order.customer.contact_number = new_contact

                # Update the customer details
                if new_name != "":
                    order.customer.name = new_name
                if new_address != "":
                    order.customer.address = new_address

                # Update cake items
                choice = input("\nDo you want to modify the cake items? (Press 'y' if yes): ")
                if choice.lower() == "y":
                    print("\n--- Modify Cake Items ---")
                    self.view_cake_list()  # display cake lists
                    for i, (cake, weight, quantity) in enumerate(order.cake_items):
                        print(f"\nCake Item {i + 1}:")
                        while True:
                            new_cake_code = input("Enter New Cake Code (Press Enter to keep current): ")
                            if new_cake_code:  # if the new cake code enter
                                # Get the flavour and unit price based on the cake code
                                cake_info = self.get_cake_info(new_cake_code)
                                if cake_info:  # based on the cake info for that cake code update the cake details
                                    flavour, unit_price = cake_info
                                    cake.code = new_cake_code
                                    cake.flavour = flavour
                                    cake.unit_price = unit_price
                                    print("\nCake details updated!")
                                    break  # Exit the while loop
                                else:
                                    print("Invalid cake code. Please try again.\n")
                            else:
                                print("The cake is remain unchanged.")
                                break  # Exit the while loop is keep the same value

                        print("\nAvailable Weight (kg): 0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0 \n")

                        # update new weight
                        while True:
                            new_weight = input("Enter New Weight (Press Enter to keep current): ")
                            if new_weight != "":
                                try:
                                    if new_weight in ['0.25', '0.5', '1', '1.0', '1.5', '2', '2.0', '2.5', '3', '3.0']:
                                        weight = float(new_weight)  # update the new weight to weight
                                        break  # Exit the loop if valid weight is entered
                                    else:
                                        raise ValueError
                                except ValueError:
                                    print("Invalid Weight. Please enter a valid weight from the options.\n")
                            else:
                                print("The current weight is remain unchanged.\n")
                                break

                        # update new quantity
                        while True:
                            new_quantity = input("Enter New Quantity (Press Enter to keep current): ")
                            if new_quantity != "":
                                try:
                                    new_quantity_int = int(new_quantity)  # covert the string entered to int
                                    if new_quantity_int >= 1:
                                        quantity = int(new_quantity_int)  # update the new quantity to quantity
                                        break  # Exit the loop if valid quantity is entered
                                    else:
                                        raise ValueError
                                except ValueError:
                                    print("Invalid Quantity. Please enter a positive integer.\n")
                            else:
                                print("The current quantity is remain unchanged.\n")
                                break

                        # update the cake details for the order in the list
                        order.cake_items[i] = (cake, weight, quantity)

                # Recalculate total amount
                order.calculate_total_amount()

                print("Order Modified Successfully!")
                print(f"\nUpdated Order Details for Order ID {order_id}:")
                self.bst.view_orders_details(self.bst.root, order)
                break
            else:
                print("Order not found. Please try again.")
                continue
        input("\nPress Enter to continue...")

    def delete_order(self):
        print("~~~~~ Delete an Order ~~~~~")

        if self.bst.root is None:  # if the BST is empty
            print("There are no orders.")
            input("\nPress Enter to continue...")
            return

        while True:
            try:
                order_id = int(input("Enter Order ID (Press 0 to cancel): "))
                if order_id < 0:  # if negative number
                    raise ValueError
                if order_id == 0:  # Exit the loop
                    return
            except ValueError:
                print("Invalid Order ID. Please enter a positive integer.\n")
                continue

            # Search the order in BST
            order = self.bst.search_order(order_id)
            if order is not None:
                # Order found
                self.bst.view_orders_details(self.bst.root, order)  # print order details
                confirm = input("Are you sure want to delete this order? (Press 'y' if yes): ")
                if confirm.lower() == "y":
                    self.bst.delete_order(order_id)
                    print("\nOrder Deleted Successfully!")
                    break
                else:
                    print("\nDeletion Cancelled.")
                    break
            else:
                print("Order not found. Please try again.")

        input("\nPress Enter to continue...")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-7): ")
            if choice == "1":
                self.view_cake_list()
                input("\nPress Enter to continue...")
            elif choice == "2":
                self.place_order()
            elif choice == "3":
                self.view_all_ordersID()
            elif choice == "4":
                self.view_order_details()
            elif choice == "5":
                self.modify_order()
            elif choice == "6":
                self.delete_order()
            elif choice == "7":
                print("Exiting the program...  ┏(＾0＾)┛ Bye~Bye~")
                break
            else:
                print("Invalid choice. Please try again.\n")


# Create and run the Cake Ordering System
system = CakeOrderingSystem()
system.run()

"""References:
Bhat, S. (n.d.) Deletion in Binary Search Tree 
https://www.geeksforgeeks.org/deletion-in-binary-search-tree/

Kumar, V. (2021) Delete a Node from a Binary Search Tree in Python 
https://www.codespeedy.com/delete-a-node-from-a-binary-search-tree-in-python/

Lane, W. (2021) ‘Writing a Binary Search Tree in Python With Examples’. in Boot.Dev 
https://blog.boot.dev/computer-science/binary-search-tree-in-python/>

PranchalK (n.d.) How to Implement Decrease Key or Change Key in Binary Search Tree? 
https://www.geeksforgeeks.org/how-to-implement-decrease-key-or-change-key-in-binary-search-tree/

Rastogik346 (n.d.) Search and Insertion in Binary Search Tree 
https://www.geeksforgeeks.org/binary-search-tree-set-1-search-and-insertion/
"""
