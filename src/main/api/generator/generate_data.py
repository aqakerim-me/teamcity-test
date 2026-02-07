import random
import string
from faker import Faker

faker = Faker()


class GenerateData:

    @staticmethod
    def get_project_name() -> str:
        words = faker.words(nb=random.randint(1, 3))
        return " ".join(words).title()

    @staticmethod
    def get_project_id() -> str:
        first_char = random.choice(string.ascii_letters)
        allowed_chars = string.ascii_letters + string.digits + "_"
        rest = "".join(
            random.choices(allowed_chars, k=random.randint(2, 15))
        )
        return first_char + rest

    @staticmethod
    def get_project_id_with_length(length: int) -> str:
        first_char = random.choice(string.ascii_letters)
        allowed_chars = string.ascii_letters + string.digits + "_"

        if length == 1:
            return first_char

        rest = "".join(random.choices(allowed_chars, k=length - 1))
        return first_char + rest

    @staticmethod
    def get_username() -> str:
        min_length = 1
        max_length = 20
        length = random.randint(min_length, max_length)

        allowed_chars = (
            string.ascii_letters +
            string.digits +
            "._-"
        )
        return "".join(random.choices(allowed_chars, k=length))

    @staticmethod
    def get_username_with_length(length: int) -> str:
        if length < 1:
            raise ValueError("Username length must be >= 1")

        allowed_chars = (
                string.ascii_letters +
                string.digits +
                "._-"
        )
        return "".join(random.choices(allowed_chars, k=length))

    @staticmethod
    def get_password() -> str:
        min_length = 1
        max_length = 20
        length = random.randint(min_length, max_length)

        allowed_chars = (
                string.ascii_letters +
                string.digits +
                string.punctuation
        )
        return "".join(random.choices(allowed_chars, k=length))