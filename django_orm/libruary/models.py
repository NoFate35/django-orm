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
    
# END


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genres = models.ManyToManyField(Genre, related_name="books")
    copies_available = models.PositiveIntegerField(default=1)
    # BEGIN (write your solution here)
    @classmethod
    def get_available_books(self):
    	return Book.objects.filter(copies_available__gt=0)

    @classmethod
    def borrow(self, user):
    	from django.db import transaction
    	with transaction.atomic():
    		print("self", self, "user", user, "self.copies_available", self.title)
    
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
