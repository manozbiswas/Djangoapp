from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from .models import Author, Data
from subprocess import check_output
import os
from django.conf import settings
# from seaborn import set
# Import Packages
import sys
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt, mpld3
import matplotlib.pylab as pylab
from matplotlib.figure import Figure
import matplotlib.path as path
import matplotlib.patches as patches

import plotly as py
from plotly.plotly import *
import plotly.graph_objs as go


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
            return render(request, 'uvrating/index.html',
                          {'uv': university, 'formpopulated': True, 'uvlist': sorted(get_uv_list())})
    return render(request, 'uvrating/index.html', {'formpopulated': False, 'uvlist': sorted(get_uv_list()),
                                                   'message': 'Please select a university name'})


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


### Shows Top 10 university list####
def show_top_uv(request):
    # uvlist = {'uvlist': sorted(get_uv_list())}
    # org_list = {'orglist':check_output(["ls", "resources/data"]).decode("utf8")}
    lists = {
        'Times Higher Education World University Ranking': 'Times Higher Education World University Ranking',
        'Shanghai Ranking': 'Shanghai Ranking',
        'Center for World University Rankings': 'Center for World University Rankings'
    }
    listOfNumber = [x for x in range(1, 11)]
    return render(request, 'uvrating/topuv.html', {'lists': lists, 'listOfNumber': listOfNumber})


def get_top_uv_form_data(request):
    rank_lists = {
        'Times Higher Education World University Ranking': 'Times Higher Education World University Ranking',
        'Shanghai Ranking': 'Shanghai Ranking',
        'Center for World University Rankings': 'Center for World University Rankings'
    }
    listOfNumber = [x for x in range(1, 11)]

    if request.method == 'POST':
        if request.POST.get('rankingSystem') and request.POST.get('numberOfUv'):
            if request.POST.get('rankingSystem') != '' and request.POST.get('numberOfUv') != '':
                rankingSystem = request.POST.get('rankingSystem')
                numberOfUv = request.POST.get('numberOfUv')
                process_top_uv_graph(rankingSystem, numberOfUv)
            return render(request, 'uvrating/topuv.html',
                          {'listOfNumber': listOfNumber, 'formpopulated': True, 'rankingSystem': rankingSystem,
                           'numberOfUv': numberOfUv, 'lists': rank_lists})
        return render(request, 'uvrating/topuv.html',
                      {'error': True, 'lists': rank_lists, 'listOfNumber': listOfNumber,})
    return render(request, 'uvrating/topuv.html',
                  {'formpopulated': False, 'listOfNumber': listOfNumber, 'error': True, 'lists': rank_lists})


def process_top_uv_graph(rankingSystem, numberOfUv):
    sns.set(style="white", color_codes=True)

    # % matplotlib inline
    pylab.rcParams['figure.figsize'] = 16, 12
    plot_data = ''
    numberOfUv = int(numberOfUv)
    if rankingSystem == 'Times Higher Education World University Ranking':
        timesData = Data.get_time_data()
        schools_to_show = timesData.university_name[:numberOfUv]
        plot_data = timesData[timesData.university_name.isin(schools_to_show)]
        hue = "university_name"
        draw_graph(plot_data, rankingSystem, numberOfUv, hue)
    elif rankingSystem == 'Shanghai Ranking':
        shanghaiData = Data.get_shanghai_data()
        schools_to_show = shanghaiData.university_name[:numberOfUv]
        plot_data = shanghaiData[shanghaiData.university_name.isin(schools_to_show)]
        hue = "university_name"
        draw_graph(plot_data, rankingSystem, numberOfUv, hue)
    elif rankingSystem == 'Center for World University Rankings':
        cwurData = Data.get_cwur_data()
        schools_to_show = cwurData.institution[:numberOfUv]
        plot_data = cwurData[cwurData.institution.isin(schools_to_show)]
        hue = "institution"
        draw_graph(plot_data, rankingSystem, numberOfUv, hue)


def draw_graph(plot_data, rankingSystem, numberOfUv, hue):
    plot_data['world_rank'] = plot_data['world_rank'].astype(int)
    ax = sns.pointplot(x='year', y='world_rank', hue=hue, data=plot_data);
    pylab.title("Top " + str(numberOfUv) + " university by " + rankingSystem, fontsize=26)
    pylab.xticks(fontsize=20)
    pylab.yticks(fontsize=20)
    pylab.ylabel("World Rank", fontsize=26)
    pylab.xlabel("Year", fontsize=26)
    pylab.savefig('resources/images/topuv.png')
    pylab.cla()
    pylab.clf()
    pylab.close()


### Radar Chart ###

def get_time_data_as_list():
    timesData = Data.get_time_data()
    all_university_names = set(timesData.university_name)
    all_university_names_list = [str(i) for i in (list(all_university_names))]
    # uvlist = {'uvlist': sorted(all_university_names_list)}
    return sorted(all_university_names_list)


def show_chart_form(request):
    uvlist = {'uvlist': get_time_data_as_list()}
    return render(request, 'uvrating/chart.html', uvlist)


def show_chart(request):
    if request.method == 'POST':
        if request.POST.get('universityName'):
            university = request.POST.get('universityName')
            university_name = [university]

            try:
                make_chart(university)
                return render(request, 'uvrating/chart.html',
                              {'uv': university, 'formpopulated': True, 'uvlist': get_time_data_as_list()})
            except IndexError:
                return render(request, 'uvrating/chart.html',
                              {'formpopulated': False, 'uvlist': get_time_data_as_list(),
                               'error': 'There is some internal error for missing data, Please try later'})
    return render(request, 'uvrating/chart.html',
                  {'formpopulated': False, 'error': "There is some itenal error please try agian later",
                   'uvlist': get_time_data_as_list()})


def make_chart(university_name):
    my_university_name = [university_name]

    timesdata = Data.get_time_data()

    properties = ['research', 'teaching', 'international', 'citations', 'income']

    datarow = timesdata[timesdata.university_name.isin(my_university_name)].tail(1).reset_index(drop=True)
    values = datarow[properties].astype(float).as_matrix().flatten()

    title_text = '-'.join([my_university_name[0], str(datarow.year[0])])

    # Choose some nice colors
    matplotlib.rc('axes', facecolor='green')

    # Make figure background the same colors as axes
    fig = plt.figure(figsize=(10, 8), facecolor='white')
    fig.suptitle(title_text, fontsize=14, fontweight='bold')

    # Use a polar axes
    axes = plt.subplot(111, polar=True)

    # Set ticks to the number of properties (in radians)
    t = np.arange(0, 2 * np.pi, 2 * np.pi / len(properties))
    plt.xticks(t, [])

    # Set yticks from 0 to 100
    plt.yticks(np.linspace(0, 100, 11))

    # Draw polygon representing values
    points = [(x, y) for x, y in zip(t, values)]
    points.append(points[0])
    points = np.array(points)
    codes = [path.Path.MOVETO, ] + \
            [path.Path.LINETO, ] * (len(values) - 1) + \
            [path.Path.CLOSEPOLY]
    _path = path.Path(points, codes)
    _patch = patches.PathPatch(_path, fill=True, color='blue', linewidth=0, alpha=.1)
    axes.add_patch(_patch)
    _patch = patches.PathPatch(_path, fill=False, linewidth=2)
    axes.add_patch(_patch)

    # Draw circles at value points
    plt.scatter(points[:, 0], points[:, 1], linewidth=2,
                s=50, color='red', edgecolor='black', zorder=10)

    # Set axes limits
    plt.ylim(0, 100)

    # Draw ytick labels to make sure they fit properly
    for i in range(len(properties)):
        angle_rad = i / float(len(properties)) * 2 * np.pi
        angle_deg = i / float(len(properties)) * 360
        ha = "right"
        if angle_rad < np.pi / 2 or angle_rad > 3 * np.pi / 2: ha = "left"
        plt.text(angle_rad, 100.75, properties[i], size=14,
                 horizontalalignment=ha, verticalalignment="center")


        # A variant on label orientation
        #    plt.text(angle_rad, 11, properties[i], size=14,
        #             rotation=angle_deg-90,
        #             horizontalalignment='center', verticalalignment="center")
    # plt.show()
    # Done
    # fig = plt.figure(figsize=(10, 8), facecolor='white')
    # fig.suptitle(title_text, fontsize=14, fontweight='bold')
    plt.savefig('resources/images/chart.png', facecolor='white')

    # plt.show()
    # return mpld3.fig_to_html(fig, 'resources/images/json.html')
    # return mpld3.save_json(fig,'resources/images/json.json')
    # figg = plt.figure()
    # mpld3.save_html(fig, 'resources/images/json.html')
    # mpld3.show(fig)
    # mpld3.show(fig)
    fig.clf()
    fig.clear()
    plt.cla()
    plt.clf()
    plt.close()


## bubble chart

def show_topmost_uv(request):
    lists = {
        'Times Higher Education World University Ranking': 'Times Higher Education World University Ranking',
        'Shanghai Ranking': 'Shanghai Ranking',
        'Center for World University Rankings': 'Center for World University Rankings'
    }
    return render(request, 'uvrating/topmostuv.html', {'lists': lists,})


def process_topmost_uv_form(request):
    rank_lists = {
        'Times Higher Education World University Ranking': 'Times Higher Education World University Ranking',
        'Shanghai Ranking': 'Shanghai Ranking',
        'Center for World University Rankings': 'Center for World University Rankings'
    }

    if request.method == 'POST':
        if request.POST.get('rankingSystem'):
            if request.POST.get('rankingSystem') != '':
                rankingSystem = request.POST.get('rankingSystem')
                display_by_plotly(rankingSystem)
            return render(request, 'uvrating/topmostuv.html',
                          {'formpopulated': True, 'rankingSystem': rankingSystem,
                           'lists': rank_lists})
        return render(request, 'uvrating/topmostuv.html',
                      {'error': True, 'lists': rank_lists})
    return render(request, 'uvrating/topmostuv.html',
                  {'formpopulated': False, 'error': True, 'lists': rank_lists})


def display_by_plotly(rankingSystem):
    if rankingSystem == 'Times Higher Education World University Ranking':
        timesData = Data.get_time_data()
        schools_to_show = timesData.university_name[:1000]
        plot_data = timesData[timesData.university_name.isin(schools_to_show)]
        # plot_data['world_rank'] = plot_data['world_rank']
        plot_data['world_rank'] = plot_data['world_rank'].str.split('-').str[0]
        plot_data['country'] = plot_data['country']
        # plot_data['world_rank'] = plot_data['world_rank'].str.split('-').str[0]
        plot_data['year'] = plot_data['year'].astype(int)
        trace = go.Scatter3d(
            x=plot_data['year'],
            y=plot_data['world_rank'],
            z=plot_data['university_name'],
            text="Country: " + plot_data['country'],
            mode='markers',  # +lines
            # name='steepest',
            marker=dict(
                size=[x for x in range(200, 0, -2)],
                color=[x for x in range(5500, 0, -1)],
                showscale=True,  # [::-1],
                sizeref=750,
                colorscale='Viridis',
                sizemode='diameter',
                line=dict(color='rgb(140, 140, 170)')
            )
        )
        data = [trace]
        layout = go.Layout(
            showlegend=False,
            height=600,
            width=1000,
            title='Total data visualization of ' + rankingSystem,
            scene=dict(
                xaxis=dict(title='X: Year',
                           titlefont=dict(color='Orange')
                           ),
                yaxis=dict(
                    title='Y: World Rank',
                    titlefont=dict(color='Orange')),
                zaxis=dict(
                    title='Z: University',
                    titlefont=dict(color='Orange')),
                # bgcolor='rgb(200,224,34)'#'rgb(168, 219, 52)'
            )
        )
        fig = go.Figure(data=data, layout=layout)
        # mpld3.save_html(fig, 'resources/images/bubblempld3.html')
        plot_url = py.offline.plot(fig, filename='resources/images/topmostuv.html', auto_open=False)

    elif rankingSystem == 'Shanghai Ranking':
        shanghaiData = Data.get_shanghai_data()
        schools_to_show = shanghaiData.university_name[:1000]
        plot_data = shanghaiData[shanghaiData.university_name.isin(schools_to_show)]

        plot_data = shanghaiData[shanghaiData.university_name.isin(schools_to_show)]
        # plot_data['world_rank'] = plot_data['world_rank']
        plot_data['world_rank'] = plot_data['world_rank'].str.split('-').str[0]
        # plot_data['world_rank'] = plot_data['world_rank'].str.split('-').str[0]
        plot_data['year'] = plot_data['year']  # .astype(int)
        trace = go.Scatter3d(
            x=plot_data['year'],
            y=plot_data['world_rank'],
            z=plot_data['university_name'],
            text=" ",
            mode='markers',  # +lines
            # name='steepest',
            marker=dict(
                size=[x for x in range(200, 0, -1)],
                color=[x for x in range(5500, 0, -1)],
                showscale=True,  # [::-1],
                sizeref=750,
                colorscale='Viridis',
                sizemode='diameter',
                line=dict(color='rgb(140, 140, 170)')
            )
        )
        data = [trace]
        layout = go.Layout(
            showlegend=False,
            height=600,
            width=1000,
            title='Total data visualization of ' + rankingSystem,
            scene=dict(
                xaxis=dict(title='X: Year',
                           titlefont=dict(color='Orange')
                           ),
                yaxis=dict(
                    title='Y: World Rank',
                    titlefont=dict(color='Orange')),
                zaxis=dict(
                    title='Z: University',
                    titlefont=dict(color='Orange')),
                # bgcolor='yellow'
            )
        )
        fig = go.Figure(data=data, layout=layout)
        # mpld3.save_html(fig, 'resources/images/bubblempld3.html')
        plot_url = py.offline.plot(fig, filename='resources/images/topmostuv.html', auto_open=False)

    elif rankingSystem == 'Center for World University Rankings':
        cwurData = Data.get_cwur_data()
        schools_to_show = cwurData.institution[:1000]
        plot_data = cwurData[cwurData.institution.isin(schools_to_show)]
        plot_data['country'] = plot_data['country']
        plot_data['world_rank'] = plot_data['world_rank']
        plot_data['year'] = plot_data['year'].astype(int)

        trace = go.Scatter3d(
            y=plot_data['year'],
            x=plot_data['world_rank'],
            z=plot_data['institution'],
            text="Country: " + plot_data['country'],
            mode='markers',  # +lines
            # name='steepest',
            marker=dict(
                size=[x for x in range(100, 0)],
                color=[x for x in range(5500, 0)],
                showscale=True,  # [::-1],
                sizeref=750,
                colorscale='Viridis',
                sizemode='diameter',
                line=dict(color='rgb(140, 140, 170)')
            )
        )
        data = [trace]
        layout = go.Layout(
            showlegend=False,
            height=700,
            width=1100,
            title='Total data visualization of ' + rankingSystem,
            scene=dict(
                xaxis=dict(title='X: World Rank',
                           titlefont=dict(color='Orange')
                           ),
                yaxis=dict(
                    title='Y: Year',
                    titlefont=dict(color='Orange')),
                zaxis=dict(
                    title='Z: University',
                    titlefont=dict(color='Orange')),
                # bgcolor='rgb(20, 24, 54)'
            )
        )
        fig = go.Figure(data=data, layout=layout)
        # mpld3.save_html(fig, 'resources/images/bubblempld3.html')
        plot_url = py.offline.plot(fig, filename='resources/images/topmostuv.html', auto_open=False)


# def process_3d_graph(plot_data, uvname, title):
#     plot_data['country'] = plot_data['country']
#     plot_data['world_rank'] = plot_data['world_rank'].str.split('-').str[0]
#     plot_data['year'] = plot_data['year'].astype(int)
#
#     trace = go.Scatter3d(
#         x=plot_data['year'],
#         y=plot_data['world_rank'],
#         z=plot_data[uvname],
#         text="Country: " + plot_data['country'],
#         mode='markers',  # +lines
#         # name='steepest',
#         marker=dict(
#             size=[x for x in range(200, 0, -1)],
#             color=[x for x in range(200, 0, -1)],
#             showscale=True,  # [::-1],
#             sizeref=750,
#             colorscale='Viridis',
#             sizemode='diameter',
#             line=dict(color='rgb(140, 140, 170)')
#         )
#     )
#     data = [trace]
#     layout = go.Layout(
#         showlegend=False,
#         height=700,
#         width=1100,
#         title='Top'  # + title
#     )
#     fig = go.Figure(data=data, layout=layout)
#     # mpld3.save_html(fig, 'resources/images/bubblempld3.html')
#     plot_url = py.offline.plot(fig, filename='resources/images/topmostuv.html', auto_open=False)






def display_university_by_country(request):
    timesData = Data.get_time_data()
    id_count_by_region = timesData.groupby('country')['world_rank'].count()
    id_count_by_region.sort_values(na_position='last', inplace=True, ascending=False)
    id_count_by_region[:10]


    trace = go.Bar(
        x=id_count_by_region,
        y=timesData['country'],
        orientation='h',
        marker=dict(
            color='rgba(55, 128, 191, 1)',
            line=dict(
                color='rgba(55, 128, 191, 1.0)',
                width=1,
            )
        )
    )
    data = [trace]
    layout = go.Layout(
        # barmode='stack',
        margin=dict(
            l=200,
            r=20,
            t=70,
            b=70,
        ),
        width=1000,
        height=700,
        yaxis=dict(
            title="Country"
        ),
        xaxis=dict(
            title="Number of university"
        )
    )
    fig = go.Figure(data=data, layout=layout)

    plot_url = py.offline.plot(fig, filename='resources/images/uvincountry.html', auto_open=False)

    return render(request, 'uvrating/total-uv-in-a-country.html', {'correctUrl': True})
