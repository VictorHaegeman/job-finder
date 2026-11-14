# job-finder

**Un skill Claude qui fait ta recherche de stage, d'alternance ou de premier emploi à ta place, en envoyant de vraies candidatures depuis ton Gmail.**

Tu installes le skill, tu dis « lance job-finder », et il te guide : il te demande ton CV et ce que tu cherches, prépare ton suivi, puis active des runs automatiques. À chaque run, il :

1. regarde d'abord si une entreprise t'a répondu, et te prévient par notification (entretien proposé, test, demande de documents…) ;
2. cherche des offres publiées qui correspondent à ton profil ;
3. trouve des entreprises pertinentes pour des candidatures spontanées (environ 70 % de PME) ;
4. vérifie leur adresse email **sur leur site officiel** (jamais d'adresse inventée) ;
5. génère un **CV et une lettre adaptés à chaque entreprise** (PDF d'une page, sans rien ajouter qui ne soit pas dans ton vrai CV) ;
6. écrit un mail court et personnel, avec un fait précis sur l'entreprise, puis **l'envoie** ;
7. tient tout à jour dans un Google Sheet.

## Avant de commencer

Il te faut :

- **Un compte Claude** (claude.ai ou l'application). Les skills marchent sur tous les plans. Les **tâches planifiées**, qui lancent les runs tout seuls, ne sont pas disponibles partout : vérifie que tu les as dans ton application.
- **L'option « Créer et modifier des fichiers » activée** (ancien nom : « Code execution and file creation »), dans **Paramètres → Capacités**. Sans elle, aucun skill ne peut fonctionner. Sur un compte Team ou Enterprise, c'est l'administrateur qui l'active.
- **Un compte Google** : celui d'où partiront les candidatures, donc l'adresse que tu veux montrer aux recruteurs. Il servira pour Gmail, Google Drive et Google Sheets.
- **Ton CV** en PDF ou Word.
- **10 à 15 minutes** pour la configuration guidée.

## Installation (application Claude ou claude.ai)

1. Va dans les [Releases](../../releases) et télécharge **`job-finder.zip`**. Ne le dézippe pas.
2. Dans Claude, ouvre **Personnaliser → Skills** (*Customize → Skills*).
3. Clique sur **+**, puis **Créer un skill**, puis **Importer un skill** (*Upload a skill*).
4. Choisis `job-finder.zip`.
5. Vérifie que **job-finder** apparaît dans la liste et que son interrupteur est **activé**.

Si l'import est refusé sur un compte d'organisation, c'est que l'administrateur a désactivé les skills personnels : demande-lui de les autoriser.

### Avec Claude Code (terminal)

```
/plugin marketplace add VictorHaegeman/job-finder
/plugin install job-finder@job-finder
```

Ou copie le dossier `skills/job-finder` dans `~/.claude/skills/`. Les connecteurs Gmail, Drive et Sheets doivent alors être configurés comme serveurs MCP dans Claude Code.

## Première utilisation

Écris simplement :

> Lance job-finder, je cherche un stage.

Le skill déroule 6 étapes :

1. **Connecteurs** : il vérifie Gmail, Drive et Sheets, et t'aide à connecter ceux qui manquent.
2. **CV** : il le lit, te montre ce qu'il a compris, et te demande les outils que tu *ne maîtrises pas* pour ne jamais les mentionner.
3. **Recherche** : type de contrat, domaines, dates, zone, types d'entreprises.
4. **Style** : il te montre un mail, un CV et une lettre d'exemple à valider.
5. **Envoi et suivi** : il confirme l'envoi automatique (activé par défaut, 12 par run, modifiable), puis crée ton dossier Drive, ton Sheet et ton libellé Gmail.
6. **Planification** : il crée la tâche planifiée avec toi (1 à 2 runs par jour en semaine) et te rappelle d'activer les notifications sur ton téléphone. **Sans cette étape, rien ne tourne tout seul.**

Il te propose ensuite de lancer le premier run devant toi.

### Prompt de la tâche planifiée

Si tu crées la tâche à la main, colle ce prompt :

```
Lance un run job-finder pour <Prénom Nom> : utilise le skill job-finder, retrouve le profil job-finder-profil.json sur mon Google Drive et suis la procédure de run complète (actions en attente d'abord, puis candidatures, suivi dans le Sheet, notification si une entreprise a répondu).
```

Active les notifications push sur la tâche et, si ton compte le permet, l'approbation automatique. Sinon, chaque run attendra une validation que personne ne donnera.

## Les règles qu'il respecte toujours

- **Aucune adresse email inventée** : seulement celles publiées sur le site de l'entreprise.
- **Une seule prise de contact par entreprise**, jamais de relance automatique.
- **Il ne répond jamais aux recruteurs à ta place** : il te prévient, et c'est toi qui réponds.
- **Rien dans le CV qui ne soit pas dans ton vrai CV** : contrôle automatique avant chaque envoi.
- **Pièces jointes vérifiées** dans le brouillon Gmail avant chaque envoi.
- **Pas de création de compte, pas de contournement de captcha, pas de fausse information** dans les formulaires.

## Commandes utiles

- « job-finder, où j'en suis ? » : bilan des candidatures et des réponses.
- « job-finder, ajoute Bordeaux à ma zone » : modifie le profil.
- « job-finder, passe en mode brouillons » : les mails ne partent plus seuls, tu les valides dans Gmail.
- « job-finder, 20 envois par run » : modifie le rythme (évite de dépasser une quarantaine par jour).
- « job-finder, j'ai trouvé mon stage » : met la campagne en pause.

## Arrêter complètement

1. Dis « job-finder, j'ai trouvé » (ou « mets en pause ») : les prochains runs s'arrêtent tout de suite.
2. Supprime ou désactive la tâche planifiée dans l'application Claude.
3. Si tu veux, désactive le skill dans **Personnaliser → Skills**. Ton Sheet et tes PDF restent dans ton Drive.

## Problèmes fréquents

| Problème | Solution |
|---|---|
| Claude ne lance pas le skill | Vérifie que job-finder est activé dans Personnaliser → Skills et que « Créer et modifier des fichiers » est activé. Écris « utilise le skill job-finder ». |
| « Il manque le connecteur Gmail / Drive / Sheets » | Paramètres → Connecteurs → connecte le service avec le bon compte Google, puis relance. |
| Les runs planifiés ne font rien ou restent bloqués | La tâche attend une approbation : ouvre la tâche et active l'approbation automatique (*Automatically approve*), si ton compte le permet. |
| Pas de notification sur le téléphone | Active les notifications de l'application Claude dans les réglages du téléphone, et les notifications de la tâche planifiée. |
| Gmail refuse les envois | Limite d'envoi atteinte ou compte à vérifier : attends 24 h, baisse le nombre d'envois par run et vérifie ta boîte Gmail. |
| Une entreprise a répondu | C'est **toi** qui réponds, depuis Gmail. Le skill ne répond jamais à ta place ; il note la réponse dans le Sheet. |
| Le CV généré contient une erreur | Dis « job-finder, corrige mon profil : … ». Le profil est mis à jour pour les envois suivants. |

## Structure

```
.claude-plugin/          manifeste du plugin et de la marketplace
skills/job-finder/
  SKILL.md               instructions principales
  references/            onboarding, run, envoi, style, garde-fous, suivi
  scripts/               generate_docs.py (CV + LM), verify_docs.py (contrôles)
  assets/                profil et fiche entreprise d'exemple (fictifs)
```

## Vie privée

Tes données (profil, CV, suivi) restent dans **ton** Google Drive. Le dépôt ne contient aucune donnée personnelle : les exemples sont fictifs.

## Avertissement

Ce skill envoie de vrais emails en ton nom. Relis ton profil et tes premiers envois, et garde un rythme raisonnable. Tu restes responsable de ce qui est envoyé depuis ton compte.

## Licence

MIT
