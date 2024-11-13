from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = "Limpia la cache de codificaciones de rostros"

    def handle(self, *args, **kwargs):
        cache.delete("reference_encodings")
        self.stdout.write(self.style.SUCCESS("Caché de codificaciones de referencia vaciada exitosamente."))