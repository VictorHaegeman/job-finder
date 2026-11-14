# Le Google Sheet de suivi

## Colonnes

`Date | Entreprise | Poste | Lieu | Source (URL) | Email de contact | Mode | CV + LM adaptés | Statut | Notes`

Exemple de ligne de candidature :

| Colonne | Exemple |
|---|---|
| Date | 14/11/2026 |
| Entreprise | Exemple SAS (logiciel vétérinaire – CANDIDATURE SPONTANÉE) |
| Poste | Candidature spontanée – stage data / BI |
| Lieu | Lyon (69) |
| Source (URL) | https://www.exemple-sas.fr/contact |
| Email de contact | contact@exemple-sas.fr (contact générique) |
| Mode | email envoyé · brouillon à valider · formulaire soumis automatiquement · formulaire uniquement |
| CV + LM adaptés | CV_Camille_Martin_Exemple_SAS_data_BI.pdf / LM_Camille_Martin_Exemple_SAS_data_BI.pdf |
| Statut | Envoyé le 14/11/2026 à 09:52 UTC (message id …, fil …) – PJ vérifiées avant envoi – libellé appliqué |
| Notes | taille PME ~40 ; fait cité : 300 cliniques clientes |

Les mises à jour suivantes s'ajoutent dans la colonne Statut, sans effacer l'historique. Par exemple : « … | Réponse le 18/11 10:12 : entretien proposé mar. 24/11 14h, NON confirmé → action n°3 ».

Écris avec `append_values` pour les nouvelles lignes, et `update_values` sur une plage précise pour les modifications. Ne réécris jamais tout le Sheet.

## Lignes spéciales

Elles sont réécrites à chaque run, à la même place si elles existent déjà (cherche-les par leur préfixe) ou ajoutées à la fin sinon. La colonne B porte le titre, la colonne J le détail.

- `[ACTIONS EN ATTENTE] mise à jour JJ/MM HH:MM — N ouvertes` : une action numérotée par paragraphe, la plus urgente en premier. Format : `n° – Entreprise – ce qui est demandé – échéance – état (pas encore répondu / répondu le …) – fil <id>`.
- `[LIGNE] Entreprises vérifiées sans adresse email publique (run JJ/MM HH:MM)` : `Nom (ville) – raison – lien du formulaire`.
- `[LIGNE] Entreprises vérifiées en réserve (run JJ/MM HH:MM)` : `Nom – adresse vérifiée – fait précis – pourquoi pas envoyé ce run`.
- `[VOLET A] (run JJ/MM HH:MM)` : les offres trouvées et ce qui en a été fait, ainsi que les sources inaccessibles.
- `[RÉCAP RUN] JJ/MM HH:MM – exécuté de … à …` : famille ciblée, nombre d'emails envoyés (avec la liste), formulaires, rebonds, brouillons rejetés, archive Drive, notification envoyée ou non, **suggestion de famille pour le prochain run**.
- `[PAUSE]` / `[FIN]` : à écrire seulement dans ces cas-là.
