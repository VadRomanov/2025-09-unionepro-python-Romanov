def is_password_good(password) -> bool:
    if len(password) < 8:
        return False

    contains_digits = False
    contains_upper_letters = False
    contains_lower_letters = False

    for char in password:
        contains_digits = contains_digits or (char.isdigit())
        contains_upper_letters = contains_upper_letters or (char.isupper())
        contains_lower_letters = contains_lower_letters or (char.islower())
        if contains_digits and contains_upper_letters and contains_lower_letters:
            return True

    return False

if __name__ == '__main__':
    print(is_password_good('aabbCC11OP'))
    print(is_password_good('abC1pu'))
