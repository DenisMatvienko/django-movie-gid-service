from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.http import HttpResponse


from .models import *
from .forms import *


#   1 функция для получения всех Жанров и 1 функция для получения всех годов, с фильмами которые не черновики
class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


#   Списиок фильмов на главной странице, с шаблоном тоже самое, что и в detail
class MoviesView(GenreYear, ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 12


#   Карточка фильма, полное его описание
class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = 'url'

    #   Шаблон не указываем потому что автоматически подставляется Detail к Movie,
    #   тем самым можно не указывать шаблон исходя из того, что в темплейтс шаблон назван movie_detail, к movie
    #   подставляется detail и шаблон находится. Если шаблон называется по маске: model(название модели)_
    #   detail(исп. класса), то можно путь к шаблону не указывать

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['form'] = ReviewForm()
        return context


#   Отзывы
class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            #   в if вычисляем родителя отзыва, для отображения в админке, чтобы знать к какому вопросу принадлежит
            #   ответ
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


#   Информация об актере
class ActorView(GenreYear, DetailView):
    model = Actor
    model_2 = FilmDirector
    template_name = 'movies/actor.html'
    slug_field = 'name'


#   Информация о режиссере
class FilmDirectorView(GenreYear, DetailView):
    model = FilmDirector
    template_name = 'movies/film_director.html'
    slug_field = 'name'


#   Фильтр фильмов запятая. "," между year__in и genres__in это логическое "И", т.е. условие фильтра, что совпадают
#   обязательно и year и genres. Для "ИЛИ", мы оборачиваем в Q и ставим | - логическое или.
#   "Q(year__in) | Q(genres__in)" - это ИЛИ. year__in, genres__in - это И. Сейчас стоит И, т.е. находится только то, что
#   удовлетворяет одновременно и year и genre
# class FilterMoviesView(ListView):
# def get_queryset(self):
#     queryset = Movie.objects.filter(
#         year__in=self.request.GET.getlist('year'),
#         genres__in=self.request.GET.getlist('genre'))
#     return queryset

#   Фильтр выводящий и год и жанр одновременно
class FilterMoviesView(ListView):
    paginate_by = 12

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join([f"year={x}&" for x in self.request.GET.getlist('year')])
        context['genre'] = ''.join([f"genre={x}&" for x in self.request.GET.getlist('genre')])
        return context


#   Добавление рейтинга фильму
class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


#   Поиск фильмов. SQLITE ищет без регистра только кодировку ASCII, в utf-8 метод tagline__icontains
#   становится полностью регистрозависимым, так что по своим свойства в SQLITE он будет находить правильно только
#   в кодировке ASCII, тоже самое и с методом __iexact и остальными
class Search(ListView):
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context
