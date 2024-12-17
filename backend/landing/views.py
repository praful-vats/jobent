from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def landing_page(request):
    return render(request, 'landing/landing_page.html')
    def landing_page(request):
        data = {
            'message': 'Welcome to the landing page!'
        }
        return JsonResponse(data)