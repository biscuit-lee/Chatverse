ALTER TABLE post ADD COLUMN IF NOT EXISTS search_vector tsvector
GENERATED ALWAYS AS (to_tsvector('english',content)) STORED;

CREATE INDEX IF NOT EXISTS post_search_indx ON post USING GIN(search_vector)