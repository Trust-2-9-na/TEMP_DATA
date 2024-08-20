from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SensorData
from .serializers import SensorDataSerializer
from rest_framework import status
from django.utils import timezone
from django.db.models import Avg
import json

def index(request):
    sensor_data = SensorData.objects.all()
    serializer = SensorDataSerializer(sensor_data, many=True)

    # Convert the serialized data to JSON string
    sensor_data_json = json.dumps(serializer.data)

    context = {
        'sensor_data': sensor_data_json
    }
    return render(request, 'temp/index.html', context)

class SensorDataList(APIView):
    def get(self, request, *args, **kwargs):
        sensor_data = SensorData.objects.all()
        serializer = SensorDataSerializer(sensor_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def average_sensor_data(request):
    # Get the current time
    now = timezone.now()

    # Calculate one hour ago
    one_hour_ago = now - timezone.timedelta(hours=1)

    # Query for sensor data in the last hour
    recent_data = SensorData.objects.filter(timestamp__gte=one_hour_ago)

    # Calculate average temperature and humidity
    averages = recent_data.aggregate(
        avg_temperature=Avg('temperature'),
        avg_humidity=Avg('humidity')
    )

    # Extract average values
    avg_temperature = averages['avg_temperature']
    avg_humidity = averages['avg_humidity']

    context = {
        'avg_temperature': avg_temperature,
        'avg_humidity': avg_humidity
    }

    return render(request, 'temp/average.html', context)
