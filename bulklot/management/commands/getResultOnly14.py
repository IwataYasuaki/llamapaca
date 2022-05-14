from django.core.management.base import BaseCommand
from datetime import date
from bulklot.utils import get_results

class Command(BaseCommand):

    def handle(self, *args, **options):

        # 抽選結果が出る14日のみ実行
        if date.today().day == 14:
            get_results()

        return

