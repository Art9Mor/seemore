from django.core.management.base import BaseCommand, CommandError
from content.models import Report, Content
from django.http import Http404


class Command(BaseCommand):
    help = 'Deletes all reports for a given content primary key'

    def add_arguments(self, parser):
        parser.add_argument('content_pk', type=int, help='The primary key of the content to delete reports for')

    def handle(self, *args, **options):
        content_pk = options['content_pk']
        try:
            content = Content.objects.get(pk=content_pk)

            reports_to_delete = Report.objects.filter(content_id=content_pk)
            reports_to_delete.delete()

            content.is_active = True
            content.save()

            self.stdout.write(self.style.SUCCESS('Successfully deleted reports for content with pk %s' % content_pk))
        except Content.DoesNotExist:
            raise CommandError('Content does not exist')
