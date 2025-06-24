from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def service(request):
    return render(request, 'index.html')