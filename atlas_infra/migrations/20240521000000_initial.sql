-- Create "users" table
CREATE TABLE "users" (
  "email" character varying(255) NOT NULL,
  "full_name" character varying(255) NOT NULL,
  "id" serial NOT NULL,
  "created_at" timestamp NOT NULL,
  PRIMARY KEY ("id")
);
-- Create index "ix_users_email" to table: "users"
CREATE UNIQUE INDEX "ix_users_email" ON "users" ("email");
-- Create "posts" table
CREATE TABLE "posts" (
  "title" character varying(200) NOT NULL,
  "body" character varying NOT NULL,
  "id" serial NOT NULL,
  "owner_id" integer NOT NULL,
  "created_at" timestamp NOT NULL,
  PRIMARY KEY ("id"),
  CONSTRAINT "posts_owner_id_fkey" FOREIGN KEY ("owner_id") REFERENCES "users" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
