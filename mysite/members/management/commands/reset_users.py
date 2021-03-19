from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Delets all users except admin."
    queryset = User.objects.all()
    keep = 'admin'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users', nargs='+',
            help='Specify users you want to keep.',
        )

    def handle(self, users, *args, **options):
        queryset = self.queryset.exclude(username=self.keep)
        if users:
            for user in users:
                queryset = queryset.exclude(username=user)
            users.append(self.keep)
        else:
            users = self.keep
        deleted = queryset.delete()
        self.stdout.write(self.style.SUCCESS(
            f"Deleted {deleted[0]} users. Kept: {users}"))
