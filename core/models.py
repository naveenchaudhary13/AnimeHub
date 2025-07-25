from django.db import models
from django.utils.text import slugify


class StatusChoices(models.TextChoices):
    """
        Represent the status of an anime
    """
    ONGOING = 'ongoing', 'Ongoing'
    COMPLETED = 'completed', 'Completed'
        
        
class Genre(models.Model):
    """
        Represent a genre of an anime
        
        Attributes:
            name (str): The name of the genre
            slug (str): The slug of the genre
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Anime(models.Model):
    """
        Represent an anime model
        
        Attributes:
            title (str): The title of the anime
            slug (str): The slug of the anime
            description (str): The description of the anime
            genres (list): The genres of the anime
            status (str): The status of the anime
            thumbnail (ImageField): The thumbnail of the anime
            release_date (DateField): The release date of the anime
            created_at (DateTimeField): The creation date of the anime
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='animes')
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ONGOING
    )
    thumbnail = models.ImageField(upload_to='anime_thumbnails/', null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def episode_count(self):
        return self.episodes.count()


class Episode(models.Model):
    """
        Represent an episode of an anime
        
        Attributes:
            anime (Anime): The anime of the episode
            episode_number (int): The episode number of the episode
            title (str): The title of the episode
            slug (str): The slug of the episode
            description (str): The description of the episode
            video_url (str): The video url of the episode
            published_at (DateTimeField): The publication date of the episode
    """
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    video_url = models.URLField()
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('anime', 'episode_number')
        ordering = ['episode_number']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.anime.title}-episode-{self.episode_number}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.anime.title} - Episode {self.episode_number}"
