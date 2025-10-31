from django.db import models
'''

class TimestampedModel(models.Model):
    """An abstract model with a pair of timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(TimestampedModel):
    name = models.CharField(max_length=30)


class Post(TimestampedModel):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=300)
    tags = models.ManyToManyField(Tag)
    views = models.DecimalField(max_digits=10, decimal_places=2)
    '''
from django.db import models
from django.db.models import Count


class Clip(models.Model):
    title = models.CharField(max_length=200)

    def like(self):
        ClipLike.objects.create(clip=self)

    def dislike(self):
        ClipDislike.objects.create(clip=self)

    @classmethod
    def rates_for(cls, *args):
        """
        Returns a tuple of integers (likes, dislikes)
        for the clip(s) filtered by provided args.
        """
        # BEGIN (write your solution here)
        clips = cls.objects.filter(title__in=args).annotate(likes=Count('cliplike', distinct=True),
                                                            dislikes=Count('clipdislike', distinct=True)).order_by("title")
        return list(clips.values_list('likes', 'dislikes'))
        # END


# Обычно используют одну модель как для положительных реакций,
# так и для отрицательных. Однако в рамках этого упражнения
# две отдельные модели использовать удобнее. В реальных проектах
# такое тоже встречается, когда некое явление пользователю
# позволено оценить одновременно и положительно, и отрицательно.
class ClipLike(models.Model):
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE)


class ClipDislike(models.Model):
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE)