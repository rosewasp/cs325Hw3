# Author: Abhash Sharma
# Course: CS 325, Fall 2020
# HW 3, #4c

# import file "shopping.txt"
# get appropriate data to carry out knapsack function


def get_int_clear_line(file_name):
    """processes a text file, clears that line, and returns the number on that line"""
    return int(file_name.readline().strip())

def fill_price_weight_dict(number, file_name):
    """return a dictionary of price:weight for all items in a case"""
    # dictionary to store item by price:weight
    item_dict = {}
    # iterate through file getting price and weight for each item
    for i in range(number):
        # map functions applies int to each line item and maps to P and W
        P, W = map(int, file_name.readline().strip().split())
        # store P:W in dictionary
        item_dict[P] = [W]
    return item_dict

def family_weight_list(size, file_name):
    """returns a list of max weight cap for each family member"""
    # array to store weight cap
    per_person_weight_cap = []
    # iterate through next lines and add to weight list
    for i in range(size):
        per_person_weight_cap.append(get_int_clear_line(file_name))
    return per_person_weight_cap

# Citation: solution based on:
# https://www.geeksforgeeks.org/python-program-for-dynamic-programming-set-10-0-1-knapsack-problem/
def shopping_knapsack(weight_cap, price_weight_dict):
    """returns the maximum price of items in a knapsack"""
    # extract necessary value from price_weight_dict
    price_array = []
    weight_array = []
    for x in price_weight_dict:
        price_array.append(x)
        weight_array.append(price_weight_dict[x][0])
    n = len(price_array)
    # array to store item list
    item_list = []

    # initialize a knapsack table
    # creates a dictionary with weight as columns and items as rows
    # +1 because index from 0 to n-1
    knap_table = [[0 for x in range(weight_cap + 1)] for x in range(n + 1)]

    # add max price in knap_table
    for i in range(n+1):  # iterate through every row
        for w in range(weight_cap+1):  # consider every column in row
            if i == 0 or w == 0:  # when no item or no weight
                knap_table[i][w] = 0
            elif weight_array[i-1] <= w:  # consider price if weight fits knapsack
                if price_array[i-1] + knap_table[i-1][w-weight_array[i-1]] > knap_table[i-1][w]:
                    knap_table[i][w] = price_array[i-1] + knap_table[i-1][w-weight_array[i-1]]
                else:
                    knap_table[i][w] = knap_table[i-1][w]
            else:
                knap_table[i][w] = knap_table[i-1][w]

    total_price_new = knap_table[n][weight_cap]

    # array to store list of items selected by one family member
    item_list = []

    # Citation: solution based on:
    # https://www.geeksforgeeks.org/printing-items-01-knapsack/

    temp_max = total_price_new
    temp_cap = weight_cap
    # iterate from 1 to n, including 1 and n
    for k in range(n, 0, -1):
        # when no item selected
        if temp_max <= 0:
            break
        if temp_max == knap_table[k - 1][temp_cap]:
            continue
        else:
            item_list.append(k)
            temp_max -= price_array[k-1]
            temp_cap -= weight_array[k-1]

    return {total_price_new: item_list}


with open('shopping.txt', 'r') as infile:
    # Part 1: processing file to extract necessary data from file
    # get the total cases in text file
    total_cases = get_int_clear_line(infile)

    # iterate thorough total cases
    # for each case separate each given value into appropriate array
    # 1. total items 2. price-weight combo 3. family size 4. weight cap per  family member
    for l in range(total_cases):
        # initialize arrays
        # each new case will have a new set of data points
        # the next line in file is the number of items for each case
        total_items = get_int_clear_line(infile)
        # a dictionary with Price:Weight
        potential_items = fill_price_weight_dict(total_items, infile)

        # get the next line in file, which is the number of people in family
        family_size = get_int_clear_line(infile)

        # put the next lines in weight array
        max_weight_per = family_weight_list(family_size, infile)

        # variable where total price for family is stored
        family_value = 0

        # item dictionary per member
        member_items = []

        # iterate through each max weight and get max price and item number for each member
        # for family of more than one, total price is calculated at the end, before printing in file
        for w in max_weight_per:
            # call to shopping_knapsack returns maximum price for each member
            # has max price per member and items per member
            new_data = shopping_knapsack(w, potential_items)
            for x in new_data:
                new_max = x
                member_items.append(new_data[x])
            # add up max price for each family member to get total price
            family_value += new_max

        with open('results.txt', 'a') as outfile:
        # write results to file
        # print("Test Case: ", l+1)
            outfile.write("Test Case %d\n" % (l + 1))
        # print("Total Price: ", family_value)
            outfile.write("Total Price %d\n" % family_value)
        # print("Member Items")
        # for i in range(len(member_items)):
            # member_items[i].sort()
            # print(i+1, ": ", member_items[i])
            outfile.write("Member Items\n")
            for i in range(len(member_items)):
                member_items[i].sort()
            # citation:
            # https://stackoverflow.com/questions/4288973/whats-the-difference-between-s-and-d-in-python-string-formatting
                outfile.write("%d: %s\n" % (i + 1, " ".join(map(str, member_items[i]))))
            outfile.write('\n')
        outfile.close()
