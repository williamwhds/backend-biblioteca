from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from .models import Book, Borrower, Loan
from .serializers import BookSerializer, BorrowerSerializer, LoanSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        user = getattr(self.request, "user", None)
        if user and user.is_authenticated:
            return Book.objects.filter(added_by=user)
        return Book.objects.none()

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = getattr(self.request, "user", None)
        if user and user.is_authenticated:
            return Borrower.objects.filter(added_by=user)
        return Borrower.objects.none()

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = getattr(self.request, "user", None)
        if user and user.is_authenticated:
            return Loan.objects.filter(added_by=user)
        return Loan.objects.none()

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
