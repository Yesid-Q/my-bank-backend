CREATE TABLE IF NOT EXISTS "documents" (
    "id" CHAR(2) NOT NULL UNIQUE PRIMARY KEY,
    "name" VARCHAR(30) UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS "type_accounts" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS "accounts" (
    "id" UUID NOT NULL PRIMARY KEY,
    "alias" VARCHAR(40) NOT NULL,
    "bank" VARCHAR(100) NOT NULL,
    "number_account" VARCHAR(11) UNIQUE NOT NULL,
    "amount" FLOAT DEFAULT(0),
    "user_id" UUID NOT NULL,
    "type_account_id" UUID NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL PRIMARY KEY,
    "doc_number" VARCHAR(20) NOT NULL UNIQUE,
    "name" VARCHAR(100) NOT NULL,
    "lastname" VARCHAR(100) NOT NULL,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "phone" VARCHAR(20) NOT NULL UNIQUE,
    "password" VARCHAR(200) NOT NULL,
    "document_id" CHAR(2) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS "transactions" (
    "id" UUID NOT NULL PRIMARY KEY,
    "amount" FLOAT NOT NULL,
    "action" SMALLINT NOT NULL,
    "owner_id" UUID,
    "account_owner_id" UUID,
    "receiver_id" UUID NOT NULL,
    "account_receiver_id" UUID NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMPTZ
);

ALTER TABLE
    "accounts"
ADD
    CONSTRAINT fk_user_account FOREIGN KEY("user_id") REFERENCES "users"("id");

ALTER TABLE
    "accounts"
ADD
    CONSTRAINT fk_type_account FOREIGN KEY("type_account_id") REFERENCES "type_accounts"("id");

ALTER TABLE
    "users"
ADD
    CONSTRAINT fk_user_document FOREIGN KEY("document_id") REFERENCES "documents"("id");

ALTER TABLE
    "transactions"
ADD
    CONSTRAINT fk_transaction_owner FOREIGN KEY("owner_id") REFERENCES "users"("id");

ALTER TABLE
    "transactions"
ADD
    CONSTRAINT fk_account_owner FOREIGN KEY("account_owner_id") REFERENCES "accounts"("id");

ALTER TABLE
    "transactions"
ADD
    CONSTRAINT fk_transaction_receiver FOREIGN KEY("receiver_id") REFERENCES "users"("id");

ALTER TABLE
    "transactions"
ADD
    CONSTRAINT fk_account_receiver FOREIGN KEY("account_receiver_id") REFERENCES "accounts"("id");

INSERT INTO
    documents("id", "name")
VALUES
    ('ti', 'tarjeta identidad'),
    ('cc', 'cedula ciudadania'),
    ('ce', 'cedula extranjera'),
    ('pp', 'pasaporte');

INSERT INTO
    type_accounts("id", "name")
VALUES
    ('a1ec61a7-5238-410e-b385-1f704162b500', 'ahorro'),
    ('9f73680b-a3a9-4fdb-980c-b7805eb65018', 'corriente');
