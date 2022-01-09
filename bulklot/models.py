from django.db import models

class LotRequest(models.Model):
    req_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(
                   max_length=100,
                   choices=[('10,2', '舎人公園'),], # offset,item
                   blank=False,
                   default='舎人公園',
               )
    sport = models.CharField(
                max_length=100,
                choices=[('130', 'テニス（人工芝）'),],
                blank=False,
                default='テニス（人工芝）',
            )

class LotRequestTime(models.Model):
    lot_request = models.ForeignKey(LotRequest, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(
               max_length=40,
               choices=[
                   ('900_1100','09:00～'),
                   ('1100_1300','11:00～'),
                   ('1300_1500','13:00～'),
                   ('1500_1700','15:00～'),
                   ('1700_1900','17:00～'),
               ]
           )
