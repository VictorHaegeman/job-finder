# Onboarding : première utilisation

Objectif : à la fin, le candidat a un profil complet sur son Drive, un Sheet de suivi, un libellé Gmail, une tâche planifiée active, et il sait exactement ce qui va se passer. Prévois 10 à 15 minutes de conversation.

Guide-le pas à pas, comme si c'était sa première fois avec un outil de ce genre. Annonce les étapes au départ (« on va faire 6 étapes : … »), dis où on en est à chaque étape (« étape 3/6 »), et pose les questions par petits groupes (2 à 4 à la fois, avec l'outil de questions à choix multiples s'il est disponible). Ne pose pas une question dont la réponse est déjà dans le CV.

## Étape 1/6 : présentation et connecteurs

Explique en quelques phrases ce que fait job-finder :

> Je vais chercher des entreprises qui correspondent à ce que tu cherches, trouver leur adresse sur leur site officiel, écrire à chacune un mail court avec un CV et une lettre adaptés, et **les envoyer automatiquement depuis ton Gmail**, environ 12 par run. Je tiens tout dans un Google Sheet et je te préviens par notification dès qu'une entreprise répond. Je ne réponds jamais aux recruteurs à ta place.

Vérifie ensuite que Gmail, Google Drive et Google Sheets sont connectés. Pour chaque connecteur manquant :

- dis lequel manque et à quoi il sert : Gmail pour envoyer les mails et lire les réponses, Drive pour garder ton profil et tes PDF, Sheets pour le suivi ;
- guide la connexion : dans Claude, menu Paramètres → Connecteurs → choisir le service → se connecter avec le compte Google qui enverra les candidatures. Si l'hôte fournit un outil de suggestion de connecteurs, utilise-le pour afficher directement le bouton de connexion ;
- attends que le candidat confirme, puis vérifie toi-même que les outils répondent, par exemple avec une recherche Gmail sans effet.

Insiste sur un point : **le compte Gmail connecté est celui d'où partiront les candidatures**. Il doit donc s'agir de l'adresse que le candidat veut montrer aux recruteurs.

## Étape 2/6 : le CV

Demande le CV en PDF (ou en Word). Lis-le entièrement et extrais-en :

- l'identité et les coordonnées : nom, téléphone, email, ville, liens LinkedIn/GitHub/portfolio ;
- la formation, avec les intitulés exacts ;
- les expériences, avec les intitulés, dates et missions réelles ;
- les projets ;
- les compétences techniques et les outils, **uniquement ceux qui sont écrits** ;
- les langues et les centres d'intérêt.

Montre-lui un résumé de ce que tu as compris et demande-lui de corriger. Puis pose deux questions qui comptent beaucoup pour la suite :

1. « Y a-t-il des outils ou des langages qu'on voit souvent dans ton domaine et que tu ne maîtrises pas ? » Ils iront dans `non_maitrise`, et le script de vérification bloquera tout document qui les mentionne. Propose des exemples courants dans son domaine. Le contrôle respecte les majuscules, mais évite quand même les noms d'outils qui sont aussi des mots courants du CV (par exemple « Tableau », qui bloquerait « Tableau de bord » en début de ligne). Utilise plutôt le nom complet de l'outil (« Tableau Software ») ou laisse ce cas à ta relecture.
2. « Y a-t-il quelque chose dans ton CV que tu ne veux pas mettre en avant ? »

Rédige ensuite les entrées du catalogue `cv.competences_cles` et `cv.projets` (4 à 8 entrées chacune, une ligne de 120 à 200 caractères, avec des clés courtes). Chaque run piochera dedans pour adapter le CV.

Choisis le **mot-témoin du CV** (`mot_temoin_cv`) : un mot assez rare, présent dans une ligne fixe du CV (expériences ou formation) et absent des lettres. Il sert à retrouver le brouillon Gmail par son contenu pour vérifier que la pièce jointe est bien là. Le mot-témoin de la lettre est la formule de politesse, « distinguées » en français. Vérifie que le mot-témoin du CV n'apparaît pas dans la formule de politesse.

## Étape 3/6 : ce qu'il cherche

Questions à poser, à adapter à ce que le CV dit déjà :

- type de contrat : stage, alternance, CDD, CDI, VIE ; et ce qui est exclu ;
- domaines ou métiers visés (2 à 4), et ceux qu'il ne veut pas ;
- durée, date de début, date de début au plus tard ;
- zone géographique : villes, départements, télétravail accepté ou non ;
- pour un stage : école et convention, niveau (bac+3, bac+4…) ;
- types d'entreprises : PME, startups, grands groupes ; par défaut environ 70 % de PME, parce qu'elles répondent beaucoup plus aux candidatures spontanées ;
- date de fin de campagne : au-delà, le skill s'arrête tout seul ;
- langue des candidatures : français par défaut, anglais possible.

## Étape 4/6 : style et signature

- Montre un exemple de mail (voir `style-mails.md`) écrit avec son vrai profil pour une entreprise fictive, et demande si le ton lui va : tutoiement exclu, mais plus ou moins formel.
- Fais valider la signature du mail (nom, formation, téléphone, LinkedIn).
- Génère un CV et une lettre d'exemple pour cette entreprise fictive avec `scripts/generate_docs.py`, vérifie-les avec `scripts/verify_docs.py` et envoie-lui les deux PDF pour qu'il valide la mise en page et le contenu. C'est le meilleur moment pour corriger une formulation qui ne lui ressemble pas.

## Étape 5/6 : envoi automatique et suivi

L'envoi automatique est **activé par défaut** (`envoi.mode = "auto"`, 12 envois par run). Dis-le clairement et fais-le confirmer une fois, parce que des mails vont partir en son nom :

> Les candidatures partiront automatiquement depuis ton Gmail, environ 12 par run, sans que tu les relises une par une. Chaque adresse est vérifiée sur le site officiel, chaque entreprise n'est contactée qu'une fois, et je ne réponds jamais aux recruteurs. Tu peux changer le nombre par run, ou passer en mode « brouillons à valider », quand tu veux. On garde l'envoi automatique ?

S'il préfère relire, mets `envoi.mode = "brouillons"` (voir `envoi.md`).

Crée ensuite :

1. Un dossier Drive `Job Finder – <Prénom Nom>`.
2. Le Sheet `Suivi candidatures – <Prénom Nom>` dans ce dossier, avec l'en-tête : `Date | Entreprise | Poste | Lieu | Source (URL) | Email de contact | Mode | CV + LM adaptés | Statut | Notes`. Ajoute la ligne `[ACTIONS EN ATTENTE] mise à jour JJ/MM HH:MM — aucune action`.
3. Le libellé Gmail `Job Finder – candidatures`, ou réutilise-le s'il existe.
4. Le fichier `job-finder-profil.json` dans le dossier, complet, avec les identifiants du dossier, du Sheet et du libellé dans `suivi`. Copie aussi le CV d'origine dans le dossier.

Si le candidat a déjà un tableau de suivi de candidatures, demande-lui le lien : il sera lu (sans être modifié) pour éviter de recontacter les mêmes entreprises.

## Étape 6/6 : activer la planification (ne pas sauter cette étape)

Sans planification, rien ne se passe tout seul : le skill ne tourne que quand on le lance. Explique-le clairement, puis **mets en place la tâche planifiée avec lui**.

- **Si l'hôte offre un outil de tâches planifiées** (par exemple « scheduled tasks » ou des outils de type create_trigger), propose de la créer toi-même : 1 à 2 runs par jour en semaine, à des heures choisies avec lui, et pas à l'heure pile (par exemple 9 h 47 et 14 h 13), parce que les envois à heure ronde ont l'air automatiques. Le prompt de la tâche doit se suffire à lui-même, par exemple :

  > Lance un run job-finder pour <Prénom Nom> : utilise le skill job-finder, retrouve le profil job-finder-profil.json sur mon Google Drive et suis la procédure de run complète (actions en attente d'abord, puis candidatures, suivi dans le Sheet, notification si une entreprise a répondu).

  Active les notifications push (et email s'il le souhaite). Après la création, dis-lui quel réglage d'approbation la tâche a reçu. Si les runs demandent une approbation à chaque action, explique-lui comment activer l'approbation automatique dans les réglages de la tâche, sinon les runs resteront bloqués sans personne pour valider.
- **Sinon**, guide-le pour la créer lui-même :
  - dans l'application Claude : section des tâches planifiées → nouvelle tâche → coller le prompt ci-dessus → choisir la fréquence → activer les notifications ;
  - dans Claude Code : une tâche planifiée du système (cron, launchd, planificateur de tâches) qui lance `claude -p "<prompt ci-dessus>"`.

  Donne-lui le prompt prêt à copier.
- Demande-lui de **garder les notifications activées sur son téléphone** : c'est par là qu'il apprendra qu'une entreprise veut le rencontrer.

## Clôture

Fais un récapitulatif : ce qui a été créé (avec les liens), le réglage d'envoi, l'horaire des runs et la date de fin. Propose ensuite de lancer **le premier run tout de suite**, devant lui. C'est rassurant de voir les premiers envois partir, et ça permet de corriger le tir avant que la planification prenne le relais.
