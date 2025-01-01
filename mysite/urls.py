"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from projetStageAomar import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("base/", views.tst, name="base"),
    path("__reload__/", include("django_browser_reload.urls")),

##############eleve/client
    path('dashboard/', views.dashboardE_view, name='dashboard'),
    path('dashboard/liste_tests',views.listeTests_view,name='listeTests'),
    path('dashboard/liste_tests/<int:id>/test_soumis',views.soumettre_test,name='soumettreTests'),
    path('dashboard/page_historiques',views.historiqueE_view,name='pageHistoriques'),
    path('dashboard/pageTests/<int:id>', views.page_tests_view, name='pageTests'),

##############admin
    path('dashadmin/', views.dashboardA_view, name='dashboardA_view'),
    path('dashadmin/listEleves',views.listeEleves_view,name='listeEleves'),
    path('dashadmin/resultatEleves',views.resultat_eleves_view,name='resultatEleves'),
    path('dashadmin/resultats_agreges',views.aggr_resultats,name='resultatagr'),
    path('dashadmin/listEleves/modifier_eleve/<int:id>',views.modifier_eleves_view,name='modifEleves'),
    path('dashadmin/listEleves/modifier_eleve/',views.modifier_eleves,name='modifierEleves'),
    #sup eleve
    path('dashadmin/listEleves/supprimer_view/<int:id>',views.supprimer_view,name='suppEleves_view'),
    path('dashadmin/listEleves/supprimer_view/supprimer_eleve/<int:id>',views.supprimer_eleve,name='suppEleves'),
    #sup resultats
    path('dashadmin/resultatEleves/supprimer_view/<int:id>',views.supprimer_viewr,name='suppResults_view'),
    path('dashadmin/resultatEleves/supprimer_view/supprimer_resultat/<int:id>',views.supprimer_resultats,name='suppResults'),

################connexion
    path('inscription/', views.inscription_view, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path("deconnexion/", views.deconnexion, name="deconnexion"),
]
