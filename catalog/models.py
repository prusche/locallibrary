from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class Subject(models.Model):
    """Model represents a book genre"""
    name = models.CharField(max_length=200, help_text='Enter the subject for this book (e.g. History-Anglo-Saxon)')

    class Meta:
        ordering = ['name']

    def __str__(self):
        """String for representing the Model object"""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail view for this author"""
        return reverse('subject-detail', args=[str(self.id)])

class Book(models.Model):
    """Model represents a book, but not a specific copy of a book"""
    title = models.CharField(max_length=200, help_text='Add the title of the book')

    # Foreign Key used because book can only have one author but authors
    # can have many books-- This is not true for multiple author books
    # so I am changing it to ManyToManyField; setting related name to relate the two
    author = models.ManyToManyField('Author', max_length=200, help_text='Add the names of the author(s)', related_name='books')

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    LC = models.CharField('Library of Congress number', max_length=50, help_text='Enter the LC number')
    # adding from django documentation
    # publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE, null=True)
    # publication_date = models.DateField(null=True, blank=True)

    # ManyToManyField because genre can contain many books. Books can have multiple genres
    # Genre class already defined so we can specify the object above
    subject = models.ManyToManyField(Subject, help_text='Select a subject for this book', related_name='books')

    language = models.ManyToManyField('Language', max_length=100, help_text='Enter the language(s) here', related_name='books')

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
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    # To show the list of authors next to the book in the admin panel
    def display_author(self):
        return ', and '.join(author.last_name + ', ' + author.first_name for author in self.author.all()[:3])

    # To show the list of authors next to book on book list page
    def display_author_first_last(self):
        return ', and '.join(author.first_name + ' ' + author.last_name for author in self.author.all()[:3])

    # To show the list of subjects next ot the book in the admin panel
    def display_subject(self):
        return ', '.join(subject.name for subject in self.subject.all()[:3])

class BookInstance(models.Model):
    """Model representing a specific copy of a book"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

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
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

        @property
        def is_overdue(self):
            if self.due_back and date.today() > self.due_back:
                return True
            return False


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

    # To show the list of authors next to book on book list page
    def display_author_first_last(self):
        return f'{self.first_name} {self.last_name}'

class Language(models.Model):
    """Model represents the languages"""
    name = models.CharField(max_length=50, help_text='Enter the language(s) of the book here')

    def __str__(self):
        return self.name

# adding from Django documentation
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name
