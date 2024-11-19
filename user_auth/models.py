from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Definimos los posibles roles como una tupla de tuplas para el campo Choice
    TIER_CHOICES = [
        ('tier1', 'Tier 1'),
        ('tier2', 'Tier 2'),
        ('tier3', 'Tier 3'),
        ('tier4', 'Tier 4'),
        ('tier5', 'Tier 5'),
    ]
    
    # Campo role con opciones de choice
    role = models.CharField(
        max_length=5,
        choices=TIER_CHOICES,
        default='tier1',  # El valor predeterminado es 'tier1'
    )


    def __str__(self):
        return self.username


# Opciones para el campo 'tier'
TIER_CHOICES = [
    ('tier1', 'Tier 1'),
    ('tier2', 'Tier 2'),
    ('tier3', 'Tier 3'),
    ('tier4', 'Tier 4'),
    ('tier5', 'Tier 5'),
]

class Code(models.Model):
    code = models.CharField(max_length=4, unique=True)  # Código único
    max_uses = models.PositiveIntegerField(default=5)  # Máximo de usos permitidos
    uses = models.PositiveIntegerField(default=0)  # Usos actuales
    tier = models.CharField(max_length=5, choices=TIER_CHOICES, default='tier1')  # Campo de 'tier'

    def is_valid(self):
        """Comprueba si el código aún tiene usos disponibles."""
        return self.uses < self.max_uses

    def use_code(self):
        """Incrementa el contador de usos si es válido."""
        if self.is_valid():
            self.uses += 1
            self.save()
            return True
        return False


    def __str__(self):
        return f"{self.code} ({self.uses}/{self.max_uses}) - {self.tier}"


