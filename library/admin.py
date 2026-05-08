from django.contrib import admin

from library.models import Book, Borrower, Loan

admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(Borrower)
