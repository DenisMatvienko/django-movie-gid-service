from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Actor, FilmDirector, Genre, Movie, MovieShots, RatingStars, Rating, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    """ Ckeditor widget """
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


#   Main header name & title
admin.site.site_title = 'Админка MovieGid'
admin.site.site_header = 'Добро пожаловать в административную панель MovieGid'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
        Category of movies
        In admin check the ordering table-viewing + links
    """
    list_display = ('id', 'name', 'url')
    list_display_links = ('id', 'name')


class ReviewInline(admin.TabularInline):
    """ With open get all movies reviews """
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotsInline(admin.TabularInline):
    """ Add movieshots to each movie in admin """
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="100", style="border-radius:10%;"')
    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
        Movies
        In admin make the ordering, filter and serch
        Bind ReviewInline, [Make a link for ReviewInline to see reviews linked to the movie, same to MovieShotsInline]

    """
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [MovieShotsInline, ReviewInline]
    #   Save button on the top
    save_on_top = True
    #   Add button "save as new object", editing-page don't close, all data in fields save,
    #   at the end, we are should change data
    save_as = True
    #   Allows you to select a field for editing directly in the table, without having to open the card. in our case
    #   is - draft
    list_editable = ('draft',)
    #   Ckeditor form
    form = MovieAdminForm
    #   In Poster field add poster-image, by func get_image
    readonly_fields = ('get_image',)
    #   We split cells with fields into a more convenient display format
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': ('description', ('poster', 'get_image'))
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),
        ('Cостав съемочной группы, информация о фильме', {
            'classes': ('collapse',),
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        ('Бюджет, сборы', {
            'classes': ('collapse',),
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ('Опции', {
            'fields': (('url', 'draft'),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="150" height="200" style="border-radius:10%;"')
    get_image.short_description = 'Постер'


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """ Reviews admin display """
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """ Genres admin display """
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """ Actors admin display """
    search_fields = ('name', 'age')
    list_display = ('name', 'age', 'get_image', 'image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60" style="border-radius:10%;"')
    get_image.short_description = 'Изображение'


@admin.register(FilmDirector)
class ActorAdmin(admin.ModelAdmin):
    """ Film Director admin display """
    search_fields = ('name', 'age')
    list_display = ('name', 'age', 'get_image', 'image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60" style="border-radius:10%;"')
    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """ Rating admin display """
    list_display = ('movie', 'star', 'ip')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """ Movie shots admin display """
    list_display = ('title', 'movie', 'get_image', 'image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="80" style="border-radius:10%;"')
    get_image.short_description = 'Изображение'


admin.site.register(RatingStars)

