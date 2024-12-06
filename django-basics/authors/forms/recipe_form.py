from django import forms
from recipes.models import Recipe
from collections import defaultdict
from django.core.exceptions import ValidationError
from utils.tools_forms import is_positive_number 

class AuthorRecipeForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.form_errors = defaultdict(list) # empty list
        
        
    
    class Meta:
        model = Recipe
        fields = ('title','description','preparation_time','preparation_time_unit','servings','servings_unit','preparation_steps','cover')
        
        widgets = {
            'cover': forms.FileInput(),
            'servings_unit' : forms.Select(
                # Display - Value
                choices=(
                    ('Porções','Porções'),
                    ('Pedaços','Pedaços'),
                    ('Pessoas','Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ("Minutos","Minutos"),
                    ("Horas","Horas"),
                )
            )
        }
        
    def clean(self,*args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        servings = cleaned_data.get('servings')
        preparation_time = cleaned_data.get('preparation_time')
        
        if len(title) < 5:
            self.form_errors['title'].append('Title mus have at least 5 chars.')
            
        if not is_positive_number(servings):
            self.form_errors['servings'].append("Servings must be a valid number")
            
        if not is_positive_number(preparation_time):
            self.form_errors['preparation_time'].append('Preparation time must be a valid number')
            
            
        if self.form_errors:
            raise ValidationError(self.form_errors)
        
        
        return super_clean