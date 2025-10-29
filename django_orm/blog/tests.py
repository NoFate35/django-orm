from django.test import TestCase

import django.db
import pytest
from django_orm.blog import models

#from .models import User, Tag, Post, PostComment, PostLike

@pytest.mark.django_db
class FooTest(TestCase):
    def test_island_can_reach(self):
        sumatra = models.Island.objects.create(name="Sumatra")
        java = models.Island.objects.create(name="Java")
        ceylon = models.Island.objects.create(name="Ceylon")
        
        fortune = models.Ship.objects.create(name="Fortune")
        pearl = models.Ship.objects.create(name="Pearl")

        sumatra.ships.add(fortune, pearl)
        java.ships.add(fortune)
        ceylon.ships.add(pearl)

        assert sumatra.can_reach(java, by_ship=fortune)
        assert sumatra.can_reach(ceylon, by_ship=pearl)
        assert not sumatra.can_reach(java, by_ship=pearl)
        assert not sumatra.can_reach(ceylon, by_ship=fortune)
        assert not java.can_reach(ceylon, by_ship=pearl)
