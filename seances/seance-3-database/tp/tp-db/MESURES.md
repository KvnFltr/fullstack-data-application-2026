# Mesures `EXPLAIN ANALYZE`

Les mesures sont réalisées après l'insertion des 200 000 items de test et `ANALYZE items`.
Les temps peuvent varier selon la machine et le cache PostgreSQL ; les résultats ci-dessous
correspondent à l'exécution du TP.

## Recherche exacte par titre

| Situation | Nœud observé | Temps d'exécution |
|---|---|---:|
| Avant l'index | `Seq Scan` | 31.239 ms |
| Après `CREATE INDEX items_titre_idx ON items (titre)` | `Index Scan` | 0.054 ms |

Facteur d'accélération : environ **578,5 fois** (`31.239 / 0.054`).

## Recherches complémentaires

- (a) Un `LIKE '%123456'` commence par un joker : un index B-tree ne peut pas exploiter
  efficacement le début de la chaîne, donc PostgreSQL privilégie généralement un `Seq Scan`.
- (b) `disponible = TRUE` correspond à presque toutes les lignes, tandis que `FALSE` correspond
  à très peu de lignes ; l'index est donc surtout utile pour le filtre sélectif `FALSE`.

| Requête | Nœud observé | Temps d'exécution |
|---|---|---:|
| `titre LIKE '%123456'` | `Seq Scan` | 27.560 ms |
| `disponible = TRUE` avec index | `Seq Scan` | 29.977 ms |
| `disponible = FALSE` avec index | `Index Scan` | 0.082 ms |

La recherche avec un joker en tête ne peut pas utiliser efficacement l'index B-tree sur
`titre`, d'où le `Seq Scan`. L'index sur `disponible` n'est pas intéressant pour `TRUE`
(200 004 lignes sur 200 004), mais il est utilisé pour `FALSE`, qui ne renvoie aucune ligne.
