from django.contrib import admin
from core.models import Genre, Anime, Episode


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'release_date', 'created_at')
    list_filter = ('status', 'release_date', 'genres')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('genres',)
    ordering = ('-created_at',)
    date_hierarchy = 'release_date'


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'anime', 'episode_number', 'published_at')
    list_filter = ('anime',)
    search_fields = ('title', 'anime__title')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('anime', 'episode_number')
