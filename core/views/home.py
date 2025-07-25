import re
from datetime import date
from django.views.generic import TemplateView, DetailView, ListView
from django.views import View
from django.shortcuts import get_object_or_404, render
from core.models import Anime, Genre, Episode


class HomePageView(TemplateView):
    """
        Represent the home page
        
        Attributes:
            template_name (str): The name of the template
            
        Methods:
            get_context_data: 
                Add the form to the context data
                This method is called when the view is instantiated
                Return the context data
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recommended_anime"] = Anime.objects.filter(status="ongoing")[:10]
        context["trending_anime"] = Anime.objects.order_by("-created_at")[:10]
        context["new_releases"] = Anime.objects.filter(release_date__lte=date.today()).order_by("-release_date")[:10]
        context["genres"] = Genre.objects.all()
        return context
    
    
class AnimeDetailView(DetailView):
    """
        Represent the detail page of an anime
        
        Attributes:
            template_name (str): The name of the template
            context_object_name (str): The name of the context
            slug_field (str): The name of the slug field
            slug_url_kwarg (str): The name of the slug url
            model (str): The name of the model
    """
    model = Anime
    template_name = 'anime_detail.html'
    context_object_name = 'anime'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class EpisodeDetailView(DetailView):
    """
        Represent the detail page of an episode
        
        Attributes:
            template_name (str): The name of the template
            context_object_name (str): The name of the context
            slug_field (str): The name of the slug field
            slug_url_kwarg (str): The name of the slug url
            model (str): The name of the model
            
        Methods:
            get_context_data: 
                Add the form to the context data
                This method is called when the view is instantiated
                Return the context data
            get_object: 
                Get the object
                This method is called when the view is instantiated
                Return the object
            extract_youtube_id: 
                Extract the youtube id
                This method is called when the view is instantiated
                Return the youtube id
    """
    model = Episode
    template_name = 'episode_detail.html'
    context_object_name = 'episode'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        episode = self.get_object()
        anime = episode.anime
        video_id = self.extract_youtube_id(episode.video_url)
        context['video_id'] = video_id
        context['anime'] = anime
        context['genres'] = anime.genres.all()
        return context

    def extract_youtube_id(self, url):
        match = re.search(r"(?:v=|be/)([a-zA-Z0-9_-]{11})", url)
        return match.group(1) if match else None
    
    def get_object(self):
        anime_slug = self.kwargs.get('anime_slug')
        episode_slug = self.kwargs.get('episode_slug')
        return get_object_or_404(Episode, anime__slug=anime_slug, slug=episode_slug)
    
    
class AllAnimeView(ListView):
    """
        Represent the list of all anime
        
        Attributes:
            model (str): The name of the model
            template_name (str): The name of the template
            context_object_name (str): The name of the context
            queryset (str): The name of the queryset
    """
    model = Anime
    template_name = 'all_anime.html'
    context_object_name = 'anime_list'
    queryset = Anime.objects.all().order_by('title')
    
    
class TrendingAnimeView(ListView):
    """
        Represent the list of trending anime
        
        Attributes:
            model (str): The name of the model
            template_name (str): The name of the template
            context_object_name (str): The name of the context
            queryset (str): The name of the queryset
    """
    model = Anime
    template_name = 'trending.html'
    context_object_name = 'anime_list'
    queryset = Anime.objects.order_by('-created_at')


class GenreAnimeView(View):
    """
        Represent the list of anime of a genre
        
        Attributes:
            None
            
        Methods:
            get: 
                Get the list of anime of a genre
                This method is called when the view is instantiated
                Return the list of anime
    """
    def get(self, request, genre_slug):
        genres = Genre.objects.all()
        all_anime = Anime.objects.prefetch_related('genres').all()
        context = {
            'genres': genres,
            'all_anime': all_anime,
        }
        return render(request, 'genre_anime.html', context)
    
    
class AboutView(TemplateView):
    """
        Represent the about page
        
        Attributes:
            template_name (str): The name of the template
    """
    template_name = 'about.html'