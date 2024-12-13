from collections import defaultdict
from django.core.exceptions import ValidationError
from utils.tools_forms import is_positive_number 

class AuthorRecipeValidator():
    
    def __init__(self, data,erros=None,ErrorClass=None):
        
        self.errors = defaultdict(list) if erros is None else erros
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()
        
          
    def clean(self,*args, **kwargs):
        data = self.data
        title = data.get('title')
        servings = data.get('servings')
        preparation_time = data.get('preparation_time')
        
        if len(title) < 5:
            self.errors['title'].append('Title mus have at least 5 chars.')
            
        if not is_positive_number(servings):
            self.errors['servings'].append("Servings must be a valid number")
            
        if not is_positive_number(preparation_time):
            self.errors['preparation_time'].append('Preparation time must be a valid number')
            
            
        if self.errors:
            raise self.ErrorClass(self.errors)
        