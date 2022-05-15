from datetime import date, datetime
from django.core.management.base import BaseCommand
from bulklot.utils import get_results

class Command(BaseCommand):

    def handle(self, *args, **options):

        today = date.today()
        print(today)
        print(today.day)

        print(datetime.today())

        return

