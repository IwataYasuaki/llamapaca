from django.db import models
from django.contrib.auth.models import User

class LotRequest(models.Model):
    requester = models.ForeignKey(User, verbose_name="申込者", on_delete=models.CASCADE)
    req_date = models.DateTimeField(verbose_name="申込日", auto_now_add=True)
    location = models.CharField(
                   verbose_name="場所", 
                   max_length=100,
                   choices=[('10,2', '舎人公園'),], # offset,item
                   blank=False,
                   default='舎人公園',
               )
    sport = models.CharField(
                verbose_name="種目", 
                max_length=100,
                choices=[('130', 'テニス（人工芝）'),],
                blank=False,
                default='テニス（人工芝）',
            )

class Member(models.Model):
    owner = models.ForeignKey(User, verbose_name="所有者", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="名前", max_length=100, blank=False)
    tmgbc_id = models.CharField(verbose_name="TMGBC登録番号", max_length=8, blank=False)
    tmgbc_password = models.CharField(verbose_name="TMGBCパスワード", max_length=15, blank=False)

    def __str__(self):
        return self.name

class LotRequestTime(models.Model):
    lot_request = models.ForeignKey(LotRequest, verbose_name="抽選申込", on_delete=models.CASCADE)
    member = models.ForeignKey(Member, verbose_name="メンバー", on_delete=models.DO_NOTHING)
    date = models.DateField(verbose_name="日付")
    time = models.CharField(
               verbose_name="時間帯",
               max_length=40,
               choices=[
                   ('900_1100','09:00～'),
                   ('1100_1300','11:00～'),
                   ('1300_1500','13:00～'),
                   ('1500_1700','15:00～'),
                   ('1700_1900','17:00～'),
               ]
           )

