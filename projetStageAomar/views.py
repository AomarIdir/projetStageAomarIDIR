from django.utils.timezone import now
from pyexpat.errors import messages
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Prefetch, Count, Avg
from django.urls import reverse
from projetStageAomar.models import Categories, Historique_tests,Questions,Reponses
from django.contrib.auth import logout, authenticate, login
from django.core.paginator import Paginator

def index(request):
    return render(request,'index.html')
def tst(request):
    return render(request,'base.html')

#A admin
#C client


####################################
@login_required

def dashboardA_view (request):
        return render(request,'dashboardAdmin.html')

################################################
@login_required
def resultat_eleves_view(request):
    user=request.user
    if user.is_authenticated:
        #user_id = user.id
        liste_resultats_eleves=Historique_tests.objects.all().order_by('-date_du_test').prefetch_related(
            Prefetch('categorie',queryset=Categories.objects.all(),to_attr="lacategorie" ),
            Prefetch('eleve',queryset=User.objects.all(),to_attr='eleves')
        )
        #systeme de page
        paginator = Paginator(liste_resultats_eleves, 10)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        historiques={"liste_resultats_eleves":liste_resultats_eleves,
                     "page_obj":page_obj}
        return render(request,'fragments/resultatsEleves.html',historiques)
    else:
        return redirect('index')
#################################### liste les eleves inscrits
@login_required
def listeEleves_view (request):
    user=request.user
    if user.is_authenticated:
        user=User.objects.exclude(is_superuser=True)
        users={
            "users":user
        }
        return render(request,'fragments/listeEleves.html',users)
    else:
        return redirect('index')
#################################### page pour modifier un eleve
@login_required 
def modifier_eleves_view(request,id):
    formulaire=User.objects.get(id=id)
    form={"formulaire":formulaire}
    return render(request,'fragments/modifEleves.html',form)

#################################### modifier un eleve 
@login_required
def modifier_eleves(request):
    id=request.POST.get("id")
    nom=request.POST.get("last_name").upper()
    prenom=request.POST.get("first_name").capitalize()
    email=request.POST.get("email").lower()
    form=User.objects.get(id=id)
    form.last_name=nom
    form.first_name=prenom
    form.email=email
    form.save()
    return HttpResponseRedirect(reverse('listeEleves'))

#################################### page supprimer un eleve 
@login_required
def supprimer_view(request,id):
    return render(request,'fragments/alerteSupp.html',{"id":id})

#################################### supprimer un eleve 
@login_required
def supprimer_eleve(request,id):
    eleve=User.objects.get(id=id)
    eleve.delete()
    return HttpResponseRedirect(reverse('listeEleves'))

#################################### page supprimer un resultat
@login_required
def supprimer_viewr(request,id):
    return render(request,'fragments/alerteSuppD.html',{"id":id})

#################################### supprimer un resultat
def supprimer_resultats(request,id):
    result=Historique_tests.objects.get(id=id)
    result.delete()
    return HttpResponseRedirect(reverse('resultatEleves'))
#################################### Résultats agrégés
@login_required
def aggr_resultats(request):  
    nbrDeTestPasse = Categories.objects.annotate(num_tests=Count('historique_tests'),moyenne_score=Avg('historique_tests__score'))

    categories_list = [{'id': category.id, 'categorie': category.categorie, 'num_tests': category.num_tests,"moy":category.moyenne_score} 
                        for category in nbrDeTestPasse]
    
    return render(request,'fragments/resultats_agreges.html',{"categories_list":categories_list})


####################################Client/eleve
@login_required
def dashboardE_view (request):   
    user=request.user
    if user.is_authenticated:
        moyenne_scores = Historique_tests.objects.aggregate(Avg('score'))
        if moyenne_scores['score__avg'] :
            moyenne= 100 - moyenne_scores['score__avg']
        else:
            moyenne=0
        return render(request,'dashboardClient.html',{"bonne_reponse":moyenne_scores['score__avg'],"mauvaise_reponse":moyenne})
    else:
        return redirect('index')

#################################### liste les tests disponibles
@login_required
def listeTests_view(request):
    user=request.user
    if user.is_authenticated:
        categories_list=Categories.objects.all()
        return render(request,'fragments/liste_tests.html',context={"tests":categories_list})
    else:
        return redirect('index')
    

#################################### page pour passer le test
@login_required
def page_tests_view(request,id):
    user=request.user
    if user.is_authenticated:

        qsts = Questions.objects.filter(categorie=id).order_by('?').prefetch_related(
            Prefetch('reponses_set', queryset=Reponses.objects.all(), to_attr='lesreponses')
        )
        tests={
            "qsts":qsts,
            "categorie":id
        }
        return render(request,'fragments/question.html',tests)
    else:
        return redirect('index')
####################################  L'historique des tests passés par les eleve/client
@login_required
def historiqueE_view(request):
    user=request.user
    if user.is_authenticated:
        user_id = user.id
        listehistoriques=Historique_tests.objects.filter(eleve=user_id).order_by('-date_du_test').prefetch_related(
            Prefetch('categorie',queryset=Categories.objects.all(),to_attr="lacategorie" )
        )
        #systeme de page
        paginator = Paginator(listehistoriques, 10)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        historiques={"historiques":listehistoriques,
                     "page_obj":page_obj}
        return render(request,'fragments/pageHistoriques.html',historiques)
    else:
        return redirect('index')
    
#################################### Soumettre le test
@login_required
def soumettre_test(request,id):
    if request.method == 'POST':
        forms = request.POST
        user = request.user
        if user.is_authenticated:
            user_id = user.id
            eleve= User.objects.get(id=user_id)
        feedback=[]
        score = 0
        totale=0
        for key, value in forms.items():
            
            # Ignorer le csrfmiddlewaretoken
            if key == 'csrfmiddlewaretoken':
                continue

            if key.startswith("qst_"):  
                try:
                    qst_id = int(key.split("_")[1])  
                    question = Questions.objects.get(id=qst_id)

                except (ValueError, Questions.DoesNotExist):
                    continue  # Si la clé ou la question n'est pas valide, passer à la suivante

                # Récupérer l'ID de la réponse choisie par l'utilisateur
                try:
                    rsp_id = int(value)  # 'value' contient l'ID de la réponse sélectionnée
                    reponse = Reponses.objects.get(id=rsp_id)
                except (ValueError, Reponses.DoesNotExist):
                    continue  # Si la réponse n'est pas valide, passer à la suivante

                totale+=1

                if reponse.est_correct:
                    score += 1
                
                feedback.append({
                    "qst":question,
                    "rsp":reponse,
                    "rsp_correct": Reponses.objects.get(qst_id=question, est_correct=True),
                    "est_correct":reponse.est_correct
                })
        score=(score*100)/totale
        # Enregistrer le résultat du test
        print(feedback)
        categorie_instance = Categories.objects.get(id=id)
        requeteHT=Historique_tests.objects.create(eleve=eleve,categorie=categorie_instance ,score=score, date_du_test=now())
        return render(request,'fragments/reponse.html',{'feedback': feedback, 'score': score})
    return render(request, 'dashboardClient.html')
 
####################################Connexion/ inscription/ Deconnexion
def inscription_view (request):
    if request.method == "POST":
        prenom=request.POST.get("prenom").capitalize()
        nom=request.POST.get("nom").upper()
        email=request.POST.get("email").lower()
        mdp=request.POST.get("mdp")
        check=request.POST.get("agree")
        if not check:
            return HttpResponse("Vous devez accepter les termes et conditions.", status=400)
        if User.objects.filter(email=email).exists():
            messageErreur="Cet e-mail est déjà utilisé. Veuillez en choisir un autre."
            return render(request, 'inscription.html',  {"messageErreur": messageErreur})
        user=User.objects.create_user(username=email,email=email,password=mdp,first_name=prenom,last_name=nom)
        cree = {"cree": "Compte créé avec succès !"}
        user.save()   
        return render(request,"index.html",cree)
    else: 
        return render(request,'inscription.html')

####################################

def connexion(request):
    if request.method == 'POST':
        email = request.POST["email"]
        mdp = request.POST["password"]

        # Authentification de l'utilisateur
        user = authenticate(request, username=email, password=mdp)

        if user is not None:
            login(request, user)
            
            # Vérifier si l'utilisateur est un superutilisateur
            if user.is_superuser:
                # Redirection vers le dashboard des superutilisateurs
                return render(request, 'dashboardAdmin.html')
            else:
                # Redirection vers le dashboard des utilisateurs normaux
                return redirect('dashboard')
        else:
            # Message d'erreur en cas d'échec de l'authentification
            erreur = {"erreur": "Identifiants invalides. Essayez à nouveau."}
            return render(request, 'index.html', erreur)
    
    # Si la requête n'est pas un POST, afficher la page de connexion sans erreur
    return render(request, 'index.html')

####################################
def deconnexion(request):
    logout(request) 
    return redirect('index')
