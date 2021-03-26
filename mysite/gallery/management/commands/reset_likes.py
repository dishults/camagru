from django.core.management.base import BaseCommand

from gallery.models import Like


class Command(BaseCommand):
    help = "Delete likes and keep some."
    queryset = Like.objects.all()
    keep = 3

    def add_arguments(self, parser):
        parser.add_argument(
            '--nb', nargs='+',
            help='Specify how many likes to keep.',
        )

    def handle(self, nb, *args, **options):
        keep = nb or self.keep
        delete = max(0, self.queryset.count() - keep)
        queryset = self.queryset.order_by('id')[:delete]
        deleted = Like.objects.filter(id__in=queryset).delete()
        self.stdout.write(self.style.SUCCESS(
            f"Deleted {deleted[0]} likes. Kept: {min(self.queryset.count(), keep)}"))
