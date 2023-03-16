from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Pojisteni(models.Model):
    typ_pojisteni = models.CharField(max_length=80, verbose_name="Typ pojištění")
    popis_pojisteni = models.CharField(max_length=400, verbose_name="Popis produktu")

    def __str__(self):
        return f"{self.typ_pojisteni}"

    class Meta:
        verbose_name = "Pojištění"
        verbose_name_plural = "Pojištění"


class Pojistenec(models.Model):
    jmeno = models.CharField(max_length=20, verbose_name="Jméno")
    prijmeni = models.CharField(max_length=50, verbose_name="Příjmení")
    email = models.CharField(max_length=50, verbose_name="E-mail")
    telefon = models.IntegerField(default=0, verbose_name="Telefon")
    ulice = models.CharField(max_length=100, verbose_name="Ulice a číslo popisné")
    mesto = models.CharField(max_length=50, verbose_name="Město")
    psc = models.IntegerField(default=0, verbose_name="PSČ")

    def __init__(self, *args, **kwargs):
        super(Pojistenec, self).__init__(*args, **kwargs)

    def __str__(self):
        return f"Jméno: {self.jmeno} {self.prijmeni}\n"

    class Meta:
        verbose_name = "Pojištěnec"
        verbose_name_plural = "Pojištěnci"


class PojistnaUdalost(models.Model):
    pojistenec = models.ForeignKey(Pojistenec, on_delete=models.CASCADE, verbose_name="Pojištěnec")
    cislo_pojistne_udalosti = models.AutoField(primary_key=True, verbose_name="Číslo pojistné události")
    pojistna_udalost = models.CharField(max_length=300, verbose_name="Pojistná událost")
    vyplacena_castka = models.FloatField(default=0, verbose_name="Vyplacená částka")

    def __str__(self):
        return f"Číslo PÚ: {self.cislo_pojistne_udalosti}, pojištěnec: {self.pojistenec.jmeno} {self.pojistenec.prijmeni}"

    class Meta:
        verbose_name = "Pojistná událost"
        verbose_name_plural = "Pojistné události"


#nastaví pojištěnci vybrané pojištění
class NastavitPojisteni(models.Model):
    pojisteni = models.ForeignKey(Pojisteni, on_delete=models.CASCADE, verbose_name= "Typ pojištění")
    pojistenec = models.ForeignKey(Pojistenec, on_delete=models.CASCADE, verbose_name= "Pojištěnec")
    cislo_smlouvy = models.AutoField(primary_key=True, verbose_name= "Čislo smlouvy")
    predmet_pojisteni = models.CharField(max_length=200, verbose_name= "Předmět pojištění")
    datum_zacatek = models.DateField(verbose_name="Platnost od")
    datum_konec = models.DateField(verbose_name="Platnost do")
    castka = models.FloatField(default=0, verbose_name="Částka")

    def __str__(self):
         return f"{self.pojisteni}"

    class Meta:
        verbose_name = "Smluvené pojištění"
        verbose_name_plural = "Smluvená pojištění"


class UzivatelManager(BaseUserManager):
    # Vytvoří uživatele
    def create_user(self, email, password):
        print(self.model)
        if email and password:
            user = self.model(email = self.normalize_email(email))
            user.set_password(password)
            user.save()
        return user
     # Vytvoří superadmina
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save()
        return user

    
class Uzivatel(AbstractBaseUser):
    email = models.EmailField(max_length=50, unique=True)
    is_admin = models.BooleanField(default=False) #zjistí, zda je uživatel admin

    class Meta:
        verbose_name = "uživatel"
        verbose_name_plural = "uživatelé"

    objects = UzivatelManager() #slouží k spravování uživatelů v aplikaci.

    USERNAME_FIELD = "email" #určuje, že email bude použit jako uživatelské jméno v Django.

    def __str__(self):
            return f"email: {self.email}"

    @property
    def is_staff(self): #pokud je uživatel správcem, is_staff vrátit True.
        return self.is_admin

    def has_perm(self, perm, obj=None): 
            return True
            # metoda zjišťuje, zda má uživatel dané specifické povolení, pro neaktivní uživatele vrací False. 
            # zde vždy vrací True, což znamená, že každý uživatel má všechna oprávnění v aplikaci.

    def has_module_perms(self, app_label): # vrací True pokud má uživatelnějaká povolení pro daný modul.
            return True