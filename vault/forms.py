from django import forms

from .models import Treasure

class ModifyTreasure(forms.ModelForm):
    # phone   = PhoneNumberField(label=_('Tālrunis'), required=True)
    # region    = forms.ModelChoiceField(label=_('Reģions'),queryset=City.objects.filter(type__in=[0,1]).order_by('type','name_lv'), widget=forms.Select(),required=False,  empty_label=None)

    # data = forms.CharField(widget=forms.Textarea(attrs={ 'rows': 1, 'cols': 1}))

    decoded_value = forms.CharField(widget=forms.Textarea(attrs={ 'rows': 1, 'cols': 1}))




    class Meta:
        model = Treasure
        fields = '__all__'        
        exclude = ['date_created', 'date_modified', 'user_created', 'user_modified','value']

        widgets = {
            'vault': forms.HiddenInput(),
            'value': forms.Textarea(attrs={ 'rows': 1, 'cols': 1})
        }




    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        colclass = {
            'title': ' col-md-5 col-xs-5',
            'decoded_value': ' col-md-5 col-xs-5',
        }


        for f in self.fields:
            # print(f)

            
            if self.fields[f] and 'class' not in self.fields[f].widget.attrs:
                self.fields[f].widget.attrs['class'] = ' form-control'

                if f in colclass:
                    self.fields[f].colclass = colclass[f]


                # self.fields[f].colclass = 'col-xs-6 col-md-6'

        #     if f in ['region','address']:
        #         self.fields[f].colclass = 'col-xs-6 col-md-6'

        #     elif f in ['type','area','land_area','name','email','phone']:
        #         self.fields[f].colclass = 'col-xs-4 col-md-4'

        #     elif f in ['description']:
        #         self.fields[f].colclass = 'col-xs-12 col-md-12'

        #     try:
        #         if self.fields[f].widget.input_type == 'select':
        #             choices = [('', '')]
        #             for c in self.fields[f].choices:
        #                 choices.append(c)
        #             self.fields[f].choices = choices
        #     except:
        #         pass