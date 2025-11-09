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
        if all(quote.approved for quote in cls.objects.all()):
            cls.objects.update(approved=False)
        not_approved = cls.objects.filter(approved=False)
        randon_num = key(not_approved.count())
        random_quote = not_approved[randon_num]
        random_quote.approved = True
        random_quote.save(update_fields=['approved'])
        return random_quote
    
        '''        
        less_shown = cls.objects.filter(
            shows=cls.objects.order_by('shows')[0].shows,
        ).order_by('id')
        quote = less_shown[key(less_shown.count())]
        quote.shows += 1
        quote.save()
        return quote
        '''
        # END