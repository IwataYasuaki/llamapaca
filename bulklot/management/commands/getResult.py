from datetime import date, timedelta
from calendar import monthrange
from django.core.management.base import BaseCommand
from bulklot.models import LotRequest, LotRequestTime, Member
from bulklot.utils import get_result, get_result_test

def judgeResult(result):
    if '当選' in result:
        return '30' # 当選(未確定)
    elif '落選' in result:
        return '50' # 落選
    else:
        return '20' # 取得失敗


class Command(BaseCommand):

    def handle(self, *args, **options):
        today = date.today()

        # 抽選結果が出る14日のみ実行
        #if not(14 <= today.day <= 16):
        if today.day != 14:
           return

        # 来月の初日と末日を取得
        mr = monthrange(today.year, today.month)[1]
        nextMonthFirst = date(today.year, today.month, 1) + timedelta(days=mr)
        mr2 = monthrange(nextMonthFirst.year, nextMonthFirst.month)[1]
        nextMonthLast = date(nextMonthFirst.year, nextMonthFirst.month, mr2)

        # 来月の抽選申込を抽出
        lrts = LotRequestTime.objects.filter(date__range=[nextMonthFirst, nextMonthLast])
        lrts = lrts.filter(status='30') # 申込完了
        old_lrts = []

        for lrt in lrts:

            # 結果取得済みの抽選申込はスキップ
            if lrt in old_lrts:
                continue 

            member = lrt.member

            # 同じメンバーの抽選申込を抽出
            lrts_member = lrts.filter(member=member)

            # 抽選結果一覧をTMGBCから取得
            try:
                results = get_result(member)
                #results = get_result_test(member)
            except Exception as e:
                print(e)
                for lrt_member in lrts_member:
                    lrt_member.result = '20' # 取得失敗
                    lrt_member.save()
                    old_lrts.append(lrt_member)
                continue

            # 申込数の不整合チェック
            if len(lrts_member) != len(results):
                print('申込数の不一致エラー (' + member.name + ')')
                print('このツール上の申込数: ' + len(lrts.member))
                print('TMGBC上の申込数: ' + len(results))
                for lrt_member in lrts_member:
                    lrt_member.result = '20' # 取得失敗
                    lrt_member.save()
                    old_lrts.append(lrt_member)
                continue

            # 同じメンバーで同じ日時の抽選申込をしているか確認
            lrts_same = lrts_member.filter(lot_request=lrt.lot_request,
                                           date=lrt.date,
                                           time=lrt.time) 

            # 同じ抽選申込をしている場合
            if len(lrts_member) == len(lrts_same):

                for i, lrt_member in enumerate(lrts_member):
                    lotYmd = lrt_member.date.strftime('%Y年%-m月%-d日')
                    lotStime = lrt_member.time[0:2].lstrip('0')

                    if lotYmd in results[i]['ymd'] and lotStime in results[i]['stime']:
                        print(lrt_member, results[i]['status'])
                        lrt_member.result = judgeResult(results[i]['status'])
                        lrt_member.save()
                    else:
                        lrt_member.result ='20' # 取得失敗 
                        lrt_member.save()

                    old_lrts.append(lrt_member)

            # 異なる抽選申込をしている場合
            else:

                for lrt_member in lrts_member:
                    lotYmd = lrt_member.date.strftime('%Y年%-m月%-d日')
                    lotStime = lrt_member.time[0:2].lstrip('0')
                    isExist = False

                    for result in results:
                        if lotYmd in result['ymd'] and lotStime in result['stime']:
                            print(lrt_member, result['status'])
                            lrt_member.result = judgeResult(result['status'])
                            lrt_member.save()
                            isExist = True
                            break
                        else:
                            continue
                        
                    if not(isExist):
                        lrt_member.result = '20' # 取得失敗
                        lrt_member.save()

                    old_lrts.append(lrt_member)

        return

