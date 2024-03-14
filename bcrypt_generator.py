import bcrypt
import secrets
import string


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for i in range(length))


def generate_bcrypt_hash(data):
    salt = bcrypt.gensalt()
    bcrypt_hash = bcrypt.hashpw(data.encode("utf-8"), salt)
    return bcrypt_hash.decode("utf-8")


# Generate a random string of 16 characters
random_string = generate_random_string(64)
bcrypt_hash = generate_bcrypt_hash(random_string)
print("Random String:", random_string)
print("Bcrypt Hash:", bcrypt_hash)
