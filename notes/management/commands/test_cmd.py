from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Test custom collectstatic override"

    def handle(self, *args, **options):
        print("Test custom collectstatic command is being executed!")