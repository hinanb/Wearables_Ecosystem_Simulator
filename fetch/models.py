from django.db import models

# Create your models here.


class Wearable(models.Model):
    user_name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.user_name
class Sensor(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    wearable= models.ForeignKey(Wearable, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Sensor_Values(models.Model):
    wearable = models.ForeignKey(Wearable, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value=models.CharField(max_length=500)
    timeStamp=models.CharField(max_length=500)


    def __str__(self):
        return self.value



class Configuration(models.Model):
    numberOfWearables = models.IntegerField(blank=True, null=True)
    HRVFrequency = models.IntegerField(blank=True, null=True)
    HRFrequency=models.IntegerField(blank=True, null=True)
    TemperatureFrequency=models.IntegerField(blank=True, null=True)

    BatchFrequency = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.numberOfWearables)



