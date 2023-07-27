import random
import string
import uuid

from backend.tests.functional.models.models import Bookmarks, Like, Reviews
from backend.tests.functional.testdata import counter, films


class GeneratorMongo:
    counter: int = counter

    def harvest(self):
        yield from self._generate_data()

    @staticmethod
    def _gen_user():
        return str(uuid.uuid4())

    @staticmethod
    def _gen_film():
        for film_id in films:
            yield film_id['film_id']

    @staticmethod
    def _gen_text():
        length = random.randint(50, 100)
        characters = string.ascii_letters + string.digits + string.punctuation
        return "".join(random.choice(characters) for _ in range(length))

    def _generate_data(self):
        yield from self._gen_like()
        yield from self._gen_review()
        yield from self._gen_bookmarks()

    def _gen_like(self):
        for film_id in self._gen_film():
            yield [
                Like(
                    user_id=self._gen_user(),
                    film_id=film_id,
                    value=0,
                )
                for _ in range(self.counter)
            ]
            yield [
                Like(
                    user_id=self._gen_user(),
                    film_id=film_id,
                    value=1,
                )
                for _ in range(self.counter)
            ]

    def _gen_review(self):
        for film_id in self._gen_film():
            yield [
                Reviews(
                    user_id=self._gen_user(),
                    film_id=film_id,
                    review=self._gen_text(),
                )
                for _ in range(self.counter)
            ]

    def _gen_bookmarks(self):
        yield [
            Bookmarks(
                user_id=self._gen_user(),
                film_id=film_id
            )
            for film_id in self._gen_film()
        ]
