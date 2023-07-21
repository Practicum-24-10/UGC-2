CREATE SCHEMA test;

ALTER SCHEMA test OWNER TO app;

SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE TABLE IF NOT EXISTS test.likes (
    user_id UUID NOT NULL,
    film_id UUID NOT NULL,
    value INTEGER NOT NULL,
    PRIMARY KEY (user_id, film_id)
);

CREATE TABLE IF NOT EXISTS test.reviews (
    user_id UUID NOT NULL,
    film_id UUID NOT NULL,
    review TEXT NOT NULL,
    PRIMARY KEY (user_id, film_id)
);

CREATE TABLE IF NOT EXISTS test.bookmarks (
    film_id UUID NOT NULL,
    user_id UUID NOT NULL,
    PRIMARY KEY (film_id, user_id)
);