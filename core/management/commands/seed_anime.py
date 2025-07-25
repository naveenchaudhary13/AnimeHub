from django.core.management.base import BaseCommand
from core.models import Anime, Genre, StatusChoices
from faker import Faker
from django.utils.text import slugify
import random
from datetime import timedelta, date

fake = Faker()

class Command(BaseCommand):
    help = "Seed database with anime and genres"

    def handle(self, *args, **kwargs):
        Genre.objects.all().delete()
        Anime.objects.all().delete()

        genre_names = ['Action', 'Adventure', 'Comedy', 'Fantasy', 'Sci-Fi']
        genres = []

        for name in genre_names:
            g = Genre.objects.create(name=name)
            genres.append(g)

        anime_data = [
            "Doraemon",
            "Chhota Bheem",
            "Oswald",
            "Noddy",
            "Ninja Hattori",
            "Kiteretsu",
            "Shinchan",
            "Bandbudh Aur Budbak",
            "Oggy and the Cockroaches",
            "Tom and Jerry",
        ]

        for title in anime_data:
            anime = Anime.objects.create(
                title=title,
                description=fake.text(max_nb_chars=200),
                status=random.choice([StatusChoices.ONGOING, StatusChoices.COMPLETED]),
                release_date=date.today() - timedelta(days=random.randint(1, 1000)),
            )
            anime.genres.set(random.sample(genres, k=2))
            anime.save()

        self.stdout.write(self.style.SUCCESS("Successfully seeded anime and genres!"))
