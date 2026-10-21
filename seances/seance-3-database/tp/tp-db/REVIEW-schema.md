# Review du schéma v2

| Point de contrôle | OK / KO | Ce que j'ai corrigé |
|---|---|---|
| Chaque table a une clé primaire | OK | Clé primaire ajoutée à chaque table, y compris la clé composite de `item_tags`. |
| Les clés étrangères sont déclarées avec `REFERENCES` | OK | Toutes les relations sont déclarées explicitement. |
| Les `ON DELETE` sont explicites et cohérents avec le métier | OK | Cascades sur les dépendances de possession et de liaison ; l'emprunteur n'est pas en cascade. |
| La règle « un seul avis par réservation » est garantie par une contrainte `UNIQUE` | OK | `reviews_reservation_id_key`. |
| La note est bornée par un `CHECK (note BETWEEN 1 AND 5)` | OK | `reviews_note_check`. |
| La table de liaison item/tag a une clé primaire composite | OK | `item_tags_pkey` sur `(item_id, tag_id)`. |
| Le libellé de tag est `UNIQUE` | OK | `tags_libelle_key`. |
| Les contraintes sont nommées | OK | Chaque contrainte ajoutée possède un nom explicite. |
| Des index existent sur les clés étrangères | OK | Index ajoutés sur `reviews.reservation_id` et `item_tags.tag_id`, les autres existaient déjà. |
| Le non-chevauchement est réellement garanti | OK | Contrainte d'exclusion `reservations_active_no_overlap` avec `daterange`. |
| Aucun type flottant pour un montant, aucun `TIMESTAMP` sans fuseau | OK | Montants en `NUMERIC` et horodatages en `TIMESTAMPTZ`. |

## Suppression d'un utilisateur

Le matériel possédé par un utilisateur est supprimé avec lui, mais un utilisateur emprunteur n'est
pas supprimable si son historique de réservations le référence. C'est préférable pour GearShare :
supprimer un compte ne doit pas effacer l'historique des prêts réalisés sur son matériel ni ses
propres emprunts.

## Règle métier non exprimée par une contrainte de ligne

Un avis est prévu après une réservation terminée. La clé étrangère et l'unicité sont garanties par
la base, mais la vérification du statut `terminee` dépend d'une autre table et reste une règle de
service applicatif.
