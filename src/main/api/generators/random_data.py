import random
from faker import Faker

faker = Faker()


class RandomData:
    @staticmethod
    def get_project_name(length: int = random.randint(3, 15)) -> str:
        return ''.join(faker.random_letters(length))