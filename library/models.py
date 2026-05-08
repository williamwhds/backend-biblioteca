from django.conf import settings
from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_year = models.IntegerField()
    genre = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    cover_image_url = models.URLField(blank=True, null=True)

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="added_books",
    )

    def __str__(self):
        return f"{self.title}, {self.author}"


class Borrower(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="added_borrowers",
    )

    def __str__(self):
        return str(self.name)


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(
        Borrower, on_delete=models.SET_NULL, null=True, blank=False
    )
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)

    @property
    def is_overdue(self):
        if self.return_date:
            return self.return_date > self.due_date
        return self.due_date < timezone.now().date()
