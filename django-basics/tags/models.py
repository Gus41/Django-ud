from django.db import models
from django.utils.text import slugify
import string
from random import SystemRandom



# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    

    
    
    def save(self, *args, **kwargs):
        if not self.slug:

            rand_chars = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5
                )
            )
            self.slug = slugify(f'{self.name}-{rand_chars}')
            

        return super().save(*args, **kwargs)
    
    def __str__(self):
        
        return self.name
    
