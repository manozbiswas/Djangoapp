from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from .models import MyList, Author

def index(request):
    return render(request, 'uvrating/index.html')

def details(request):
    authors = Author.objects.all()
    template = loader.get_template('uvrating/index.html')
    context = RequestContext(request, {
        'authors' : authors
    })
    return HttpResponse(template.render(context))


def authors(request):
    authors = Author.objects.all()
    context = {'authors': authors}
    return render(request, 'uvrating/authors.html', context)

def handle404(request):
    try:
        authors = Author.objects.all()
    except Author.DoesNotExist:
        raise Http404('Author Does not exist')
    return render(request, 'uvrating/authors.html', {'authors': authors})