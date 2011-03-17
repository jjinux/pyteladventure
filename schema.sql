create table if not exists nodes (
    id integer primary key autoincrement,

    -- The root node will have parent_id and choice set to NULL.
    parent_id integer references nodes on delete cascade,
    choice string,

    outcome string not null,
    created_at datetime not null
);

create index if not exists nodes_parent_id on nodes (parent_id);