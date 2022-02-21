from os import getenv

db_uri = getenv("DATABASE_URI")
if db_uri is None:
    raise ValueError("DATABASE_URI is not set")

tortoise_config = {
    "connections": {"default": db_uri},
    "apps": {
        "main": {"models": ["models", "aerich.models"], "default_connection": "default"}
    },
}
