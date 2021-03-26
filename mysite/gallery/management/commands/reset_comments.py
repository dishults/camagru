from django.core.management.base import BaseCommand

from gallery.models import Comment


class Command(BaseCommand):
    help = "Delete comments and keep some."
    queryset = Comment.objects.all()
    keep = 3

    def add_arguments(self, parser):
        parser.add_argument(
            '--nb', type=int,
            help='Specify how many comments to keep.',
        )

    def handle(self, nb, *args, **options):
        keep = nb or self.keep
        delete = max(0, self.queryset.count() - keep)
        queryset = self.queryset.order_by('id')[:delete]
        deleted = Comment.objects.filter(id__in=queryset).delete()
        self.stdout.write(self.style.SUCCESS(
            f"Deleted {deleted[0]} comments. Kept: {keep}"))
