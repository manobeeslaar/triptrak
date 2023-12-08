from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()

# Create your models here.
class Trip(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=2)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trips")
    
    def __str__(self):
        return f"{self.city}, {self.country}"

class Note (models.Model):
    EXCURSIONS = (
        ("event", "Event"),
        ("dining", "Dining"),
        ("lodging", "Lodging"),
        ("transportation", "Transportation"),
        ("other", "Other"),
    )
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="notes")
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=100, choices=EXCURSIONS)
    img = models.ImageField(upload_to="notes/", blank=True, null=True, default="notes/default.png")
    rating = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    def __str__(self):
        return f"{self.name} - {self.trip.city}"