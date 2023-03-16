from django import forms
from .models import Pojistenec, Pojisteni, Uzivatel, PojistnaUdalost, NastavitPojisteni

class PojistenecForm(forms.ModelForm):
    
    class Meta:
        model = Pojistenec
        fields = ["jmeno", "prijmeni", "email", "telefon", "ulice", "mesto", "psc"] 


class PojisteniForm(forms.ModelForm):

    class Meta:
        model = Pojisteni
        fields = ["typ_pojisteni", "popis_pojisteni"]


class PojistnaUdalostForm(forms.ModelForm):

    class Meta:
        model = PojistnaUdalost
        fields = ["pojistenec", "cislo_pojistne_udalosti", "pojistna_udalost", "vyplacena_castka"]


class NastavitPojisteniForm(forms.ModelForm):

    class Meta:
        model = NastavitPojisteni
        fields = ["pojisteni", "pojistenec", "cislo_smlouvy", "predmet_pojisteni", "datum_zacatek", "datum_konec", "castka"]
        widgets = {
            'cislo_smlouvy': forms.TextInput(attrs={'readonly': 'readonly'})
        }
        

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)
    
    
class UzivatelForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    
    class Meta:
        model = Uzivatel
        fields = ["email", "password"]