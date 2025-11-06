from django.db import models, transaction
from django.db.models import Avg, Count


class Author(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    # BEGIN (write your solution here)
    
# END


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # BEGIN (write your solution here)
    def get_top_genres():
        genres = Genre.objects.prefetch_related('books').prefetch_related('borrows')
        print('gggenres', genres)
# END


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genres = models.ManyToManyField(Genre, related_name="books")
    copies_available = models.PositiveIntegerField(default=1)

    # BEGIN (write your solution here)
    def get_available_books():
        return Book.objects.filter(copies_available__gt=0)


    def borrow(cls, user):
        with transaction.atomic():
            try:
                Book.objects.filter(id=cls.id).update(copies_available=(cls.copies_available - 1))
            except:
                raise ValueError("No copies available")
            Borrow.objects.create(book=cls, user=user)


    def get_popular_books():
        return Book.objects.prefetch_related('borrows').annotate(borrow_count = Count('borrows')).order_by('-borrow_count')
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

    
# END
