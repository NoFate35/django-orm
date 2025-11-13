from django.test import TestCase
from django_orm.shop import models
import django.db

import pytest

class TestShop(TestCase):
    def setUp(self):
        self.cart = models.ShoppingCart.objects.create()
        self.apple = models.ShopItem.objects.create(name="apple", price=2.0)
        self.pear = models.ShopItem.objects.create(name="pear", price=3.0)
        return super().setUp()

    @pytest.mark.django_db
    def test_shoppingcart_add(self):
        self.cart.add(self.apple, 5)
        assert models.ShoppingCartPosition.objects.count() == 1
        with pytest.raises(django.db.IntegrityError):
            self.cart.add(self.apple, 3)  # повторное добавление не должно быть возможно!


    @pytest.mark.django_db
    def test_shoppingcart_preview(self):
        napkin = models.ShopItem.objects.create(name="napkin", price=0.1)
        self.cart.add(self.apple, 2)
        self.cart.add(self.pear)
        self.cart.add(napkin, 100)
        assert list(self.cart.preview()) == [
            ("napkin", 100),
            ("apple", 2),
            ("pear", 1),
        ]


    @pytest.mark.django_db
    def test_shoppingcart_total_price(self):
        self.cart.add(self.apple, 17)
        self.cart.add(self.pear, 23)
        assert self.cart.total_price == self.apple.price * 17 + self.pear.price * 23

