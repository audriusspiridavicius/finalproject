from typing import Any
from django import forms

from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
from .models import DeliveryAddress, Account, Company

from django.forms import inlineformset_factory

User = get_user_model()
        
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
    
    error_massages = {
        "required": "Privalomas laukas"
    }
    
    password2 = forms.CharField(label="Patvirtinkite slaptažodį",max_length=100, min_length=8,
                                widget=forms.PasswordInput(),
                                validators=[validate_password],
                                help_text="Patvirtinkite slaptažodį",
                                error_messages=error_massages
                                )
    
    password = forms.CharField(label="Slaptažodis",max_length=100, min_length=8,
                               widget=forms.PasswordInput(),
                               validators=[validate_password],
                               help_text="Slaptažodis",
                               error_messages=error_massages
                               )
    email = forms.CharField(max_length=100,
                            validators=[EmailValidator("Iveskite teisingo formato elektroninį paštą"), ],
                            required=True,
                            error_messages=error_massages
                            )
    
    def clean_email(self):
        email_value = self.cleaned_data['email']
        # email_value = email_value.strip()
        
        return email_value
    
    def clean(self) -> dict[str, Any]:
        clean_data = super().clean()
        pass1 = clean_data.get('password')
        pass2 = clean_data.get('password2')
        usr = clean_data.get('email')
        
        
        
        user_exist = User.objects.filter(email=usr)
        
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
        
class DeliveryTypeForm(forms.Form):
    
    delivery_types = (('dpd', 'dpd' ),
                      ('venipak', 'venipak' ),
                      ('delivery3', 'Atsiėmimas parduotuvėje' ),
                      ('delivery4', 'Atsiėmimas sandelyje' ),
                      )
    
    delivery_type = forms.ChoiceField(
        choices=delivery_types, 
        widget=forms.RadioSelect(), 
        label='Pristatymas')
    
    class Meta:
        fields= ('delivery_type',)

        
class DeliveryDetailsForm(forms.ModelForm):
    
    country = forms.ChoiceField(label="šalis", choices=(('Lietuva','Lietuva'),))
    city = forms.CharField(label="Miestas")
    street = forms.CharField(label="Gatvė")
    house_number = forms.CharField(label="Namo numeris")
    post_code = forms.CharField(label="Pašto kodas", required=False)
    other_info = forms.CharField(label="Papildoma informacija", required=False)
    
    def clean_house_number(self):
        data = self.cleaned_data["house_number"]
        if not data.isdigit():
            raise forms.ValidationError("namo numeris privalo buti skaicius")
        
        return data
    
    
    class Meta:
        model = DeliveryAddress
        fields = ('country', 'city','street','house_number','post_code','other_info')
        
        
class PaymnetTypeForm(forms.Form):
    
    payment_types = (('cash', 'grynais' ),
                      )
    
    payment_type = forms.ChoiceField(
        choices=payment_types, 
        widget=forms.RadioSelect(), 
        label='Pasirinkite mokėjimo būdą')
    
    class Meta:
        fields= ('payment_type',)
        
        
        
class EmailForm(forms.ModelForm,forms.Form):
    
    error_massages = {
        "required": "Privalomas laukas"
    }
    
    email = forms.CharField(max_length=100,
                        validators=[EmailValidator("Iveskite teisingo formato elektroninį paštą"), ],
                        required=True,
                        error_messages=error_massages
                        )
    
    
    def clean_email(self):
        usr_email = self.cleaned_data['email']
        user_exist = User.objects.filter(email=usr_email).exists()
        
        if user_exist:
            raise forms.ValidationError(
                    "Toks Vartotojas jau egzistuoja"
                )
        return usr_email
    # def clean(self) -> dict[str, Any]:
    #     clean_data = super().clean()
    #     usr = clean_data.get('email')
        
        
        
    #     user_exist = User.objects.filter(email=usr).exists()
        
    #     if user_exist:
    #         raise forms.ValidationError(
    #                 "Toks Vartotojas jau egzistuoja"
    #             )
        
    class Meta:
        model = User
        fields = ('email',)