from django import forms
from .models import UserData
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(UserDataForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))