from django.db import models


# Modelo para la franquicia
class Franchise(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Modelo para el personaje
class Character(models.Model):
    TIER_CHOICES = [
        ("tier1", "Tier 1"),
        ("tier2", "Tier 2"),
        ("tier3", "Tier 3"),
        ("tier4", "Tier 4"),
        ("tier5", "Tier 5"),
    ]
    tier = models.CharField(
        max_length=5,
        choices=TIER_CHOICES,
        default="tier1",  # El valor predeterminado es 'tier1'
    )
    url_img = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=255)
    franchise = models.ForeignKey(
        Franchise, on_delete=models.CASCADE, related_name="characters"
    )

    def __str__(self):
        return self.name


# Modelo para las poses
class Pose(models.Model):
    name = models.CharField(max_length=255)
    prompt = models.TextField()
    TIER_CHOICES = [
        ("tier1", "Tier 1"),
        ("tier2", "Tier 2"),
        ("tier3", "Tier 3"),
        ("tier4", "Tier 4"),
        ("tier5", "Tier 5"),
    ]
    tier = models.CharField(
        max_length=5,
        choices=TIER_CHOICES,
        default="tier1",  # El valor predeterminado es 'tier1'
    )

    img_type = models.ForeignKey(
        "ImageType",  # Entre comillas porque está definido más abajo
        on_delete=models.SET_NULL,  # Corrección del atributo
        blank=True,
        null=True,
        related_name="poses",
    )

    def __str__(self):
        return self.name


# Modelo para las skins
class Skin(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="skins"
    )
    name = models.CharField(max_length=255, default="default")
    prompt = models.TextField()
    TIER_CHOICES = [
        ("tier1", "Tier 1"),
        ("tier2", "Tier 2"),
        ("tier3", "Tier 3"),
        ("tier4", "Tier 4"),
        ("tier5", "Tier 5"),
    ]
    tier = models.CharField(
        max_length=5,
        choices=TIER_CHOICES,
        default="tier1",  # El valor predeterminado es 'tier1'
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
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class URLSD(models.Model):
    url = models.URLField(unique=True)


class Tag(models.Model):
    name = models.CharField(
        max_length=50, unique=True
    )  # Nombre único para identificar el tag

    def __str__(self):
        return self.name


class Special(models.Model):
    name = models.CharField(max_length=255)
    prompt = models.TextField()
    TIER_CHOICES = [
        ("tier1", "Tier 1"),
        ("tier2", "Tier 2"),
        ("tier3", "Tier 3"),
        ("tier4", "Tier 4"),
        ("tier5", "Tier 5"),
    ]
    tier = models.CharField(
        max_length=5,
        choices=TIER_CHOICES,
        default="tier1",  # El valor predeterminado es 'tier1'
    )
    tags_required = models.ManyToManyField(
        Tag, related_name="specialsAdd", blank=True
    )  # Relación opcional
    tags_deleted = models.ManyToManyField(
        Tag, related_name="specialsDel", blank=True
    )  # Relación opcional
    # Relación muchos a muchos con Tag

    def __str__(self):
        return f"{self.name}- {self.tier}"

class SpecialPreset(models.Model):
    TIER_CHOICES = [
        ("tier1", "Tier 1"),
        ("tier2", "Tier 2"),
        ("tier3", "Tier 3"),
        ("tier4", "Tier 4"),
        ("tier5", "Tier 5"),
    ]
    name = models.CharField(max_length=255)
    tier = models.CharField(
        max_length=5,
        choices=TIER_CHOICES,
        default="tier5",  # El valor predeterminado es 'tier1'
    )
    specials = models.ManyToManyField(
        Special, related_name="presets", blank=True
    )  # Relación muchos a muchos con Special
    
    def __str__(self):
        return self.name
    


class ControlPose(models.Model):
    name = models.CharField(max_length=255)  # El nombre de la pose
    url_img = models.URLField()  # La URL de la imagen
    
    img_type = models.ForeignKey(
        ImageType,  # Ahora sin comillas porque ya está definido arriba
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="posesControl",
    )

    def __str__(self):
        return self.name

    