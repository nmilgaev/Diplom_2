import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_user_data(email_suffix="@example.com"):
    email = f"{generate_random_string(10)}{email_suffix}"
    password = generate_random_string(12)
    name = generate_random_string(8)
    return {"email": email, "password": password, "name": name}
