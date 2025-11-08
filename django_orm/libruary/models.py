from django.db import models, transaction
from django.db.models import Avg, Count


class Author(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    # BEGIN (write your solution here)
    @classmethod
    def get_author_borrow_stats(self):
        return Author.objects.annotate(total_borrows = Count('books__borrows'))
# END


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # BEGIN (write your solution here)
    @classmethod
    def get_top_genres(self):
        return Genre.objects.annotate(
            count_books = Count('' \
            'books__borrows')).order_by('-count_books')[:3]
# END


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genres = models.ManyToManyField(Genre, related_name="books")
    copies_available = models.PositiveIntegerField(default=1)

    # BEGIN (write your solution here)
    @classmethod
    def get_available_books(self):
        return self.objects.filter(copies_available__gt=0)

    @transaction.atomic
    def borrow(cls, user):
        if cls.copies_available == 0:
            raise ValueError("No copies available")
        cls.copies_available -= 1
        cls.save(update_fields=['copies_available'])
        Borrow.objects.create(book=cls, user=user)

    @classmethod
    def get_popular_books(self):
        return self.objects.annotate(borrow_count = Count('borrows')).order_by('-borrow_count')
    # END 


class User(models.Model):
    name = models.CharField(max_length=100)
    borrowed_books = models.ManyToManyField(
        Book, through="Borrow", related_name="borrowers"
    )


class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrows")
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    # BEGIN (write your solution here)
    @classmethod
    def get_top_rated_books(self, min_reviews, limit):
        return (Book.objects.annotate(
            reviews_count = Count('reviews'), 
            avg_rating = Avg('reviews__rating')).filter(reviews_count__gte = min_reviews).order_by('-avg_rating')[:limit])        
    
# END
