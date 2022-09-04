import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# sales = SHEET.worksheet('sales')
# data = sales.get_all_values()
# print(data)

def get_sales_data():
    """
    Get sales figure  from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter data here: ")
        # print(f"The Data provide is {data_str}")
        sales_data = data_str.split(",")
        
        if (validate_data(sales_data)):
            print("Data is valid!")
            break
    
    return sales_data
    


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raise ValueError if strings cannot be converted in to int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required,  you provide {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, Please try again.\n")
        return False
        
    return True

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relewant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet... \n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully \n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate  the surplus for each item type.

    The Surplus is defined as the sales figure subtracted from  the stuck
    -Positive surplis indicates waste.
    -Negative surplis indicates extra made when stock was sold out.
    """
    print("Calculating surplus data... \n")
    stock = SHEET.worksheet("stock").get_all_values()
    # pprint(stock.pop())
    # to get the last row from stock sheet
    stock_row = stock[-1]
    # print(f"stock row: {stock_row}")
    # print(f"sales row: {sales_row}")
    # we can change str to int here as well stock_row = [int(stock) for stock in stock_row]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus  = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data



def main():
    """
    Run all program function 
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data,"sales")
    calculate_surplus_data(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    # print(new_surplus_data)
    update_worksheet(new_surplus_data,"surplus")



print("Welcome to Love Sandwiches Data Automation")
main()