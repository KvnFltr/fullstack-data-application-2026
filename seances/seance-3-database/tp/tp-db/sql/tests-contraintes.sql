-- Schéma initial : chacune de ces instructions doit échouer.
INSERT INTO users (email, password_hash, display_name)
VALUES ('alice@esiee.fr', 'faux', 'Alice bis');

INSERT INTO items (owner_id, titre, tarif_jour)
VALUES (999, 'Propriétaire absent', 10.00);

INSERT INTO items (owner_id, titre, tarif_jour)
VALUES (1, 'Tarif invalide', -1.00);

INSERT INTO reservations (item_id, borrower_id, date_debut, date_fin)
VALUES (1, 2, '2026-11-10', '2026-11-01');

INSERT INTO reservations (item_id, borrower_id, date_debut, date_fin, statut)
VALUES (1, 2, '2026-11-10', '2026-11-11', 'en_attente_peut_etre');

-- Schéma v2 : les cas de contrôle ci-dessous doivent échouer.

-- Extrait de l'erreur attendue : reviews_note_check.
INSERT INTO reviews (reservation_id, note, commentaire)
VALUES (1, 6, 'Note invalide');

-- Cet avis valide sert de première ligne pour tester l'unicité.
INSERT INTO reviews (reservation_id, note, commentaire)
VALUES (1, 5, 'Deuxième avis');

-- Extrait de l'erreur attendue : reviews_reservation_id_key.
INSERT INTO reviews (reservation_id, note, commentaire)
VALUES (1, 4, 'Deuxième avis');

-- Le premier tag crée la donnée de référence ; le second doit échouer.
INSERT INTO tags (libelle) VALUES ('velo');
INSERT INTO tags (libelle) VALUES ('velo');

-- Extrait de l'erreur attendue : reviews_reservation_id_fkey.
INSERT INTO reviews (reservation_id, note, commentaire)
VALUES (999, 5, 'Réservation inexistante');
