import logging
import random
import string
import uuid

from storage_research.models.models import Bookmarks, Like, Reviews

log = logging.getLogger(__name__)


class Generator:
    counter: int = 0

    def harvest(self):
        while True:
            yield from self._generate_data()

    @staticmethod
    def _gen_user():
        return uuid.uuid4()

    @staticmethod
    def _gen_film():
        return uuid.uuid4()

    @staticmethod
    def _gen_text():
        length = random.randint(50, 100)
        characters = string.ascii_letters + string.digits + string.punctuation
        return "".join(random.choice(characters) for _ in range(length))

    @staticmethod
    def _gen_rating():
        return random.randint(1, 10)

    def random_butch(self):
        random_num = random.random()
        if random_num <= 0.5:
            self.counter += 1
            return 1
        else:
            random_num = random.randint(2, 100)
            self.counter += random_num
            return random_num

    def _generate_data(self):
        while True:
            yield self._gen_like()
            yield self._gen_review()
            yield self._gen_bookmarks()

    def _gen_like(self):
        return [
            Like(
                user_id=self._gen_user(),
                film_id=self._gen_film(),
                value=self._gen_rating(),
            )
            for _ in range(self.random_butch())
        ]

    def _gen_review(self):
        return [
            Reviews(
                user_id=self._gen_user(),
                film_id=self._gen_film(),
                review=self._gen_text(),
            )
            for _ in range(self.random_butch())
        ]

    def _gen_bookmarks(self):
        return [
            Bookmarks(user_id=self._gen_user(), film_id=self._gen_film())
            for _ in range(self.random_butch())
        ]
