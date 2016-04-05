from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from .models import Author, Data
import os
from django.conf import settings
# from seaborn import set
# Import Packages
import sys
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt



def index(request):
    # dir = os.path.dirname(__file__) ##H:\py\mysite\myapp project dir
    # dirr = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) ##Base dir H:\py\mysite

    return render(request, 'uvrating/index.html')


# def details(request):
#     authors = Author.objects.all()
#     template = loader.get_template('uvrating/index.html')
#     context = RequestContext(request, {
#         'authors': authors
#     })
#     return HttpResponse(template.render(context))


# def authors(request):
#     authors = Author.objects.all()
#     context = {'authors': authors}
#     return render(request, 'uvrating/authors.html', context)


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

    context = {'uvlist': sorted(all_university_names_list)}

    return render(request, 'uvrating/index.html', context)


def show_university_list(request):
    uvlist = {'uvlist': sorted(get_uv_list())}
    return render(request, 'uvrating/index.html', uvlist)


def get_uv_list():
    timesData = Data.get_time_data()
    shanghaiData = Data.get_shanghai_data()
    cwurData = Data.get_cwur_data()

    all_university_names = set(timesData.university_name).union(set(shanghaiData.university_name)).union(
        set(cwurData.institution))

    all_university_names_list = [str(i) for i in (list(all_university_names))]
    return all_university_names_list


def process_form_data(request):
    if request.method == 'POST':
        if request.POST.get('universityName'):
            university = request.POST.get('universityName')
            university_name = [university]
            ### process_graph function is called
            process_graph(university_name)
            return render(request, 'uvrating/index.html', {'formpopulated' : True , 'uvlist': sorted(get_uv_list())})
    return render(request, 'uvrating/index.html', {'formpopulated' : False , 'uvlist': sorted(get_uv_list()),
                                                   'message' : 'Please select a university name'})


def process_graph(university):
    timesData = Data.get_time_data()
    shanghaiData = Data.get_shanghai_data()
    cwurData = Data.get_cwur_data()
    # university_name = []
    # university_name = university
    times_plot_data = timesData[timesData.university_name.isin(university)][['world_rank', 'year']]
    shanghai_plot_data = shanghaiData[shanghaiData.university_name.isin(university)][['world_rank', 'year']]
    cwur_plot_data = cwurData[cwurData.institution.isin(university)][['world_rank', 'year']]

    times_plot_data['source'] = 'Times'
    shanghai_plot_data['source'] = 'Shanghai'
    cwur_plot_data['source'] = 'CWUR'

    ## parse the first number in rank for data ranges

    times_plot_data['world_rank'] = times_plot_data['world_rank'].str.split('-').str[0]
    shanghai_plot_data['world_rank'] = shanghai_plot_data['world_rank'].str.split('-').str[0]

    plot_data = times_plot_data.append(shanghai_plot_data).append(cwur_plot_data)
    plot_data['world_rank'] = plot_data['world_rank'].astype(int)

    ############ added myself
    times_plot_data['source'] = ''
    shanghai_plot_data['source'] = ''
    cwur_plot_data['source'] = ''
    #################
    sns.set(style="ticks", color_codes=True)
    plt.rcParams['figure.figsize'] = 16, 12
    ax = sns.pointplot(x='year', y='world_rank', hue='source', data=plot_data);

    # Styling

    plt.title(university[0] + " Ranking", fontsize=26)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.ylabel("World Rank", fontsize=26)
    plt.xlabel("Year", fontsize=26)
    plt.tight_layout()
    plt.legend(loc='upper left', fontsize=20)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # Save File
    plt.savefig('resources/images/university.png')
    plt.cla()
    plt.clf()
    plt.close()


    # return HttpResponse("image processed")
