# Review de la ressource `reservations`

| **Point de contrôle**                                             | **OK / KO** | **Ce que j'ai corrigé**                                                                                     |
|-------------------------------------------------------------------|-------------|-------------------------------------------------------------------------------------------------------------|
| Les codes de statut correspondent à la spec (201, 404, 409)       | OK          | -                                                                                                           |
| `response_model` présent sur les 4 routes                         | OK          | -                                                                                                           |
| La validation `date_fin > date_debut` est dans le schéma Pydantic | KO          | Ajouté un validateur Pydantic après validation des champs pour éviter une erreur si une date est invalide. |
| Le router n'accède pas au stockage de `items`                     | OK          | -                                                                                                           |
| Pas d'`async def` sans `await`                                    | OK          | -                                                                                                           |
| Aucune dépendance ajoutée dans `requirements.txt` (ou justifiée) | OK          | -                                                                                                           |
| Les routes littérales sont déclarées avant les routes paramétrées | KO          | `POST /{reservation_id}/annuler` avant `GET /{reservation_id}`          |
| Réponse cohérente pour `POST /reservations/999/annuler`           | OK          | -                                                                                                           |
