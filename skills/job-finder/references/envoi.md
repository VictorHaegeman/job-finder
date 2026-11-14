# Procédure d'envoi d'une candidature

Chaque étape protège d'une erreur réelle déjà rencontrée : mauvaise pièce jointe, PDF de deux pages, doublon, brouillon oublié. Ne saute pas d'étape pour gagner du temps.

## 1. Fichier JSON de l'entreprise

Crée un fichier `jobs/<slug>.json` au format de `assets/job.exemple.json` :

- `slug` : `<Entreprise>_<domaine>`, sans accents ni espaces. Il donne les noms de fichiers `CV_<Prénom>_<Nom>_<slug>.pdf` et `LM_<Prénom>_<Nom>_<slug>.pdf`, propres et lisibles par le recruteur ;
- `cv_title` : le poste visé, la durée et la disponibilité ;
- `cv_profile` : 2 à 3 phrases adaptées à l'entreprise, construites uniquement à partir du CV ;
- `cv_skills` et `cv_projects` : des **clés** du catalogue du profil, dans l'ordre le plus pertinent pour cette entreprise. Le texte libre est possible, mais seulement pour reformuler un élément du CV ;
- `body` : la lettre (voir `style-mails.md`) ;
- `lm_closing` : la formule de politesse, qui contient le mot-témoin de la lettre ;
- `subject` et `mail_body` : l'objet et le corps du mail.

## 2. Générer et contrôler

```bash
python3 scripts/generate_docs.py --profile profil.json --jobs jobs/
python3 scripts/verify_docs.py --profile profil.json --jobs jobs/
```

Si `verify_docs.py` sort en erreur, corrige le JSON (texte trop long, outil non maîtrisé cité…) et recommence. Ne passe jamais à l'étape suivante avec un échec. Relis aussi une fois le texte extrait de la lettre : nom de l'entreprise correct, aucun reste d'une autre entreprise.

## 3. Créer le brouillon et vérifier les pièces jointes

1. `create_draft` avec le destinataire, l'objet, le corps et **les deux PDF en pièces jointes** (encodés en base64, type `application/pdf`, avec les noms de fichiers ci-dessus).
2. Vérifie que le brouillon est trouvable par le contenu des pièces jointes :
   - `list_drafts` avec la requête `<mot_temoin_cv> to:<destinataire>` doit renvoyer ce brouillon : le CV est bien attaché ;
   - `list_drafts` avec la requête `<mot_temoin_lm> to:<destinataire>` doit renvoyer ce brouillon : la lettre est bien attachée.

   Gmail indexe le texte des PDF non compressés, et c'est pour ça que le générateur ne les compresse pas. L'indexation peut prendre quelques secondes : réessaie une ou deux fois avant de conclure à un échec.
3. Si l'une des deux recherches échoue : supprime le brouillon, recrée-le une fois. S'il échoue encore, n'envoie pas et note « brouillon rejeté : pièce jointe non vérifiée ».

## 4. Envoyer (mode « auto », le mode par défaut)

1. Fais un dernier anti-doublon : `in:sent newer_than:3d` sur le domaine de l'entreprise.
2. `send_message` avec l'identifiant du brouillon.
3. Applique le libellé du skill au fil.
4. Ajoute la ligne dans le Sheet (format dans `suivi.md`), avec l'heure d'envoi, l'identifiant du message et celui du fil.

**Mode « brouillons »** : arrête-toi après l'étape 3, applique le libellé et ajoute la ligne avec Mode = « brouillon à valider ». Dans le résumé et la notification, liste les brouillons prêts. Dans ce mode, les brouillons restent volontairement en place : la règle « aucun brouillon en fin de run » ne s'applique qu'au mode auto.

## 5. Si Gmail refuse l'envoi

Si l'envoi est refusé (permission, limite de quota, compte suspendu), ne réessaie pas en boucle. Supprime les brouillons non envoyés, ou laisse-les en signalant clairement qu'ils attendent. Envoie une notification qui explique le blocage et ce que le candidat doit faire. Note-le dans `[RÉCAP RUN]`.

Rythme : Gmail tolère sans problème une quinzaine d'envois personnalisés par run. Au-delà de 40 à 50 par jour, le risque d'être classé comme spam augmente. Ne dépasse pas `envoi.par_run` × 2 runs par jour sans que le candidat l'ait demandé.
