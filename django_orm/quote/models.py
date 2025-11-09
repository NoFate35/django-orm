import random
from django.db import models, transaction


def random_one(count):
    return random.randint(0, count - 1)


class Quote(models.Model):
    text = models.TextField()
    source = models.CharField(max_length=200)
    # BEGIN (write your solution here)
    
    # END

    @classmethod
    @transaction.atomic
    def of_the_day(cls, key=random_one):
        # BEGIN (write your solution here)
        pass
        # END