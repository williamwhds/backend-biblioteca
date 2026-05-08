from django.urls import include, path
from rest_framework.routers import DefaultRouter

from library.views import BookViewSet, BorrowerViewSet, LoanViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet, basename="book")
router.register(r"loans", LoanViewSet, basename="loan")
router.register(r"borrowers", BorrowerViewSet, basename="borrower")

urlpatterns = [
    path("api/", include(router.urls)),
]
