from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from .models import Book, Author, BookInstance, Subject, Language

# Create your views here.
def index(request):
    """View function for home page of site"""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Books Read
    num_already_read = Book.objects.filter(status__exact='y').count()
    # Books not read
    num_to_read = Book.objects.filter(status__exact='n').count()

    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books' : num_books,
        'num_instance' : num_instance,
        'num_already_read' : num_already_read,
        'num_to_read' : num_to_read,
        'num_authors' : num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalog/index.html', context=context)

# Class-based View for showing all books
class BookListView(generic.ListView):
    model = Book
    paginate_by = 50

class BookDetailView(generic.DetailView):
    model = Book

class SubjectListView(generic.ListView):
    model = Subject

class SubjectDetailView(generic.DetailView):
    model = Subject

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """ Generic class-based view listing books on load to current user """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
