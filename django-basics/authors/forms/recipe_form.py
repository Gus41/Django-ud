from django import forms
from recipes.models import Recipe
from authors.validators import AuthorRecipeValidator
class AuthorRecipeForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
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
    def clean(self):
        
        AuthorRecipeValidator(self.cleaned_data)
        
        return super().clean()
        
   