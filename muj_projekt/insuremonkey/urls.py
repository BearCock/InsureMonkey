from django.urls import path, include
from . import views


urlpatterns = [
    # aplikace/pojistenci, druhá část určuje, který view se zobrazí na této stránce, 
    # třetí argument "name= "registrace"" určuje jméno této URL adresy, které lze použít v šablonách pro přesměrování na tuto stránku, 
    # např: <a href="{% url 'registrace' %}">Registrace</a>

path("", views.Index.as_view(), name="index"),
path("o_aplikaci/", views.OAplikaci.as_view(), name="o_aplikaci"),
path("registrace/", views.UzivatelViewRegister.as_view(), name= "registrace"),
path("login/", views.UzivatelViewLogin.as_view(), name="login"),
path("logout/", views.logout_user, name="logout"),

path("pojistenci/", views.Pojisteneci.as_view(), name="pojistenci"),
path("novy_pojistenec/", views.NovyPojistenec.as_view(), name="novy_pojistenec"),
path("<int:pk>/edit/", views.PojistenecEdit.as_view(), name="pojistenec_edit"),
path("<int:pk>/pojistenec_detail/", views.PojistenecActualView.as_view(), name="pojistenec_detail"), #pk = id

path("pojisteni/", views.PojisteniView.as_view(), name="pojisteni"),
path("nove_pojisteni/", views.NovePojisteni.as_view(), name="nove_pojisteni"),
path("<int:pk>/pojisteni_edit/", views.PojisteniEdit.as_view(), name="pojisteni_edit"),
path("<int:pk>/pojisteni_detail/", views.PojisteniActualView.as_view(), name="pojisteni_detail"), #pk = id


path("pojistne_udalosti/", views.PojistneUdalosti.as_view(), name="pojistne_udalosti"),
path("nova_pojistna_udalost/", views.NovaPojistnaUdalost.as_view(), name="nova_pojistna_udalost"),
path("<int:pk>/pojistna_udalost_edit/", views.PojistnaUdalostEdit.as_view(), name="pojistna_udalost_edit"),
path("<int:pk>/pojistna_udalost_detail/", views.PojistnaUdalostActualView.as_view(), name="pojistna_udalost_detail"),

path("nastavit_pojisteni/", views.NastavitPojisteniNove.as_view(), name="nastavit_pojisteni"),
path("<int:pk>/nastavit_pojisteni_detail/", views.NastavitPojisteniActualView.as_view(), name="nastavit_pojisteni_detail"),
path("<int:pk>/nastavit_pojisteni_edit/", views.NastavitPojisteniEdit.as_view(), name="nastavit_pojisteni_edit"),
path("<int:pk>/pojistne_udalosti/", views.PojistnaUdalostListView.as_view, name="pojistne_udalosti_pojistenec")

]

