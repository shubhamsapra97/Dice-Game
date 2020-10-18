if __name__ == "__main__":
    # Getting user input
    while True:
        try:
            N = int(input("Enter number of players "))
            M = int(input("Enter points to accumulate "))
        except ValueError:
            print("Sorry, I didn't understand that.\n")
            continue
        else:
            break