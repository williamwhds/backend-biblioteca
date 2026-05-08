from rest_framework import serializers

from accounts.serializers import LibraryManagerSerializer

from .models import Book, Borrower, Loan


class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ["id", "name", "email", "phone"]


class BookSerializer(serializers.ModelSerializer):
    added_by_detail = LibraryManagerSerializer(source="added_by", read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "genre",
            "isbn",
            "cover_image",
            "is_available",
            "added_by",
            "added_by_detail",
        ]


class LoanSerializer(serializers.ModelSerializer):
    book_details = BookSerializer(source="book", read_only=True)
    borrower_details = BorrowerSerializer(source="borrower", read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "book",
            "book_details",
            "borrower",
            "borrower_details",
            "loan_date",
            "due_date",
            "return_date",
        ]
