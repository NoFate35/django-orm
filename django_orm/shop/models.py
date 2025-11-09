from django.db import models


class ShoppingCart(models.Model):
    def preview(self):
        # BEGIN (write your solution here)
        pass
        # END

    def add(self, item, quantity=1):
        # BEGIN (write your solution here)
        pass
        # END

    @property
    def total_price(self):
        # BEGIN (write your solution here)
        pass        
        # END


class ShopItem(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class ShoppingCartPosition(models.Model):
    # BEGIN (write your solution here)
    pass
    # END

