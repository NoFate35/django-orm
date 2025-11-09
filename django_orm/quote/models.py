import random
from django.db import models, transaction


def random_one(count):
    return random.randint(0, count - 1)


class Quote(models.Model):
    text = models.TextField()
    source = models.CharField(max_length=200)
    # BEGIN (write your solution here)
    approved = models.BooleanField(default=False)
    # END

    @classmethod
    @transaction.atomic
    def of_the_day(cls, key=random_one):
        # BEGIN (write your solution here)
        if all(quote.approved for quote in Quote.objects.all()):
            Quote.objects.update(approved=False)
        count = Quote.objects.filter(approved=False).count()
        print('yyyy', count)
        # END