# core/management/commands/seed_thumbnails.py

from django.core.management.base import BaseCommand
from core.models import Anime
from duckduckgo_search import ddg_images
import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse

class Command(BaseCommand):
    help = 'Seed thumbnails for all Anime without one'

    def handle(self, *args, **options):
        animes = Anime.objects.filter(thumbnail='')  # or use isnull=True if it's nullable

        for anime in animes:
            query = f"{anime.title} anime poster"
            print(f"Searching for: {query}")

            try:
                results = ddg_images(query, max_results=1)
                if not results:
                    print(f"No image found for: {anime.title}")
                    continue

                image_url = results[0]['image']
                print(f"Downloading: {image_url}")

                response = requests.get(image_url)
                if response.status_code == 200:
                    name = urlparse(image_url).path.split('/')[-1]
                    anime.thumbnail.save(name, ContentFile(response.content), save=True)
                    print(f"Saved thumbnail for: {anime.title}")
                else:
                    print(f"Failed to download: {image_url}")

            except Exception as e:
                print(f"Error for {anime.title}: {e}")
