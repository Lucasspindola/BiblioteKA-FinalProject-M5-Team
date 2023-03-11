from .models import Book, Follow
from copies.models import Copie, Loan
from rest_framework.views import Response, Request
from datetime import datetime, timedelta

class CustomFollowMixin:
    def post(self, request: Request, *args, **kwargs: dict):
        try:
            book = Book.objects.get(id=kwargs.get("pk"))
        except Book.DoesNotExist:
            return Response({"detail": "Not found."}, 404)

        copies = Copie.objects.filter(is_available=True, book=kwargs.get("pk"))

        if copies:
            return Response({"message": "There are copies available for this book."}, 400)

        try:
            followers = Follow.objects.get(book=book, user=request.user)
            if followers:
                return Response({"message": "User already follow this book."}, 409)
        except Follow.DoesNotExist:
            pass        

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):

        loans = Loan.objects.filter(copie__book=self.kwargs.get("pk"))

        now = datetime.now()

        for i in loans:
            month_loan = int(i.expected_return_date.strftime("%m"))
            day_loan = int(i.expected_return_date.strftime("%d"))
            list_days = []
            if now.month == month_loan:
                list_days.append(i.expected_return_date.strftime("%d"))
                list_days.sort(key=None, reverse=False)
                day = int(list_days[0])
                if day == day_loan:
                    serializer.validated_data["will_be_available_date"] = datetime.strftime(i.expected_return_date, "%Y-%m-%d")

            list_days.append(i.expected_return_date.strftime("%d"))
            list_days.sort(key=None, reverse=False)
            day = int(list_days[0])
            if day == day_loan:
                serializer.validated_data["will_be_available_date"] = datetime.strftime(i.expected_return_date, "%Y-%m-%d")

        serializer.save(user_id=self.request.user.id, book_id=self.kwargs.get("pk"))
