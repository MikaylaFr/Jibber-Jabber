# validate_username returns False if the username is not allowed
# otherwise, returns True

def validate_username(username):
    # lowercaseUN = username.lower()
    lowercaseUN = username
    print("username: ", username)
    if lowercaseUN == '':
        print('not a valid username')
        return False
    if "null" in lowercaseUN:
        print('not a valid username')
        return False
    if ' ' in lowercaseUN:
        print('not a valid username')
        return False
    