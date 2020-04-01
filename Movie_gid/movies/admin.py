from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Actor, FilmDirector, Genre, Movie, MovieShots, RatingStars, Rating, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget


#   ckeditor widget
class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


#   Заголовок админки и title
admin.site.site_title = 'Админка MovieGid'
admin.site.site_header = 'Добро пожаловать в административную панель MovieGid'


#   "Категории" в админке выставляем внутри порядок отображения таблицы + ссылки у столбцов
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('id', 'name')


#   При открытии выидим все отзывы к фильму
class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


#   Прикрепляем кадры из фильма к нашему фильму в админке, TabularInline - горизонтальное отображение,
#   Stacked- вертикальое + метод для наглядного вывода изображения
class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="100", style="border-radius:10%;"')
    get_image.short_description = 'Изображение'


#   "Фильмы" в админке выставляем порядок отображения, фильтр по категориям и годам, и поиск
#   [оставляем привязку для ReviewInline, чтобы видеть отзывы привязвнные к фильму][оставляем привязку для
#   MovieShotsInline, чтобы видеть кадры из фильма привязвнные к фильму]
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [MovieShotsInline, ReviewInline]
    #   Кнопка сохранения сверху
    save_on_top = True
    #   Добавляем конопку сохранить как новый объект, карточка изменения не закрывается, все данные в полях остаются,
    #   остается только изменить старые данные на новые и сохранить (делается в случае если новому фильму надо изменить
    #   только одно значение, а остальные оставить такими же)
    save_as = True
    #   Позволяет выбрать поле для редактирования прямо в таблице, без необходимости открывать карточку. в нашем случае
    #   это draft (черновик)
    list_editable = ('draft',)
    #   ckeditor form
    form = MovieAdminForm
    #   В поле постера добавили отображение изображения постера, функцией get_image
    readonly_fields = ('get_image',)
    #   Разбиваем ячейки с полями в более удобный формат отображения (пример: 2 поля в кортеже означают 2
    #   поля стоящих рядом в карточке). Словарь где ключ и значение это одна строка в шаблоне админки
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


#   В отзывах ставим порядок таблицы, внутри свойства запрещаем к редактированию 2 поля имя и емаил
@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


#   Добавили имя и урл для отображения в таблицу админки, когда открывает Жанр
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


#   Добавили имя и возраст для отображения в таблицу админки, когда открывает Актера
@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    search_fields = ('name', 'age')
    list_display = ('name', 'age', 'get_image', 'image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60" style="border-radius:10%;"')
    get_image.short_description = 'Изображение'


#   Добавили имя и возраст для отображения в таблицу админки, когда открывает Режиссера
@admin.register(FilmDirector)
class ActorAdmin(admin.ModelAdmin):
    search_fields = ('name', 'age')
    list_display = ('name', 'age', 'get_image', 'image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60" style="border-radius:10%;"')
    get_image.short_description = 'Изображение'


#   Добавили имя и ip для отображения в таблицу админки, когда открывает Рейтинг
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'star', 'ip')


#   Добавили имя и ip для отображения в таблицу админки, когда открывает Кадры фильма
@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image', 'image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="80" style="border-radius:10%;"')
    get_image.short_description = 'Изображение'


admin.site.register(RatingStars)

