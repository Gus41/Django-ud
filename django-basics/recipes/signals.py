from recipes.models import Recipe 
from django.db.models.signals import pre_delete,pre_save
from django.dispatch import receiver
import os


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
        print("Removing cover from recipe")
    except(ValueError,FileNotFoundError):
        print("Error removing cover path")


@receiver(pre_delete,sender=Recipe)
def delete_recipe_cover(sender,instance,*args, **kwargs):
    old_instance = Recipe.objects.get(pk=instance.pk)
    delete_cover(old_instance)
    

@receiver(pre_save,sender=Recipe)
def delete_recipe_old_cover(sender,instance,*args, **kwargs):
    old_instance = Recipe.objects.get(pk=instance.pk)
    new_cover = old_instance.cover != instance.cover
    if new_cover:
        delete_cover(old_instance)
    

