from django.db import models
from django.db.models import F, Sum


class ShoppingCart(models.Model):
    def preview(self):
        # BEGIN (write your solution here)
        positions = total_price = self.positions.annotate(positional_price=F('item__price') * F('quantity')).order_by('-positional_price').values_list('item__name', 'quantity')
        return positions

    def add(self, item, quantity=1):
        # BEGIN (write your solution here)
        ShoppingCartPosition.objects.create(cart=self, item=item, quantity=quantity)
        # END

    @property
    def total_price(self):
        # BEGIN (write your solution here)
        total_price = self.positions.annotate(positional_price=F('item__price') * F('quantity')).aggregate(Sum('positional_price'))
        return total_price['positional_price__sum']     
        # END


class ShopItem(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class ShoppingCartPosition(models.Model):
    # BEGIN (write your solution here)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='positions')
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["cart", "item"], name="unique_item")]
    
    PRICE = F("positions__price") * F("quantity")
    # END

