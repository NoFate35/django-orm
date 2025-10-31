from django.test import TestCase

import django.db
import pytest
from django_orm.blog import models

#from .models import User, Tag, Post, PostComment, PostLike

@pytest.mark.django_db
class FooTest(TestCase):
    def test_clip_rates_for(self):
        new_one = models.Clip.objects.create(title="The lazy cat")
        assert models.Clip.rates_for(new_one.title) == [(0, 0)]

        dogs = models.Clip.objects.create(title="Funny dogs")
        for _ in range(12):
            dogs.like()
        for _ in range(4):
            dogs.dislike()
        assert models.Clip.rates_for(dogs.title) == [(12, 4)]

        cats = models.Clip.objects.create(title="Funny cats")
        for _ in range(10):
            cats.like()
        for _ in range(7):
            cats.dislike()
        assert models.Clip.rates_for(cats.title) == [(10, 7)]

        titles = [dogs.title, cats.title]
        assert models.Clip.rates_for(*titles) == [(10, 7), (12, 4)]
