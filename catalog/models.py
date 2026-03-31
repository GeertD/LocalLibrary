import uuid

from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

class Genre(models.Model):
    """
    Model for a book genre.
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry, etc.)"
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("genre-detail", args=[str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message="Genre already exists (case insensitive match)"
            ),
        ]


class Author(models.Model):
    """Model for an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(verbose_name="Died", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    
    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])


class Language(models.Model):
    """Model for a language."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Book(models.Model):
    """
    Model for a book (but not a specific copy).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(to=Author, on_delete=models.RESTRICT, null=True)
    summary = models.TextField(
        max_length=1000,
        help_text="Enter a brief description of the book"
        )
    isbn = models.CharField(
        verbose_name="ISBN", 
        max_length=13,
        unique=True,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>'
        )
    genre = models.ManyToManyField(
        to=Genre,
        help_text="Select a genre for this book.")
    language = models.ForeignKey(to=Language, on_delete=models.RESTRICT, null=False)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])
    
    def display_genre(self):
        """Create a string for the genre. Required to display genre in admin."""
        return ", ".join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = "Genre"
    

class BookInstance(models.Model):
    """
    Model for a specific copy of a book.
    """
    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this book instance across the whole library"        
    )
    book = models.ForeignKey(to=Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availability",
    )
    
    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f"{self.id} {self.book.title}"

    
