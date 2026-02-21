import random
import string
import time
from faker import Faker

faker = Faker()


class GenerateData:

    @staticmethod
    def get_project_name() -> str:
        words = faker.words(nb=random.randint(1, 3))
        return " ".join(words).title()

    @staticmethod
    def get_project_id() -> str:
        # Use timestamp + random to ensure uniqueness
        timestamp_suffix = str(int(time.time() * 1000))[-6:]  # Last 6 digits of ms timestamp
        first_char = random.choice(string.ascii_letters)
        allowed_chars = string.ascii_letters + string.digits + "_"
        rest = "".join(
            random.choices(allowed_chars, k=random.randint(4, 8))
        )
        return first_char + rest + timestamp_suffix

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
    
    @staticmethod
    def get_step_id() -> str:
        return "step_" + "".join(random.choices(string.ascii_letters + string.digits, k=8))
    
    @staticmethod
    def get_build_type_id() -> str:
        return "buildType_" + "".join(random.choices(string.ascii_letters + string.digits, k=8))

    @staticmethod
    def get_build_type_name() -> str:
        words = faker.words(nb=random.randint(2, 4))
        return "_".join(words).title()

    @staticmethod
    def get_build_parameter_name() -> str:
        prefix = random.choice(["env.", "system.", "config."])
        name = "".join(
            random.choices(string.ascii_uppercase, k=random.randint(3, 8))
        )
        return f"{prefix}{name}"

    @staticmethod
    def get_build_parameter_value() -> str:
        length = random.randint(5, 50)
        allowed_chars = string.ascii_letters + string.digits + "_-."
        return "".join(random.choices(allowed_chars, k=length))

