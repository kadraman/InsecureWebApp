drop table users if exists cascade;
drop table products if exists cascade;

create table users
(
    id           UUID not null,
    username     varchar(255) not null,
    password     varchar(255),
    date_created timestamp,
    first_name   varchar(255) not null,
    last_name    varchar(255) not null,
    email        varchar(255) not null,
    phone        varchar(255) not null,
    address      varchar(255) default null,
    city         varchar(255) default null,
    state        varchar(255) default null,
    zip          varchar(255) default null,
    country      varchar(255) default null,
    role         varchar(255) default null,
    enabled      bit(1)       not null,
    primary key (id)
);
create table products
(
    id             UUID         not null,
    code           varchar(255) not null,
    name           varchar(255) not null,
    summary        clob         not null,
    description    clob         not null,
    image          varchar(255),
    price          float        not null,
    on_sale        bit(1)       default 0 not null,
    sale_price     float        default 0.0 not null,
    in_stock       bit(1)       default 1 not null,
    time_to_stock  integer      default 0 not null,
    rating         integer      default 1 not null,
    available      bit(1)       default 1 not null,
    primary key (id)
);
create table reviews
(
    id              UUID            not null,
    product_id      UUID            not null,
    username        varchar(255)    not null,
    review_date     datetime        default NOW(),
    comment         clob            default null,
    rating          integer         default 1 not null,
    visible         bit             not null,
    primary key (id)
);
alter table reviews
    add constraint FKproducts_product_id foreign key (product_id) references products (id) on delete cascade;

