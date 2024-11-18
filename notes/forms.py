from django import forms

from .models import Note



class ModifyNote(forms.ModelForm):
    tags = forms.CharField(label='Tags',required=False)
    class Meta:
        model = Note
        fields = '__all__'        
        exclude = ['date_created', 'date_modified', 'user_created', 'user_modified','archive', 'title', 'info', 'tags']

        widgets = {
            # 'tags': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        colclass = {
            # 'title': ' col-md-5 col-xs-5',
        }
        self.fields['description'].required = True
        for f in self.fields:            
            if self.fields[f] and 'class' not in self.fields[f].widget.attrs:
                self.fields[f].widget.attrs['class'] = ' form-control'
                if f in colclass:
                    self.fields[f].colclass = colclass[f]

class SearchForm(forms.Form):
    search = forms.CharField(label='Search',required=False)