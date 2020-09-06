from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.http import HttpResponse

from .models import *
from .forms import *


class GenreYear:
    """
        Object of filters for Genre, Years & Categories
    """
    def get_genres(self):
        """ Get list of genres into sidebar """
        return Genre.objects.get_queryset().order_by('id')

    def get_years(self):
        """ Get list of years into sidebar """
        return Movie.objects.filter(draft=False).values('year')

    def get_category(self):
        """ Get list of categories """
        return Category.objects.all()


class MoviesCategoryView(GenreYear, ListView):
    """ List by categories """
    paginate_by = 9

    def get_queryset(self):
        queryset = Movie.objects.filter(category__in=self.request.GET.getlist('category')).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        """ For with pagination urls didn't have the errors and we are can find second pages & others pages  """
        context = super().get_context_data(*args, **kwargs)
        context['category'] = ''.join([f"category={x}&" for x in self.request.GET.getlist('category')])
        return context


class MoviesView(GenreYear, ListView):
    """ List of movies on main page """
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 9


class MovieDetailView(GenreYear, DetailView):
    """ Movie-page, with all description """
    model = Movie
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['form'] = ReviewForm()
        return context


class AddReview(View):
    """ Add reviews into movie-page """
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            #   get parent of review, for displaying in admin panel. That for we are knew, for which
            #   question belongs answer
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """ Actors information """
    model = Actor
    model_2 = FilmDirector
    template_name = 'movies/actor.html'
    slug_field = 'name'


class FilmDirectorView(GenreYear, DetailView):
    """ Film directors information """
    model = FilmDirector
    template_name = 'movies/film_director.html'
    slug_field = 'name'


class FilterMoviesView(GenreYear, ListView):
    """ Filter which displays year and genre objects in same time """
    paginate_by = 9

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        ).distinct()
        return queryset

    """ For with pagination urls didn't have the errors and we are can find second pages & others pages  """
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join([f"year={x}&" for x in self.request.GET.getlist('year')])
        context['genre'] = ''.join([f"genre={x}&" for x in self.request.GET.getlist('genre')])
        return context
        

class AddStarRating(View):
    """ Add count of stars by each movie-objects """
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


class Search(ListView):
    """
        Movies search
        Note:
            SQLITE search without case sensitive just in ASCII encoding,
            Method in UTF-8 tagline__icontains - full case sensitive
        That reason limited search
    """
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context
