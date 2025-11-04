from django.db.models import Count
from django.shortcuts import render

from django_app.models import Teacher


def index(request):
    # BEGIN (write your solution here)
    
    # END

    return render(
        request,
        "index.html",
        {
            "teachers": teachers,
        },
    )