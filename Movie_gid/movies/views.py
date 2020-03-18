from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie


#   Списиок фильмов на главной странице, с шаблоном тоже самое, что и в detail
class MoviesView(ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)


#   Карточка фильма, полное его описание.
class MovieDetailView(DetailView):
    model = Movie
    slug_field = 'url'
    #   Шаблон не указываем потому что автоматически подставляется Detail к Movie,
    #   тем самым можно не указывать шаблон исходя из того, что в темплейтс шаблон назван movie_detail, к movie
    #   подставляется detail и шаблон находится. Если шаблон называется по маске: model(название модели)_
    #   detail(исп. класса), то можно путь к шаблону не указывать

