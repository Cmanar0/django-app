from django.shortcuts import render

def terms_view(request):
    return render(request, 'authentication/terms.html')
