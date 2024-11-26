BASE_URL = "https://stellarburgers.nomoreparties.site/api"

ENDPOINTS = {
    "register_user": f"{BASE_URL}/auth/register",
    "login": f"{BASE_URL}/auth/login",
    "logout": f"{BASE_URL}/auth/logout",
    "token": f"{BASE_URL}/auth/token",
    "user": f"{BASE_URL}/auth/user",
    "orders": f"{BASE_URL}/orders"
}

EXISTING_USER = {
    "email": "nmilgaevaaa@gmail.com",
    "password": "glwgWgkw3gk3",
    "name": "NikitaMilgaev"
}

MISSING_FIELDS_USER = {
    "email": "missing-fields@google.com",
    "password": "",
    "name": "MissingFields"
}

INVALID_USER = {
    "email": "invalid_user@example.com",
    "password": "wrong_password"
}

INGREDIENTS = [
    "61c0c5a71d1f82001bdaaa6d",  # Флюоресцентная булка R2-D3
    "61c0c5a71d1f82001bdaaa6f",  # Мясо бессмертных моллюсков Protostomia
    "61c0c5a71d1f82001bdaaa70",  # Говяжий метеорит (отбивная)
    "61c0c5a71d1f82001bdaaa71",  # Биокотлета из марсианской Магнолии
]
