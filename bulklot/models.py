from django.db import models

class LotRequest(models.Model):
    req_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)

class LotRequestTime(models.Model):
    lot_request = models.ForeignKey(LotRequest, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=40)
