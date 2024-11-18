from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(prompt, allow_default=False):
    while True:
        date_str = input(prompt).strip()
        if not date_str and allow_default:
            return datetime.now().strftime(date_format)  # Return today's date as string in correct format
        try:
            # Parse the string into a datetime object to validate it
            valid_date = datetime.strptime(date_str, date_format)
            # Return the date back as a string in the correct format
            return valid_date.strftime(date_format)
        except ValueError:
            print("Invalid date format. Please use 'dd-mm-yyyy'.")

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()
    

def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
    return get_category()

def get_description():
    return input("Enter a description (optional): ")