from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField(default=0.0)  # Ensure this field is present and has a default value

    def __str__(self):
        return f"SensorData at {self.timestamp} - Temp: {self.temperature}°C, Humidity: {self.humidity}%"
