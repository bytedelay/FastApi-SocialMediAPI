from passlib.context import CryptContext

crypt_pass = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hasher(password: str):
    return crypt_pass.hash(password)

def verifyhash(user_attempted_password, hashed_password):
    return crypt_pass.verify(user_attempted_password,hashed_password) #checks the password validity

    