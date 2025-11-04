from django.test import TestCase

import pytest

from django_orm.libruary.models import Author, Book, Borrow, Genre, Review, User


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



class StudentsTest(TestCase):
    @pytest.mark.django_db
    def test_get_available_books(self, book):
        # Проверяем, что книга появляется в списке доступных
        available_books = Book.get_available_books()
        assert book in available_books

        # Делаем книгу недоступной и проверяем
        book.copies_available = 0
        book.save()
        available_books = Book.get_available_books()
        assert book not in available_books


    @pytest.mark.django_db
    def test_borrow_book(self, book, user):
        initial_copies = book.copies_available
        book.borrow(user)

        # Проверяем уменьшение количества копий
        book.refresh_from_db()
        assert book.copies_available == initial_copies - 1

        # Проверяем создание записи о заимствовании
        assert Borrow.objects.filter(book=book, user=user).exists()


    @pytest.mark.django_db
    def test_borrow_book_no_copies(self, book, user):
        book.copies_available = 0
        book.save()

        # Проверяем, что возникает ошибка при попытке взять книгу
        with pytest.raises(ValueError, match="No copies available"):
            book.borrow(user)


    @pytest.mark.django_db
    def test_get_popular_books(self, book, user):
        # Создаем дополнительную книгу
        second_book = Book.objects.create(
            title="Анна Каренина", author=book.author, copies_available=1
        )

        # Берем первую книгу дважды
        book.borrow(user)
        book.borrow(User.objects.create(name="Петр Иванов"))

        # Берем вторую книгу один раз
        second_book.borrow(user)

        popular_books = Book.get_popular_books()
        assert popular_books[0] == book
        assert popular_books[1] == second_book


    @pytest.mark.django_db
    def test_get_top_rated_books(self, book):
        second_book = Book.objects.create(
            title="Вторая книга", author=book.author, copies_available=1
        )

        Review.objects.create(book=book, rating=5)
        Review.objects.create(book=book, rating=4)
        Review.objects.create(book=book, rating=3)

        Review.objects.create(book=second_book, rating=5)
        Review.objects.create(book=second_book, rating=5)

        top_books = Review.get_top_rated_books(min_reviews=3, limit=1)

        # Проверяем, что вернулась первая книга (у второй мало отзывов)
        assert len(top_books) == 1
        assert top_books[0] == book
        assert top_books[0].avg_rating == 4.0


    @pytest.mark.django_db
    def test_get_top_genres(self, book, genre, user):
        # Создаем дополнительный жанр и книгу
        second_genre = Genre.objects.create(name="Поэзия")
        second_book = Book.objects.create(
            title="Стихотворения", author=book.author, copies_available=1
        )
        second_book.genres.add(second_genre)

        # Создаем заимствования
        book.borrow(user)
        book.borrow(User.objects.create(name="Петр Иванов"))
        second_book.borrow(user)

        top_genres = Genre.get_top_genres()
        assert top_genres[0] == genre
        assert top_genres[1] == second_genre


    @pytest.mark.django_db
    def test_get_author_borrow_stats(self, book, user):
        # Создаем заимствования
        book.borrow(user)
        book.borrow(User.objects.create(name="Петр Иванов"))

        author_stats = Author.get_author_borrow_stats()

        author_borrows = author_stats.get(id=book.author.id)
        assert author_borrows.total_borrows == 2
