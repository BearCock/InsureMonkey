from django.shortcuts import render, redirect, reverse
from django.views import generic, View
from .models import Pojistenec, Pojisteni, PojistnaUdalost, Uzivatel, NastavitPojisteni
from .forms import PojistenecForm, PojisteniForm, LoginForm, UzivatelForm, PojistnaUdalostForm, NastavitPojisteniForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


# třída vytvoři seznam pojištěnců
class Pojisteneci(generic.ListView): 
    template_name = "insuremonkey/pojistenci.html" #cesta k template
    context_object_name = "pojistenci" # pod tímto jménem budeme volat list objektů v templatu

    #vrátí seznam pojištěnců dle ID
    def get_queryset(self):
        return Pojistenec.objects.all().order_by("-id")  # seřadí pojištěnce sestupně


# založit nového pojištěnce
class NovyPojistenec(LoginRequiredMixin ,generic.edit.CreateView):
    form_class = PojistenecForm
    template_name = "insuremonkey/novy_pojistenec.html"

    # Metoda pro GET request, zobrazí formulář
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form":form})
        #"form":form" je slovník, kde klíč "form" je přiřazen hodnotě "form". 
        # Tuto hodnotu bude možné využít v šabloně a vyrenderovat formulář na webové stránce.

    # Metoda pro POST request, zkontroluje formulář, pokud je validní, vytvoří nového uživatele; 
    # pokud ne, zobrazí formulář s chybovou hláškou
    def post(self, request):
        form = self.form_class(request.POST) 
        if form.is_valid():
            form.save(commit=True)
            return redirect("pojistenci")
        return render(request, self.template_name, {"form":form})
    # Tento kód implementuje funkci POST(musí být psáno takto!) metody v Django view. V této funkci se nejprve vytvoří formulář na základě dat v požadavku POST. 
    # Poté se ověří, zda formulář je platný pomocí funkce form.is_valid(). 
    # Pokud formulář je platný, uloží se pomocí form.save(commit=True). 


# třída vytvoří náhled na aktuální informace o pojištěnci
class PojistenecActualView(generic.DetailView):
    model = Pojistenec
    template_name = "insuremonkey/pojistenec_detail.html"
    
    # metoda se volá při zobrazení detailu pojištěnce
    def get(self, request, pk):
        try:
            pojistenec = self.get_object()
        except:
            return redirect ("pojistenci")
        return render(request, self.template_name, {"pojistenec": pojistenec})
    # Metoda post se volá po odeslání formuláře a zpracovává akce na stránce. Pokud je uživatel přihlášen a klikne na tlačítko pro editaci objektu ("edit" in request.POST), 
    # je přesměrován na stránku pro úpravu objektu (return redirect("pojistenec_edit", pk = self.get_object().pk))
    def post(self, request, pk):
        if request.user.is_authenticated:
            if "edit" in request.POST:
                return redirect("pojistenec_edit", pk = self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
                    return redirect(reverse("pojistenci"))
                else:
                    obj = self.get_object()
                    print(f"Pojištěnec vymazán {obj}")
                    obj.delete()
        return redirect(reverse("pojistenci"))


# třída, umožňující editaci údajů pojištěnce
class PojistenecEdit(LoginRequiredMixin, generic.edit.CreateView):
    form_class = PojistenecForm
    template_name = "insuremonkey/novy_pojistenec.html"

    def get(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
            return redirect(reverse("pojistenci"))
        try:
            pojistenec = Pojistenec.objects.get(pk = pk)
        except:
            messages.error(request, "Tento pojištěnec neexistuje.")
            return redirect("pojistenci")
        form = self.form_class(instance=pojistenec)
        return render(request, self.template_name, {"form":form})

    def post(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
            return redirect(reverse("pojistenci"))
        form = self.form_class(request.POST)

        if form.is_valid():
            jmeno = form.cleaned_data["jmeno"]
            prijmeni = form.cleaned_data["prijmeni"]
            email = form.cleaned_data["email"]
            telefon = form.cleaned_data["telefon"]
            ulice = form.cleaned_data["ulice"]
            mesto = form.cleaned_data["mesto"]
            psc= form.cleaned_data["psc"]
            try:
                pojistenec = Pojistenec.objects.get(pk = pk)
            except:
                messages.error(request, "Tento pojištěnec neexistuje.")
                return redirect(reverse("pojistenci"))
            pojistenec.jmeno = jmeno
            pojistenec.prijmeni = prijmeni
            pojistenec.email = email
            pojistenec.telefon =  telefon
            pojistenec.ulice = ulice
            pojistenec.mesto = mesto
            pojistenec.psc = psc
            pojistenec.save()
        return redirect(reverse("pojistenci"))


# třída vytváří seznam typů pojištění
class PojisteniView(generic.ListView):
    template_name = "insuremonkey/pojisteni.html"
    context_object_name = "pojisteni"

    # volá se při načtení seznamu objektů a vrací všechny objekty modelu Pojisteni, řazené podle ID sestupně
    def get_queryset(self):
        return Pojisteni.objects.all().order_by("-id")


# třída zakládá nový typ pojištění
class NovePojisteni(LoginRequiredMixin, generic.edit.CreateView):
    form_class = PojisteniForm
    template_name = "insuremonkey/nove_pojisteni.html"

    def get(self, request):
        if not request.user.is_admin:
            messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
            return redirect(reverse("index"))
        form = self.form_class(None)
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        if not request.user.is_admin:
            messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
            return redirect(reverse("pojisteni"))
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse("pojisteni"))
        return render(request, self.template_name, {"form":form})

# třída vytvoří náhled na aktuální informace o pojištění
class PojisteniActualView(generic.DetailView):
    model = Pojisteni
    template_name = "insuremonkey/pojisteni_detail.html"

    def get(self, request, pk):
        try:
            pojisteni = self.get_object()
        except:
            return redirect ("pojisteni")
        return render(request, self.template_name, {"pojisteni": pojisteni})

    def post(self, request, pk):
        if request.user.is_authenticated:
            if "edit" in request.POST:
                return redirect("pojisteni_edit", pk = self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
                    return redirect(reverse("pojistenci"))
                else:
                    obj = self.get_object()
                    print(f"Pojištěnní vymazáno {obj}")
                    obj.delete()
        return redirect(reverse("pojisteni"))

# třída, umožňující editovat pojištění
class PojisteniEdit(LoginRequiredMixin, generic.edit.CreateView):
    form_class = PojisteniForm
    template_name = "insuremonkey/nove_pojisteni.html"

    def get(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
            return redirect(reverse("pojisteni"))
        try:
            pojisteni = Pojisteni.objects.get(pk = pk)
        except:
            messages.error(request, "Toto pojištění neexistuje.")
            return redirect("pojisteni")
        form = self.form_class(instance=pojisteni)
        return render(request, self.template_name, {"form":form})

    def post(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
            return redirect(reverse("pojisteni"))
        form = self.form_class(request.POST)

        if form.is_valid():
            typ_pojisteni = form.cleaned_data["typ_pojisteni"]
            popis_pojisteni = form.cleaned_data["popis_pojisteni"]
            try:
                pojisteni = Pojisteni.objects.get(pk = pk)
            except:
                messages.error(request, "Toto pojištění neexistuje.")
                return redirect(reverse("pojisteni"))
            pojisteni.typ_pojisteni = typ_pojisteni
            pojisteni.popis_pojisteni = popis_pojisteni
            pojisteni.save()
        return redirect(reverse("pojisteni")) # po uložení vrátí na seznam


# třída vytvoří seznam všech pojistných událostí
class PojistneUdalosti(generic.ListView):
    template_name = "insuremonkey/pojistne_udalosti.html"
    context_object_name = "pojistne_udalosti"

    def get_queryset(self):
        return PojistnaUdalost.objects.all().order_by("cislo_pojistne_udalosti")


# umožňuje vytvořit novou pojistnou událost
class NovaPojistnaUdalost(LoginRequiredMixin, generic.edit.CreateView):
    form_class = PojistnaUdalostForm
    template_name = "insuremonkey/nova_pojistna_udalost.html"

    def get(self, request):
        if not request.user.is_admin:
            messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
            return redirect(reverse("pojistne_udalosti"))
        form = self.form_class(None)
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        if not request.user.is_admin:
            messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
            return redirect(reverse("pojistne_udalosti"))
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse("pojistne_udalosti"))
        return render(request, self.template_name, {"form":form})


# třída vytvoří náhled na aktuální informace o pojistné události
class PojistnaUdalostActualView(generic.DetailView):
    model = PojistnaUdalost
    template_name= "insuremonkey/pojistna_udalost_detail.html"

    def get(self, request, pk):
        try:
            pojistna_udalost = self.get_object()
        except:
            return redirect ("pojistne_udalosti")
        return render(request, self.template_name, {"pojistnaudalost":  pojistna_udalost})

    def post(self, request, pk):
        if request.user.is_authenticated:
            if "edit" in request.POST:
                return redirect("pojistna_udalost_edit", pk = self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
                    return redirect(reverse("pojistne_udalosti"))
                else:
                    obj = self.get_object()
                    print(f"Pojistná událost vymazána. {obj}")
                    obj.delete()
        return redirect(reverse("pojistne_udalosti"))

# třída, umožňující editovat pojistnou událost
class PojistnaUdalostEdit(LoginRequiredMixin, generic.edit.CreateView):
    form_class = PojistnaUdalostForm
    template_name = "insuremonkey/nova_pojistna_udalost.html"

    def get(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
            return redirect(reverse("pojistne_udalosti"))
        try:
            pu = PojistnaUdalost.objects.get(pk = pk)
        except:
            messages.error(request, "Tato pojistná událost neexistuje.")
            return redirect("pojistne_udalosti")
        form = self.form_class(instance=pu)
        return render(request, self.template_name, {"form":form})

    def post(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
            return redirect(reverse("pojistne_udalosti"))
        form = self.form_class(request.POST)

        if form.is_valid():
            pojistenec = form.cleaned_data["pojistenec"]
            pojistna_udalost = form.cleaned_data["pojistna_udalost"]
            vyplacena_castka = form.cleaned_data["vyplacena_castka"]
            try:
                pu = PojistnaUdalost.objects.get(pk = pk)
            except:
                messages.error(request, "Tato pojistná událost neexistuje!")
                return redirect(reverse("pojistne_udalosti"))
            pu.pojistenec = pojistenec
            pu.pojistna_udalost = pojistna_udalost
            pu.vyplacena_castka = vyplacena_castka
            pu.save()
        return redirect(reverse("pojistne_udalosti")) # po uložení vrátí na seznam
    

# třída slouží k zobrazení seznamu pojistnách událostí
class PojistnaUdalostListView(generic.DetailView):
    model = PojistnaUdalost
    template_name = "insuremonkey/pojistenec_detail.html"
    context_object_name = "pojistne_udalosti"

    def get_queryset(self):
        pojistenec_pk = self.kwargs.get('pk')
        return PojistnaUdalost.objects.filter(pojistenec__pk=pojistenec_pk)
    
    
# registrace nového uživatele
class UzivatelViewRegister(generic.edit.CreateView):
    form_class = UzivatelForm
    model = Uzivatel
    template_name = "insuremonkey/registrace.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request," Jste přihlášený/á, nelze se registrovat.")
            return redirect(reverse("index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request," Jste přihlášený/á, nelze se registrovat.")
            return redirect(reverse("index"))
        form = self.form_class(request.POST)
        if form.is_valid(): #kontrola, zda je formular validni
            uzivatel = form.save(commit = False) # ulozi uzivatele, commit = FALSE, kvuli nastaveni hesla nize a jeho hashovani
            password = form.cleaned_data["password"]
            uzivatel.set_password(password)
            uzivatel.save()
            login(request, uzivatel)
            return redirect("index")

        return render(request, self.template_name, {"form": form})

# přihlášení/odhlášení uživatele
class UzivatelViewLogin(generic.edit.CreateView):
    form_class = LoginForm
    template_name = "insuremonkey/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request," Jste přihlášený/á, nelze seznovu přihlásit.")
            return redirect(reverse("index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request," Jste přihlášený/á, nelze seznovu přihlásit.")
            return redirect(reverse("index"))
        form = self.form_class(request.POST)

        if form.is_valid(): #kontrola, zda je formular validní
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "tento účet neexistuje.")
        return render(request, self.template_name, {"form": form})

def logout_user(request): # odhlášení uživatele
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.info(request, "Nelze provést odhlášení, pokud nejste přihlášeni.")
    return redirect(reverse("login"))


# jednoduchý pohled, přiřazený k šabloně "index.html"
class Index(View):
    def get(self, request):
        return render(request, "insuremonkey/index.html")


# jednoduchý pohled, přiřazený k šabloně "o_aplikaci"
class OAplikaci(View):
    def get(self, request):
        return render(request, "insuremonkey/o_aplikaci.html")


# nastaví pojištěnci požadované pojištění
class NastavitPojisteniNove(LoginRequiredMixin, generic.edit.CreateView):
    form_class = NastavitPojisteniForm
    template_name = "insuremonkey/nastavit_pojisteni.html"

    def get(self, request):
        if not request.user.is_admin:
            messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
            return redirect(reverse("pojistenec_detail"))
        pojistenec = Pojistenec.objects.get(pk=request.GET.get('pojistenec_id')) #nastaví jméno pojištěnce do kolonky pojištěnec dle jeho id
        initial_data = {'pojistenec': pojistenec} # vytvoří se instance formuláře pro nastavení pojištění pro konkrétníjo pojištěnce a vstupní data se inicializují pomocí initial_data.
        form = self.form_class(initial=initial_data)
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        if not request.user.is_admin:
            messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
            return redirect(reverse("pojistenec_detail"))
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save(commit=True)
            pojistenec_id = form.cleaned_data['pojistenec'].id
            return redirect(reverse("pojistenec_detail", kwargs={'pk': pojistenec_id}))  #ID pojištěnce, na kterého se má stránka zaměřit. Celý tento krok vytvoří návratovou URL adresu, která se předá objektu redirect() jako cílová stránka.
        return render(request, self.template_name, {"form":form})

# třída vytvoří náhled na aktuální informace pojištění, které má pojištěnec nastavené/přiřazené
class NastavitPojisteniActualView(generic.DetailView):
    model = NastavitPojisteni
    template_name = "insuremonkey/nastavit_pojisteni_detail.html"

    def get(self, request, pk):
        try:
            nastavit_pojisteni = self.get_object()
        except:
            return redirect ("pojisteni")
        return render(request, self.template_name, {"nastavit_pojisteni": nastavit_pojisteni})

    def post(self, request, pk):
        if request.user.is_authenticated:
            if "edit" in request.POST:
                return redirect("nastavit_pojisteni_edit", pk = self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
                    return redirect(reverse("pojistenec_detail"))
                else:
                    obj = self.get_object()
                    print(f"Pojištěnní vymazáno {obj}")
                    obj.delete()
        return redirect(reverse("pojistenec_detail", args=[pk])) # po vymázání psmluveného pojištění se přesměruje zpět na detail pojištěnce

# editace již přiřazeného k pojištěnci
class NastavitPojisteniEdit(LoginRequiredMixin, generic.edit.CreateView):
    form_class = NastavitPojisteniForm
    template_name = "insuremonkey/nastavit_pojisteni.html"

    def get(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
            return redirect(reverse("pojisteni"))
        try:
            edit_pojisteni = NastavitPojisteni.objects.get(pk = pk)
        except:
            messages.error(request, "Toto pojištění neexistuje.")
            return redirect("pojistenec_detail")
        form = self.form_class(instance= edit_pojisteni)
        return render(request, self.template_name, {"form":form})

    def post(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Pro tuto operaci nemáte dostatečná práva.")
            return redirect(reverse("pojistenec_detail"))
        form = self.form_class(request.POST)

        if form.is_valid():
            pojisteni = form.cleaned_data["pojisteni"]
            datum_zacatek = form.cleaned_data["datum_zacatek"]
            datum_konec = form.cleaned_data["datum_konec"]
            castka = form.cleaned_data["castka"]

            try:
                nastavit_pojisteni = NastavitPojisteni.objects.get(pk = pk)
            except:
                messages.error(request, "nelze vybrat pojištění.")
                return redirect(reverse("pojistenec_detail"))
            nastavit_pojisteni.pojisteni = pojisteni
            nastavit_pojisteni.datum_zacatek = datum_zacatek
            nastavit_pojisteni.datum_konec = datum_konec
            nastavit_pojisteni.castka = castka
            nastavit_pojisteni.save()
        return redirect(reverse("pojistenec_detail", kwargs={'pk': nastavit_pojisteni.pojistenec.pk}))
    