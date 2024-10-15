from django.db import models


class WeatherHistory(models.Model):
    location = models.CharField(max_length=100, verbose_name="location")
    date = models.DateField(verbose_name="date")
    temperature = models.IntegerField(verbose_name="temperature")

    def __str__(self):
        return f"{self.location}, {self.temperature}, {self.date}"
