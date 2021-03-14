from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from datetime import datetime, timedelta
import ipdb
import pytz


class Command(BaseCommand):
    help = "Delete inactive users that haven't confirmed their account within given period."
    queryset = User.objects.all()

    def add_arguments(self, parser):
        parser.add_argument(
            '--days', type=int, default=30,
            help='Specify number of days after which older accounts will be deleted (default=30)',
        )

    def handle(self, days, *args, **options):
        period = datetime.now(pytz.utc) - timedelta(days)
        deleted = self.queryset.filter(
            date_joined__lt=period).filter(is_active=False).delete()
        self.stdout.write(self.style.SUCCESS(
            f"Successfully deleted {deleted[0]} user(s)"))
