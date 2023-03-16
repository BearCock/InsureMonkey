from django.contrib import admin
from .models import Pojistenec, Pojisteni, PojistnaUdalost, Uzivatel, UzivatelManager  #import modelů
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# třída pro vytvoření uživatele
class UzivatelCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Uzivatel
        fields = ['email']

    def save(self, commit=True):
        if self.is_valid():
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            return user

# třída slouží k úpravě informací o uživateli
class UzivatelChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Uzivatel
        fields = ['email', 'is_admin']

    def __init__(self, *args, **kwargs):
        super(UzivatelChangeForm, self).__init__(*args, **kwargs)
        self.Meta.fields.remove("password")

# třída definuje vlastnosti a nastavení pro správu uživatelů v administrativním rozhraní.
class UzivatelAdmin(UserAdmin):
    form = UzivatelChangeForm
    add_form = UzivatelCreationForm

    list_display = ['email', 'is_admin']
    list_filter = ['is_admin']
    fieldsets = (
        (None, {'fields': ['email', 'password']}),
        ('Permissions', {'fields': ['is_admin']}),
    )

    add_fieldsets = (
        (None, {
            'fields': ['email', 'password']}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = []


#registrace modelů
admin.site.register(Pojisteni)
admin.site.register(Pojistenec)
admin.site.register(PojistnaUdalost)
admin.site.register(Uzivatel, UzivatelAdmin)
