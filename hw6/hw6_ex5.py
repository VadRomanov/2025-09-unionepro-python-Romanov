import re

def is_login(value):
    if (re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._]{1,18}[a-zA-Z0-9]$', value)):
        if (re.search(r'\.{2,}|_{2,}|\._|_\.', value)):
            return False
        return True
    else:
        return False

if __name__ == '__main__':
    print(is_login('login_rf.login'))
