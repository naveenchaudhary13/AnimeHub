from django.urls import path
from core.views import HomePageView, AnimeDetailView, EpisodeDetailView, AllAnimeView, GenreAnimeView, TrendingAnimeView, AboutView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('anime/<slug:slug>/', AnimeDetailView.as_view(), name='anime_detail'),
    path('anime/<slug:anime_slug>/episode/<slug:episode_slug>/', EpisodeDetailView.as_view(), name='episode_detail'),
    path('anime/', AllAnimeView.as_view(), name='all_anime'),
    path('genre/<slug:genre_slug>/', GenreAnimeView.as_view(), name='genre_anime'),
    path('trending-anime/', TrendingAnimeView.as_view(), name='trending_anime'),
    path('about/', AboutView.as_view(), name='about'),
]
