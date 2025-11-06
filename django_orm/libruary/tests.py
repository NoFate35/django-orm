from django.test import TestCase

import pytest

from django_orm.libruary.models import Author, Book, Borrow, Genre, Review, User

"""
@pytest.fixture
def author():
    return Author.objects.create(name="Лев Толстой", country="Россия")


@pytest.fixture
def genre():
    return Genre.objects.create(name="Роман")


@pytest.fixture
def user():
    return User.objects.create(name="Иван Петров")


@pytest.fixture
def book(author, genre):
    book = Book.objects.create(title="Война и мир", author=author, copies_available=2)
    book.genres.add(genre)
    return book
"""


class StudentsTest(TestCase):
	
    def setUp(self):
        self.author = Author.objects.create(name="Лев Толстой", country="Россия")
        self.genre = Genre.objects.create(name="Роман")
        self.book = Book.objects.create(title="Война и мир", author=self.author, copies_available=2)
        self.book.genres.add(self.genre)
        self.user = User.objects.create(name="Иван Петров")
	
    @pytest.mark.django_db
    def test_get_available_books(self):
        # Проверяем, что книга появляется в списке доступных
        available_books = Book.get_available_books()
        assert self.book in available_books

        # Делаем книгу недоступной и проверяем
        self.book.copies_available = 0
        self.book.save()
        available_books = Book.get_available_books()
        assert self.book not in available_books


    @pytest.mark.django_db
    def test_borrow_book(self):
        initial_copies = self.book.copies_available
        self.book.borrow(self.user)

        # Проверяем уменьшение количества копий
        self.book.refresh_from_db()
        assert self.book.copies_available == initial_copies - 1

        # Проверяем создание записи о заимствовании
        assert Borrow.objects.filter(book=self.book, user=self.user).exists()


    @pytest.mark.django_db
    def test_borrow_book_no_copies(self):
        self.book.copies_available = 0
        self.book.save()

        # Проверяем, что возникает ошибка при попытке взять книгу
        with pytest.raises(ValueError, match="No copies available"):
            self.book.borrow(self.user)


    @pytest.mark.django_db
    def test_get_popular_books(self):
        # Создаем дополнительную книгу
        second_book = Book.objects.create(
            title="Анна Каренина", author=self.book.author, copies_available=1
        )

        # Берем первую книгу дважды
        self.book.borrow(self.user)
        self.book.borrow(User.objects.create(name="Петр Иванов"))

        # Берем вторую книгу один раз
        second_book.borrow(self.user)

        popular_books = Book.get_popular_books()
        assert popular_books[0] == self.book
        assert popular_books[1] == second_book


    @pytest.mark.django_db
    def test_get_top_rated_books(self):
        second_book = Book.objects.create(
            title="Вторая книга", author=self.book.author, copies_available=1
        )

        Review.objects.create(book=self.book, rating=5)
        Review.objects.create(book=self.book, rating=4)
        Review.objects.create(book=self.book, rating=3)

        Review.objects.create(book=second_book, rating=5)
        Review.objects.create(book=second_book, rating=5)

        top_books = Review.get_top_rated_books(min_reviews=3, limit=1)

        # Проверяем, что вернулась первая книга (у второй мало отзывов)
        assert len(top_books) == 1
        assert top_books[0] == self.book
        assert top_books[0].avg_rating == 4.0


    @pytest.mark.django_db
    def test_get_top_genres(self):
        # Создаем дополнительный жанр и книгу
        second_genre = Genre.objects.create(name="Поэзия")
        second_book = Book.objects.create(
            title="Стихотворения", author=self.book.author, copies_available=1
        )
        second_book.genres.add(second_genre)

        # Создаем заимствования
        self.book.borrow(self.user)
        self.book.borrow(User.objects.create(name="Петр Иванов"))
        second_book.borrow(self.user)

        top_genres = Genre.get_top_genres()
        assert top_genres[0] == self.genre
        assert top_genres[1] == second_genre


    @pytest.mark.django_db
    def test_get_author_borrow_stats(self):
        # Создаем заимствования
        self.book.borrow(self.user)
        self.book.borrow(User.objects.create(name="Петр Иванов"))

        author_stats = Author.get_author_borrow_stats()

        author_borrows = author_stats.get(id=self.book.author.id)
        assert author_borrows.total_borrows == 2
