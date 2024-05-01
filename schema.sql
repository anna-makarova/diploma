DROP TABLE IF EXISTS complex;

create table complex
(
    id          INTEGER
        primary key autoincrement,
    title       TEXT not null,
    address     TEXT,
    price       INTEGER,
    total_floor INTEGER
);