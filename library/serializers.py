from rest_framework import serializers

from accounts.serializers import LibraryManagerSerializer

from .models import Book, Borrower, Loan


class BorrowerSerializer(serializers.ModelSerializer):
    address = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    added_by_detail = LibraryManagerSerializer(source="added_by", read_only=True)

    class Meta:
        model = Borrower
        fields = ["id", "name", "email", "address", "added_by", "added_by_detail"]
        read_only_fields = ["added_by", "added_by_detail"]


class BookSerializer(serializers.ModelSerializer):
    added_by_detail = LibraryManagerSerializer(source="added_by", read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "published_year",
            "genre",
            "isbn",
            "cover_image_url",
            "is_available",
            "added_by",
            "added_by_detail",
        ]
        read_only_fields = ["is_available", "added_by_detail", "added_by"]


class LoanSerializer(serializers.ModelSerializer):
    book_details = BookSerializer(source="book", read_only=True)
    borrower_details = BorrowerSerializer(source="borrower", read_only=True)
    added_by_detail = LibraryManagerSerializer(source="added_by", read_only=True)
    borrower = serializers.PrimaryKeyRelatedField(
        queryset=Borrower.objects.all(), required=True, allow_null=False
    )

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
            "added_by",
            "added_by_detail",
        ]
        read_only_fields = ["loan_date", "added_by", "added_by_detail"]
