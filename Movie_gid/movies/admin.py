from django.contrib import admin
from .models import Category, Actor, FilmDirector, Genre, Movie, MovieShots, RatingStars, Rating, Reviews


admin.site.register(Category)
admin.site.register(Actor)
admin.site.register(FilmDirector)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieShots)
admin.site.register(RatingStars)
admin.site.register(Rating)
admin.site.register(Reviews)
