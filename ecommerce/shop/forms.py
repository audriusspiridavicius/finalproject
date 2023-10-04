from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
        
def validate_password(value):
    
    validation_errors = []
    
    has_number = any(i.isdigit() for i in value)
    has_upper_Letter = any(i.isupper() for i in value)
    has_lower_Letter = any(i.isupper() for i in value)
    has_special_symbol = any(not c.isalnum() for c in value)
    
    if not has_number:
        err = forms.ValidationError(_("Slaptazodis turi tureti bent 1 skaiciu!!!"))
        validation_errors.append(err)
    
    if not has_upper_Letter:
        err = forms.ValidationError(_("Slaptazodis turi tureti didziasias raides(A-Z)"))
        validation_errors.append(err)
        
    if not has_lower_Letter:
        err = forms.ValidationError(_("Slaptazodis turi tureti mazasias raides(a-z)"))
        validation_errors.append(err)
        
    if not has_special_symbol:
        err = forms.ValidationError("Slaptazodis turi tureti simboli(!@#$%^&*()-+?_=,<>/)", code="danger")
        validation_errors.append(err)
        
    if validation_errors:
        raise forms.ValidationError(
           validation_errors
        )
         
class RegistrationForm(forms.ModelForm):
    
    password2 = forms.CharField(max_length=100, min_length=8,
                                widget=forms.PasswordInput(),
                                validators=[validate_password]
                                )
    
    password = forms.CharField(max_length=100, min_length=8,
                               widget=forms.PasswordInput(),
                               validators=[validate_password]
                               )
    email = forms.CharField(max_length=100, validators=[EmailValidator("Iveskite teisingo formato elektroninį paštą")])
    
    def clean(self) -> dict[str, Any]:
        clean_data = super().clean()
        pass1 = clean_data.get('password')
        pass2 = clean_data.get('password2')
        usr = clean_data.get('email')
        
        
        
        user_exist = User.objects.filter(username=usr)
        
        if user_exist:
            raise forms.ValidationError(
                    "Toks Vartotojas jau egzistuoja"
                )
        
        if pass1 != pass2:
            raise forms.ValidationError(
                    "Slaptažodžiai turi sutapti!"
                )
    class Meta:
        model = User
        fields = ('email', 'password','password2')
        