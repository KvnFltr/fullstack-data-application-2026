CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE reviews (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    reservation_id BIGINT NOT NULL,
    note INTEGER NOT NULL,
    commentaire TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT reviews_pkey PRIMARY KEY (id),
    CONSTRAINT reviews_reservation_id_fkey FOREIGN KEY (reservation_id)
        REFERENCES reservations (id) ON DELETE CASCADE,
    CONSTRAINT reviews_reservation_id_key UNIQUE (reservation_id),
    CONSTRAINT reviews_note_check CHECK (note BETWEEN 1 AND 5)
);

CREATE TABLE tags (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    libelle VARCHAR(50) NOT NULL,
    CONSTRAINT tags_pkey PRIMARY KEY (id),
    CONSTRAINT tags_libelle_key UNIQUE (libelle),
    CONSTRAINT tags_libelle_lowercase_check CHECK (libelle = lower(libelle))
);

CREATE TABLE item_tags (
    item_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,
    CONSTRAINT item_tags_pkey PRIMARY KEY (item_id, tag_id),
    CONSTRAINT item_tags_item_id_fkey FOREIGN KEY (item_id)
        REFERENCES items (id) ON DELETE CASCADE,
    CONSTRAINT item_tags_tag_id_fkey FOREIGN KEY (tag_id)
        REFERENCES tags (id) ON DELETE CASCADE
);

ALTER TABLE reservations
    ADD CONSTRAINT reservations_active_no_overlap
    EXCLUDE USING gist (
        item_id WITH =,
        daterange(date_debut, date_fin, '[)') WITH &&
    )
    WHERE (statut = 'active');

CREATE INDEX reviews_reservation_id_idx ON reviews (reservation_id);
CREATE INDEX item_tags_tag_id_idx ON item_tags (tag_id);
