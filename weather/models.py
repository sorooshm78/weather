from django.db import models
from django.core.cache import cache
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=City)
def delete_cache_city(sender, instance, **kwargs):
    cache.delete(instance.name)
