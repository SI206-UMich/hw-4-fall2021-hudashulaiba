import unittest
import random #FOR EXTRA CREDIT

# The Customer class
# The Customer class represents a customer who will order from the stalls.
class Customer: 
    # Constructor
    def __init__(self, name, wallet = 100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    def reload_money(self,deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases   
    def validate_order(self, cashier, stall, item_name, quantity):
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):  
            print("Our stall has run out of " + item_name + " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity): 
            print("Don't have enough money for that :( Please reload more money!")
        else:
            bill = cashier.place_order(stall, item_name, quantity) 
            self.submit_order(cashier, stall, bill) 
    
    # Submit_order takes a cashier, a stall and an amount as parameters, 
    # it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    #TO DO
    def submit_order(self, cashier, stall, amount): 
        self.wallet = self.wallet - amount
        cashier.receive_payment(stall, amount)
        #EXTRA CREDIT
        if cashier.lucky():
            self.wallet = self.wallet + 10

    # The __str__ method prints the customer's information.    
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."


# The Cashier class
# The Cashier class represents a cashier at the market. 
class Cashier:

    # Constructor
    def __init__(self, name, directory =[], orders = 0): #add list of customers for EC
        self.name = name
        self.directory = directory[:] # make a copy of the directory
        self.orders = orders #for extra credit

    #EXTRA CREDIT
    #for each 10th order, run lucky draw w 5% probability of customer getting $10
    def lucky(self):
        #keep track of order
        self.orders+=1

        #if it's the 10th
        if self.orders % 10 == 0:
            if random.randrange(0,20) == 1:
                #added in validate order customer gets 10 bucks if true
                return True
            else:
                return False
    

    # Whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money
        #FOR EXTRA CREDIT
        self.lucky()

    # Places an order at the stall.
	# The cashier pays the stall the cost.
	# The stall processes the order
	# Function returns cost of the order, using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        return stall.compute_cost(quantity) 
    
    # string function.
    def __str__(self):

        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

## Complete the Stall class here following the instructions in HW_4_instructions_rubric
#TO DO
class Stall:

    #initialize, defaults: cost - 7, earnings - 0
    def __init__(self, name, inventory, cost = 7, earnings = 0):
        self.name = name
        self.inventory = inventory.copy()
        self.cost = cost
        self.earnings = earnings

    def __str__(self):
        keyslist = str(self.inventory.keys())
        return("Hello, we are " + self.name + ". This is the current menu " + keyslist + ". We charge $" + str(self.cost) + 
                " per item. We have $" + str(self.earnings) + " in total.")

    #takes food name and quantity
    def process_order(self, name, quantity):
        #decrease quantity from stall's inventory
        self.inventory[name] = self.inventory[name] - quantity

    def has_item(self, name, quantity):
        #check if food is in the directory
        if name in self.inventory:
            #true if enough food is left
            if quantity <= self.inventory[name]:
                return True
        #otherwise return false
        return False

    def stock_up(self, name, quantity):
        #add quantity to existing quantity if item in dictionary
        if name in self.inventory:
            self.inventory[name] = self.inventory[name] + quantity
        else:
            #create new item in dictionary
            self.inventory[name] = quantity

    def compute_cost(self, quantity):
        #return total for order
        return quantity * self.cost



class TestAllMethods(unittest.TestCase):
    
    def setUp(self):
        inventory = {"Burger":40, "Taco":50}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Stall("The Grill Queen", inventory, cost = 10)
        self.s2 = Stall("Tamale Train", inventory, cost = 9)
        self.s3 = Stall("The Streatery", inventory) #default cost = 7
        self.c1 = Cashier("West")
        self.c2 = Cashier("East")
        #the following codes show that the two cashiers have the same directory
        for c in [self.c1, self.c2]:
            for s in [self.s1,self.s2,self.s3]:
                c.add_stall(s)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

	## Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3) 

	## Check to see whether constructors work
    def test_stall_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

		# Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})
        
    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_custormer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings
        
        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_custormer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)


	# Check to see that the server can serve from the different stalls
    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1))
        self.assertFalse(c3.has_stall(self.s3)) 
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)


	# Test that computed cost works properly.
    def test_compute_cost(self):
        #what's wrong with the following statements?
        #can you correct them? DONE
        self.assertEqual(self.s1.compute_cost(5), 50) #ISSUE: cost should be 50 (5*10), not 51
        self.assertEqual(self.s3.compute_cost(6), 42) #ISSUE: cost should be 42 (7*6), not 45

	# Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases
        i1 = {"Pizza":35, "Salad":70, "Pasta":12}
        i2 = {"Bread":89, "Sandwich":18, "Quesadilla":63, "Rice":109}

        s1 = Stall("Italian", i1, 12)
        s2 = Stall("Carb City", i2, 8)

        # Test to see if has_item returns True when a stall has enough items left
        # Please follow the instructions below to create three different kinds of test cases 
        # Test case 1: the stall does not have this food item:
        self.assertFalse(s1.has_item("Bread", 1)) 
        
        # Test case 2: the stall does not have enough food item: 
        self.assertFalse(s2.has_item("Sandwich", 23)) 

        # Test case 3: the stall has the food item of the certain quantity: 
        self.assertTrue(s1.has_item("Pizza", 35)) 
        self.assertTrue(s2.has_item("Rice", 20)) 

	# Test validate order
    def test_validate_order(self):
        #set up
        i1 = {"Pizza":35, "Salad":70, "Pasta":12}
        i2 = {"Bread":89, "Sandwich":18, "Quesadilla":63, "Rice":109}

        huda = Customer("Huda") #default wallet = 100
        mike = Customer("Mike", 703)
        helen = Customer("Helen", 89)
        ann = Customer("Ann", 35)

        s1 = Stall("Italian", i1, 12)
        s2 = Stall("Carb City", i2, 8)

        c1 = Cashier("Tyler", [s1])
        c2 = Cashier("Frankie", [s2])

		#start testing
        #new line for easy comparison
        print('\n')
        # case 1: test if a customer doesn't have enough money in their wallet to order
        annbefore = ann.wallet
        ann.validate_order(c2, s2, "Rice", 5)
        print("EXPECTED: Don't have enough money for that :( Please reload more money!\n")
        #assert equal by seeing if the order went through with wallet
        self.assertEqual(annbefore, ann.wallet)

		# case 2: test if the stall doesn't have enough food left in stock
        helenbefore = helen.wallet
        helen.validate_order(c1, s1, "Pasta", 13)
        print("EXPECTED: Our stall has run out of Pasta :( Please try a different stall!\n")
        #assert equal by seeing if the order went through with wallet
        self.assertEqual(helenbefore, helen.wallet)

		# case 3: check if the cashier can order item from that stall
        hudabefore = huda.wallet
        huda.validate_order(c2, s2, "Quesadilla", 3)
        #assert equal by seeing if the order went through with wallet
        self.assertNotEqual(hudabefore, huda.wallet)

        # case 4: test when the stall doesn't have the item
        mikebefore = mike.wallet
        mike.validate_order(c1, s2, "Bread", 2)
        print("EXPECTED: Sorry, we don't have that vendor stall. Please try a different one. \n")
        #assert equal by seeing if the order went through with wallet
        self.assertEqual(mikebefore, mike.wallet)

    # Test if a customer can add money to their wallet
    def test_reload_money(self):
        #set up
        huda = Customer("Huda") #default wallet = 100
        mike = Customer("Mike", 703)
        helen = Customer("Helen", 10)
        ann = Customer("Ann", 0)

        #reload default wallet
        huda.reload_money(10)
        self.assertEqual(huda.wallet, (100 + 10))

        #relaod wallet with unique nonzero amount
        mike.reload_money(89)
        self.assertEqual(mike.wallet, (703 + 89))

        #reload wallet but value is 0
        helen.reload_money(0)
        self.assertEqual(helen.wallet, (0 + 10))

        #reload wallet that starts with nothing
        ann.reload_money(320)
        self.assertEqual(ann.wallet, (0 + 320))
    
### Write main function
def main():
    #Create different objects

    #at least 2 dictionaries w 3 types of food (food name and quantity) 
    i1 = {"Pizza":35, "Salad":70, "Pasta":12}
    i2 = {"Bread":89, "Sandwich":18, "Quesadilla":63, "Rice":109}

    #3 customer objects unique name and wallet amount
    huda = Customer("Huda") #default wallet = 100
    mike = Customer("Mike", 703)
    helen = Customer("Helen", 89)
    ann = Customer("Ann", 35)

    #2 stall objects w/ unique name and cost. use created inventories
    s1 = Stall("Italian", i1, 12)
    s2 = Stall("Carb City", i2, 8)

    #2 cashier objects w/ unique name and directory
    c1 = Cashier("Tyler", [s1])
    c2 = Cashier("Frankie", [s2])

    #Try all cases in the validate_order function
    #Below you need to have *each customer instance* try the four cases
    #case 1: the cashier does not have the stall 
    mike.validate_order(c1, s2, "Bread", 2)
    print("EXPECTED: Sorry, we don't have that vendor stall. Please try a different one. \n")
    
    #case 2: the casher has the stall, but not enough ordered food or the ordered food item
    helen.validate_order(c2, s2, "Salad", 2)
    print("EXPECTED: Our stall has run out of Salad :( Please try a different stall!\n")
    helen.validate_order(c1, s1, "Pasta", 13)
    print("EXPECTED: Our stall has run out of Pasta :( Please try a different stall!\n")
    
    #case 3: the customer does not have enough money to pay for the order:
    ann.validate_order(c2, s2, "Rice", 5)
    print("EXPECTED: Don't have enough money for that :( Please reload more money!\n") 
    
    #case 4: the customer successfully places an order
    huda.validate_order(c2, s2, "Quesadilla", 3) 


if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)
