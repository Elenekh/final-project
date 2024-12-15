import json

# Function to register a new user
def register(filename):
    # Load existing data from the file if it exists
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"usernames": [], "passwords": []}

    while True:
        # Prompt for user details
        username = input("Choose your username: ").strip()
        password = input("Choose your password: ").strip()

        # Ensure that the username is unique
        if username in data["usernames"]:
            print("Username already taken! Please choose a different username.")
        else:
            # Append the new user's details to the data
            data["usernames"].append(username)
            data["passwords"].append(password)

            # Save the updated data to the JSON file
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"Registration successful! Welcome, {username}!")
            break

# Function to login
def login(filename):
    # Load existing data from the file
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("No users found. Please register first.")
        return

    while True:
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        # Check if the username exists and if the password is correct
        if username in data["usernames"]:
            index = data["usernames"].index(username)
            if data["passwords"][index] == password:
                print(f"Welcome back, {username}!")
                break
            else:
                print("Incorrect password! Please try again.")
        else:
            print("Username not found! Please check and try again.")

# Main loop
def main():
    filename = "user_data.json"  # JSON file where user data will be stored

    while True:
        print("\n--- Welcome to the User Registration and Login System ---")
        account_ans = input("Choose an option: \na) Sign Up \nb) Login and Shop \nc) Quit\nYour choice: ").strip().lower()

        if account_ans == "a":
            register(filename)
        elif account_ans == "b":
            login(filename)
        elif account_ans == "c":
            print("Goodbye! Have a great day!")
            break
        else:
            print("Invalid option. Please choose a valid option from a, b, or c.")

if __name__ == "__main__":
    main()
