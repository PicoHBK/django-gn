from django.db import models

# Modelo para la franquicia
class Franchise(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Modelo para el personaje
class Character(models.Model):
    TIER_CHOICES = [
        ('tier1', 'Tier 1'),
        ('tier2', 'Tier 2'),
        ('tier3', 'Tier 3'),
        ('tier4', 'Tier 4'),
        ('tier5', 'Tier 5'),
    ]
    tier = models.CharField(
        max_length=5,
        choices=TIER_CHOICES,
        default='tier1',  # El valor predeterminado es 'tier1'
    )
    url_img = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=255)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name='characters')
    

    def __str__(self):
        return self.name

# Modelo para las poses
class Pose(models.Model):
    name = models.CharField(max_length=255)
    prompt = models.TextField()
    TIER_CHOICES = [
        ('tier1', 'Tier 1'),
        ('tier2', 'Tier 2'),
        ('tier3', 'Tier 3'),
        ('tier4', 'Tier 4'),
        ('tier5', 'Tier 5'),
    ]
    tier = models.CharField(
        max_length=5,
        choices=TIER_CHOICES,
        default='tier1',  # El valor predeterminado es 'tier1'
    )

    def __str__(self):
        return self.name

# Modelo para las skins
class Skin(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='skins')
    name = models.CharField(max_length=255, default="default")
    prompt = models.TextField()
    TIER_CHOICES = [
        ('tier1', 'Tier 1'),
        ('tier2', 'Tier 2'),
        ('tier3', 'Tier 3'),
        ('tier4', 'Tier 4'),
        ('tier5', 'Tier 5'),
    ]
    tier = models.CharField(
        max_length=5,
        choices=TIER_CHOICES,
        default='tier1',  # El valor predeterminado es 'tier1'
    )
    url_img = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

# Modelo para los emotes
class Emote(models.Model):
    name = models.CharField(max_length=255)
    prompt = models.TextField()

    def __str__(self):
        return self.name

# Modelo para los tipos de imagen
class ImageType(models.Model):
    name = models.CharField(max_length=255)
    prompt = models.TextField()
    url_img = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class URLSD(models.Model):
    url = models.URLField(unique=True)
