from django.shortcuts import render
from django.http  import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Post

# Create your views here.
def index(request):
    title = 'Home'
    return render(request, 'index.html', {'title':title})
# Create your views here.
