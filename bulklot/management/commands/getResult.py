from django.core.management.base import BaseCommand
from bulklot.utils import get_results

class Command(BaseCommand):

    def handle(self, *args, **options):

        get_results()

        return

