from django.shortcuts import render

def homepage(request):
    return render(request, 'api/homepage.html', {})