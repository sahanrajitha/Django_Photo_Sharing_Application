from django import forms

from .models import Catagory, Photo
#from .models import Catagory

class AddNewPhoto(forms.ModelForm):
    
    '''category = forms.CharField(
        max_length=200,
        widget= forms.TextInput(
            attrs={'class':'some_class', 
                'id':'category-input',
                'placeholder':'Enter existing category or new one.'}
        )
    )'''

    category = forms.ModelChoiceField(
        queryset=Catagory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-contsrol', 'id':'category-select'})
    )
       
    image = forms.ImageField()
    
    title = forms.CharField()

    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Photo
        fields = "__all__"


        

    
class AddNewCategory(forms.ModelForm):
    def clean_name(self,*args, **kwargs):
        name = self.cleaned_data["name"]
        if Catagory.objects.filter(name=name).exists():
            raise forms.ValidationError("Category is already exists. Try with other one.")

        return name

    class Meta:
        model=Catagory
        fields = ['name']