from django.db import models
import uuid

# Create your models here.
class Genre(models.Model):
    """Model represents a book genre"""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object"""
        return self.name

class Book(models.Model):
    """Model represents a book, but not a specific copy of a book"""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author but authors
    # can have many books-- This is not true for multiple author books
    # so I am changing it to ManyToManyField
    author = models.ManyToManyField('Author', null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    LC = models.CharField('Library of Congress number', max_length=50, help_text='Enter the LC number')

    # ManyToManyField because genre can contain many books. Books can have multiple genres
    # Genre class already defined so we can specify the object above
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    language = models.ManyToManyField('Language', max_length=100, help_text='Enter the language(s) here')

    READ_STATUS = (
        ('y', 'Read'),
        ('c', 'Currently Reading'),
        ('n', 'Not Read'),
    )

    status = models.CharField(
        max_length=1,
        choices=READ_STATUS,
        blank=True,
        default='n',
        help_text='Read status',
    )

    class Meta:
        ordering = ['LC']

    def __str__(self):
        """String for representing the Model object"""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail view for this book"""
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    """Model representing a specific copy of a book"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """Model represents an author"""
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        """String for representing the Model object"""
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        """Returns the url to access a detail view for this author"""
        return reverse('author-detail', args=[str(self.id)])

class Language(models.Model):
    """Model represents the languages"""
    name = models.CharField(max_length=50, help_text='Enter the language(s) of the book here')

    def __str__(self):
        return self.name
