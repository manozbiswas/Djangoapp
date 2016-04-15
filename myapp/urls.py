from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.show_university_list, name='index'),
    # url(r'^details$', views.details, name='details'),
    url(r'^topuv', views.show_top_uv, name='Top university'),
    url(r'^processtopuvform', views.get_top_uv_form_data, name='Top university'),
    url(r'^processdata', views.process_form_data, name='Form'),
    url(r'^showchart', views.show_chart, name='Chart'),
    url(r'^uvreputation', views.show_chart_form, name='Chart form'),
    # url(r'^import', views.show_university_list, name='Import'),
    # ex: /polls/5/

    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
