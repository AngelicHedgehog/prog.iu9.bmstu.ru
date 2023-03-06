from django.shortcuts import render


def home(request):
    return render(request, 'one_test/home.html')