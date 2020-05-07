from django.urls import path

from . import views


urlpatterns = [
    path('', views.MoviesView.as_view(), name='main'),
    path('category/', views.MoviesCategoryView.as_view(), name='category'),
    path('filter/', views.FilterMoviesView.as_view(), name='filter'),
    path('search/', views.Search.as_view(), name='search'),
    path('add-rating/', views.AddStarRating.as_view(), name='add_rating'),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('actor/<str:slug>/', views.ActorView.as_view(), name='actor_detail'),
    path('film_director/<str:slug>', views.FilmDirectorView.as_view(), name='film_director_detail'),
]