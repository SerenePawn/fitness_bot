
CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER NOT NULL UNIQUE,
    "weight_wished" INTEGER NOT NULL,
    "status" varchar(255) NOT NULL DEFAULT 'new',
    "lang_code" varchar(3) NOT NULL,
    "ctime" timestamp NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS "weighing" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    "weight" INTEGER NOT NULL,
    "ctime" timestamp NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS "staff" (
    "user_id" INTEGER NOT NULL UNIQUE,
    "banned" BOOLEAN NOT NULL DEFAULT false,
    "is_staff" BOOLEAN NOT NULL DEFAULT false,
    "is_superadmin" BOOLEAN NOT NULL DEFAULT false
);
