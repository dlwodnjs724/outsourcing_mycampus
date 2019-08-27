from django import forms

from core.models import UnivRegister


class UnivRegisterForm(forms.ModelForm):
    class Meta:
        model = UnivRegister
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'placeholder': 'ex) example@',
        })
