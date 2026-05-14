from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_year = models.IntegerField()
    genre = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    cover_image_url = models.ImageField(upload_to="book_covers/", blank=True, null=True)

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="added_books",
    )

    def __str__(self):
        return f"Livro: {self.title}, {self.author}"

    @property
    def is_available(self) -> bool:
        return not self.loans.filter(return_date__isnull=True).exists()


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
        return f"Comodatário: {self.name}; {self.email}"


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    borrower = models.ForeignKey(
        Borrower, on_delete=models.SET_NULL, null=True, blank=False
    )
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)

    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="added_loans",
    )

    def clean(self):
        active_loans = Loan.objects.filter(book=self.book, return_date__isnull=True)
        if not self.pk and active_loans.exists():
            raise ValidationError(
                "Este livro foi emprestado e ainda não foi devolvido."
            )

        if self.due_date < self.loan_date:
            raise ValidationError(
                "A data de vencimento deve ser posterior à data de empréstimo."
            )

        if self.return_date and self.return_date < self.loan_date:
            raise ValidationError(
                "A data de devolução não pode ser anterior à data de empréstimo."
            )

    @property
    def is_overdue(self):
        if self.return_date:
            return self.return_date > self.due_date
        return self.due_date < timezone.now().date()

    def __str__(self):
        return f"Empréstimo: {self.book} para {self.borrower} no dia {self.loan_date}"
