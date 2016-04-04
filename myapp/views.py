from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django import forms
from .forms import UvListForm
import sys
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from .models import MyList, Author, Data

DATA_URL = '/resources/data/'
all_university_names = ''


class MyView:

    def __init__(self):
        timesData = pd.read_csv("resources/data/timesData.csv")
        shanghaiData = pd.read_csv("resources/data/shanghaiData.csv")
        cwurData = pd.read_csv("resources/data/cwurData.csv")
        all_university_names = set(timesData.university_name).union(set(shanghaiData.university_name)).union(
            set(cwurData.institution))
        all_university_names_list = [str(i) for i in (list(all_university_names))]
        getUvData = r'\n'.join([str(university) for university in sorted(all_university_names_list)]).encode("utf-8")


def index(request):
    return render(request, 'uvrating/index.html')


def details(request):
    authors = Author.objects.all()
    template = loader.get_template('uvrating/index.html')
    context = RequestContext(request, {
        'authors': authors
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


def importdata(request):

    timesData = pd.read_csv("resources/data/timesData.csv")
    shanghaiData = pd.read_csv("resources/data/shanghaiData.csv")
    cwurData = pd.read_csv("resources/data/cwurData.csv")

    all_university_names = set(timesData.university_name).union(set(shanghaiData.university_name)).union(
        set(cwurData.institution))

    all_university_names_list = [str(i) for i in (list(all_university_names))]

    # getUvData = r''.join([ str(university) for university in sorted(all_university_names_list) ]).encode("utf-8")

    context = {'uvlist': sorted(all_university_names_list)}

    return render(request, 'uvrating/index.html', context)


def show_university_list(request):
    # timesData = Data.get_time_data(request)
    # shanghaiData = Data.get_shanghai_data(request)
    # cwurData = Data.get_cwur_data(request)
    #
    # all_university_names = set(timesData.university_name).union(set(shanghaiData.university_name)).union(
    #     set(cwurData.institution))
    #
    # all_university_names_list = [str(i) for i in (list(all_university_names))]
    #
    # # getUvData = r''.join([ str(university) for university in sorted(all_university_names_list) ]).encode("utf-8")

    context = {'uvlist': sorted(get_uv_list(request))}

    return render(request, 'uvrating/index.html', context)

def get_uv_list(request):
    timesData = Data.get_time_data(request)
    shanghaiData = Data.get_shanghai_data(request)
    cwurData = Data.get_cwur_data(request)

    all_university_names = set(timesData.university_name).union(set(shanghaiData.university_name)).union(
        set(cwurData.institution))

    all_university_names_list = [str(i) for i in (list(all_university_names))]
    return  all_university_names_list

def process_from_data(request):
    if request.method == 'POST':
        # form = UvListForm(request.POST)
        if request.POST.get('universityName'):
            data = request.POST.get('universityName')

            return HttpResponse(data)

    return HttpResponse("bad request")
    # return render(request, 'uvrating/index.html', {'form': form})