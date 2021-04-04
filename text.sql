create schema users;

alter schema users owner to postgres;

create table if not exists permissions
(
    description text,
    rule        text not null
        constraint permissions_pk
            primary key
);

create table if not exists roles
(
    name        text not null
        constraint roles_pk
            primary key,
    description text
);

create table if not exists accounts
(
    name     text    not null,
    surname  text    not null,
    password varchar not null,
    email    text    not null
        constraint accounts_pk
            primary key,
    role     text    not null
        constraint accounts_roles_name_fk
            references roles
            on update cascade
);

create table if not exists log
(
    account text                    not null
        constraint log_accounts_email_fk
            references accounts,
    time    timestamp default now() not null,
    event   text                    not null,
    constraint log_pk
        unique (account, time)
);

create table if not exists roles_permissions
(
    role   text not null
        constraint roles_permissions_roles_name_fk
            references roles
            on update cascade,
    permit text not null
        constraint roles_permissions_permissions_rule_fk
            references permissions
            on update cascade,
    constraint roles_permissions_pk
        primary key (role, permit)
);

