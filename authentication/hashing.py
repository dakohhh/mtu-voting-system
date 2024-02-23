import bcrypt


def hashPassword(password:str):
    result = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    return result.decode("utf8")


def checkPassword(user_input_password:str, password:str):
    result  = bcrypt.checkpw(user_input_password.encode(), password.encode())
    return result
