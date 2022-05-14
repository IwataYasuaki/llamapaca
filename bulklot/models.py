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

    def __str__(self):
        return self.req_date.strftime('%Y年%-m月%-d日%H:%M') + '/' + \
               self.requester.username + '/' + \
               self.get_location_display() + '/' + \
               self.get_sport_display()

class Member(models.Model):
    owner = models.ForeignKey(User, verbose_name="所有者", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="名前", max_length=100, blank=False)
    tmgbc_id = models.CharField(verbose_name="TMGBC登録番号", max_length=8, blank=False)
    tmgbc_password = models.CharField(verbose_name="TMGBCパスワード", max_length=15, blank=False)

    def __str__(self):
        return self.name

class LotRequestTime(models.Model):
    lot_request = models.ForeignKey(LotRequest, verbose_name="抽選申込", on_delete=models.CASCADE)
    member = models.ForeignKey(Member, verbose_name="メンバー", on_delete=models.SET_NULL, blank=False, null=True)
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
    status = models.CharField(
                verbose_name="ステータス", 
                max_length=40,
                choices=[
                    ('10','待機中'),
                    ('20','処理中'),
                    ('30','完了'),
                    ('40','エラー'),
                ],
                blank=False,
                default='10',
            )
    result = models.CharField(
                verbose_name="抽選結果", 
                max_length=40,
                choices=[
                    ('10','未取得'),
                    ('15','取得中'),
                    ('20','取得失敗'),
                    ('30','当選'),
                    ('40','当選(確定済)'),
                    ('50','落選'),
                ],
                blank=False,
                default='10',
            )

    def __str__(self):
        return self.lot_request.__str__() + '/' + \
               self.member.name + '/' + \
               self.date.strftime('%Y年%-m月%-d日') + '/' + \
               self.get_time_display() + '/' + \
               self.get_status_display() + '/' + \
               self.get_result_display()


