-- Create all tables with improved constraints and indexing
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    global_role TEXT NOT NULL DEFAULT 'viewer',
    password_hash TEXT NOT NULL,
    birthdate TEXT,
    profile_picture TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    wiki_roles TEXT NOT NULL DEFAULT '{}' 
);

CREATE TABLE IF NOT EXISTS wikis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    owner_id INTEGER NOT NULL,
    description TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    wiki_id INTEGER NOT NULL,
    created_by INTEGER NOT NULL,
    slug TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wiki_id) REFERENCES wikis(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    UNIQUE (wiki_id, slug)
);

-- Page history table
CREATE TABLE IF NOT EXISTS page_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    updated_by INTEGER NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comment TEXT,
    FOREIGN KEY (page_id) REFERENCES pages(id) ON DELETE CASCADE,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid_filename TEXT NOT NULL UNIQUE,
    original_filename TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    wiki_id INTEGER NOT NULL,
    uploaded_by INTEGER NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_path TEXT NOT NULL,
    FOREIGN KEY (wiki_id) REFERENCES wikis(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Junction table for page-media relationships
CREATE TABLE IF NOT EXISTS page_media (
    page_id INTEGER NOT NULL,
    media_id INTEGER NOT NULL,
    PRIMARY KEY (page_id, media_id),
    FOREIGN KEY (page_id) REFERENCES pages(id) ON DELETE CASCADE,
    FOREIGN KEY (media_id) REFERENCES media(id) ON DELETE CASCADE
);

-- Create indexes for optimized queries
CREATE INDEX IF NOT EXISTS idx_pages_wiki_slug ON pages(wiki_id, slug);
CREATE INDEX IF NOT EXISTS idx_wikis_slug ON wikis(slug);
CREATE INDEX IF NOT EXISTS idx_page_history_page ON page_history(page_id);
CREATE INDEX IF NOT EXISTS idx_media_wiki ON media(wiki_id);
CREATE INDEX IF NOT EXISTS idx_media_filename ON media(uuid_filename);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
