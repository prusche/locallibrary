from django.contrib import admin
from .models import Author, Subject, Book, BookInstance, Language, Publisher

# Register your models here.
#admin.site.register(Author)
#admin.site.register(Book)
admin.site.register(Subject)
#admin.site.register(BookInstance)
admin.site.register(Language)
admin.site.register(Publisher)

#class BookInline(admin.TabularInline):
#    model = Book
#    def get_extra(self, request, obj=None, **kwargs):
#        extra = 0
#        if obj:
#            return extra - obj.bookinstance_set.count()
#        return extra

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
# Does not work because author is not set as a ForeignKey to book
#    inlines = [BookInline]

#Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
#        if obj:
#            return extra - obj.bookinstance_set.count()
        return extra
# Register the Admin classes for Book using the decorator (this does
# the same thing as the admin.site.register() syntax)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_author', 'LC', 'display_subject')
    list_filter = ('status', 'author', 'subject')
    inlines = [BookInstanceInline]

# Register the BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
