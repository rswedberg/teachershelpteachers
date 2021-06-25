CREATE TABLE questions (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  question TEXT NOT NULL
);
