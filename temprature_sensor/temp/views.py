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

from django.shortcuts import render
from .models import SensorData

def index(request):
    sensor_data = SensorData.objects.all()
    serializer = SensorDataSerializer(sensor_data, many=True)
    sensor_data_json = json.dumps(serializer.data)
    return render(request, 'temp/index.html', {'sensor_data_json': sensor_data_json})
    
def charts_view(request):
    sensor_data = SensorData.objects.all()
    serialized_data = serialize('json', sensor_data)
    return render(request, 'temp/charts.html', {'sensor_data_json': serialized_data})

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
    try:
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

        # Format to two decimal points
        avg_temperature = round(avg_temperature, 2) if avg_temperature is not None else 0
        avg_humidity = round(avg_humidity, 2) if avg_humidity is not None else 0

        context = {
            'avg_temperature': avg_temperature,
            'avg_humidity': avg_humidity
        }

        return render(request, 'temp/average.html', context)
    
    except Exception as e:
        # Handle any exceptions and provide a meaningful response
        return render(request, 'temp/error.html', {'error_message': str(e)})

    


