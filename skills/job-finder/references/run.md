# Procédure d'un run

Un run planifié n'a personne devant l'écran. Ne pose pas de question : choisis l'interprétation la plus raisonnable, note-la dans `[RÉCAP RUN]` et continue. Les seules choses qui arrêtent un run sont un connecteur manquant, une condition d'arrêt, ou un blocage d'envoi Gmail. Dans ces trois cas, envoie une notification.

## 0. Préparation

- Vérifie les connecteurs (Gmail, Drive, Sheets). S'il en manque un, notifie et arrête-toi.
- Télécharge `job-finder-profil.json` depuis Drive et garde-le en local (`profil.json`) pour les scripts.
- Installe les dépendances si besoin : `pip install reportlab pypdf`.
- Note l'heure de début du run (UTC et heure locale du candidat).

## 1. Conditions d'arrêt

- Date du jour postérieure à `envoi.fin_campagne` : écris `[FIN] campagne terminée le JJ/MM` dans le Sheet, envoie une notification de fin avec le bilan total, et arrête-toi.
- Une ligne du Sheet ou un message du candidat indique qu'il a trouvé, ou qu'il met en pause : écris `[PAUSE]` avec la raison, envoie une notification et arrête-toi. Les actions déjà en attente restent signalées dans la notification.

## 2. Lire le Sheet en entier

Lis toute la plage (A:J), enregistre le résultat dans un fichier et traite-le en Python. Construis :

- l'ensemble des entreprises déjà contactées, avec leurs noms normalisés : minuscules, sans accents, sans forme juridique (SAS, SA, SARL, Group, France…), sans ce qui est entre parenthèses ;
- les domaines email déjà utilisés ;
- le contenu des lignes spéciales du run précédent (actions en attente, réserve, entreprises sans adresse, suggestion pour la prochaine famille).

Si un ancien tableau de suivi a été fourni à l'onboarding, lis-le aussi, en lecture seule, et ajoute ses entreprises à l'ensemble.

## 3. Réponses des recruteurs et actions en attente (priorité absolue)

1. Recherche dans Gmail : `in:inbox newer_than:2d -category:promotions -category:social`, ainsi que tous les fils portant le libellé du skill qui ont un message récent.
2. Pour chaque message qui vient d'une entreprise contactée ou d'un recruteur, ouvre le fil complet (`get_thread`) et classe-le :
   - **réponse humaine** : entretien proposé, test technique, demande de documents ou de disponibilités, appel, refus motivé ;
   - **réponse automatique** : accusé de réception, absence, refus type ;
   - **rebond** (mailer-daemon) : adresse invalide.
3. Applique le libellé du skill à tout fil d'entreprise.
4. Mets à jour la colonne Statut de la ligne de l'entreprise : date, heure, résumé en une phrase et identifiant du fil.
5. Chaque réponse humaine qui demande quelque chose au candidat devient une **action** dans `[ACTIONS EN ATTENTE]`, avec un numéro, l'entreprise, ce qui est demandé, l'échéance, le fil, et l'état « répondu / pas encore répondu ». Pour savoir si le candidat a répondu, vérifie `in:sent` dans le fil. Écris « proposé le …, NON confirmé » tant que rien ne confirme. Une échéance passée sans réponse reste ouverte avec « ÉCHÉANCE DÉPASSÉE ». Une action ne se ferme que si le fil montre qu'elle est traitée, ou si le candidat le dit.
6. Une invitation de calendrier n'est pas une confirmation : c'est une proposition à accepter.

**Ne réponds jamais dans ces fils.** Si le candidat a demandé explicitement un brouillon de réponse, prépare-le sans l'envoyer et signale-le.

## 4. Volet A : offres publiées

- Sources : sites carrières des entreprises, Welcome to the Jungle, Indeed, LinkedIn (consultation publique), job boards d'écoles, France Travail, selon ce qui est accessible. Si une source refuse l'accès, note-le dans `[VOLET A]` et passe à la suivante, sans chercher à la contourner.
- Filtre selon le profil : zone, domaine, type de contrat, niveau, durée, dates. Écarte les offres publiées depuis plus de 30 jours.
- Si l'offre donne une adresse email : candidature par email (procédure `envoi.md`, en citant l'offre).
- Si l'offre demande un formulaire : remplis-le seulement s'il ne faut ni créer de compte ni passer de captcha, avec des informations exactes tirées du profil (navigateur automatisé, par exemple Playwright). Sinon, note l'offre dans `[VOLET A]` avec le lien, pour que le candidat postule lui-même.
- Ne mets jamais de fausse information dans un formulaire, par exemple une case « je suis disponible en CDI » cochée pour passer.

## 5. Volet B : candidatures spontanées

1. **Choisis une famille** d'entreprises différente du run précédent : secteur, taille, zone. La suggestion du dernier `[RÉCAP RUN]` est un bon point de départ. Commence par la `[LIGNE] réserve` du run précédent : ces entreprises sont déjà vérifiées.
2. **Constitue une liste de 20 à 30 candidates** par recherche web, annuaires (French Tech, pôles de compétitivité, CCI, salons, classements) et pages « clients » ou « partenaires » d'entreprises déjà ciblées. Si la plateforme le permet, répartis la vérification entre des sous-agents, en leur demandant uniquement de lire les sites et de rapporter adresses et faits, sans rien envoyer.
3. **Pour chaque candidate :**
   - anti-doublon : nom normalisé contre le Sheet, puis recherche Gmail `in:anywhere <domaine>` ;
   - adresse vérifiée sur le site officiel (voir `garde-fous.md`) ;
   - un **fait précis** tiré du site : produit, client, chiffre, projet récent. S'il n'y en a pas, ou si le site est presque vide, ne l'envoie pas et mets l'entreprise en réserve ;
   - pertinence : le poste visé a du sens dans cette entreprise, et elle est dans la zone.
4. Retiens au plus `envoi.par_run` cibles, dont environ 70 % de PME (selon `recherche.part_pme`).
5. Les entreprises vérifiées mais sans adresse publique vont dans `[LIGNE] sans adresse email publique`, avec le lien de leur formulaire s'il en existe un. Les entreprises valables en surplus vont dans `[LIGNE] réserve`.

## 6. Génération, contrôle, envoi

Suis `envoi.md` pour chaque cible. Traite les entreprises une par une ou par petits lots : la génération est rapide, et ce sont la vérification et l'envoi qui prennent du temps.

## 7. Après les envois

- Recherche `from:mailer-daemon newer_than:1d` : un rebond sur un envoi du jour se note sur la ligne de l'entreprise (« adresse invalide, rebond le … ») et l'adresse est retirée.
- Vérifie qu'aucun brouillon de candidature ne reste (`list_drafts` avec le mot-témoin du CV).
- Range les PDF envoyés dans le dossier Drive. Une archive par run, par exemple `candidatures_run_AAAA-MM-JJ_HHMM.tar.xz`, suffit si l'envoi fichier par fichier est trop lourd. Vérifie que la taille du fichier sur Drive est égale à celle du fichier local.
- Réécris les lignes spéciales, puis envoie la notification et le résumé (SKILL.md, section 4).
