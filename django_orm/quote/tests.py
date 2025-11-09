from django.test import TestCase
from django_orm.quote import models
import pytest

QUOTES = (
    (
        "I'm sorry, Dave. I'm afraid I can't do that.",
        "HAL, 2001: A Space Odyssey",
    ),
    (
        "Greetings, programs!",
        "Flynn, TRON",
    ),
    (
        "Try not. Do, or do not. There is no try.",
        "Yoda, The Empire Strikes Back",
    ),
)
class TestQuote(TestCase):
    def setUp(self):
        self.quotes = [models.Quote.objects.create(text=text, 
                source=source).id for text, source in QUOTES ]
        return super().setUp()

    @pytest.mark.django_db
    def test_quote_of_the_day_first(self):
        q1, q2, q3 = self.quotes

        seven_first_ones = [
            models.Quote.of_the_day(key=lambda _: 0).id  # всегда берём первую
            for _ in range(7)
            ]
        assert seven_first_ones == [q1, q2, q3, q1, q2, q3, q1]
    
    @pytest.mark.django_db
    def test_quote_of_the_day_single(self):
        # цитата всего одна
        quote = models.Quote.objects.create(text="?", source="?").id

        always_the_same = [
            models.Quote.of_the_day().id  # берём случайную
            for _ in range(10)
        ]
        assert always_the_same == [quote] * 10
    
    @pytest.mark.django_db
    def test_quote_of_the_day_random(self):
        q1, q2, q3 = self.quotes

        three_random_quotes = {models.Quote.of_the_day().id for _ in range(3)}
        # если из n цитат случайно выбрать n без повторов,
        # то каждая из этих n цитат должна быть выбрана
        assert three_random_quotes == {q1, q2, q3}
