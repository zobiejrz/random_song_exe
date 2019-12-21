from UpdateStatus import * as us

def TakeCommand():
    """
    Gets a user command and executes it
    """
    user_input = input(" >>> ")

    if user_input == "status":
        us.PrintOptions()
    elif user_input == "wotd":
        us.UpdateWOTD()
    elif user_input == "freq":
        pass
    elif user_input == "toggle":
        pass
    elif user_input == "tweet":
        pass
    elif user_input == "options":
        pass
    elif user_input == "quit":
        pass
    else:
        print( "\n'{}' isn't understood input. Type 'options' to see valid commands.\n".format(user_input) )
