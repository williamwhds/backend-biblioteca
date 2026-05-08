from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Book, Borrower, Loan
from .serializers import BookSerializer, BorrowerSerializer, LoanSerializer


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(added_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class BorrowerViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Borrower.objects.filter(added_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Loan.objects.filter(added_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        loan = self.get_object()
        if loan.return_date:
            return Response(
                {"error": "Already returned"}, status=status.HTTP_400_BAD_REQUEST
            )

        loan.return_date = timezone.now()
        loan.save()
        return Response({"status": "Book returned successfully"})
