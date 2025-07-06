-- Users table with enhanced constraints
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL CHECK(length(username) >= 3),
    email TEXT UNIQUE NOT NULL CHECK(email LIKE '%@%'),
    global_role TEXT NOT NULL DEFAULT 'viewer' 
        CHECK(global_role IN ('viewer', 'editor', 'admin', 'superadmin')),
    password_hash TEXT NOT NULL CHECK(length(password_hash) >= 60),
    birthdate TEXT CHECK(birthdate IS NULL OR date(birthdate) IS NOT NULL),
    profile_picture TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    wiki_roles TEXT NOT NULL DEFAULT '{}' CHECK(json_valid(wiki_roles)),
    is_active BOOLEAN DEFAULT 1
);

-- Categories table with slug and color
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL CHECK(length(name) >= 2),
    slug TEXT UNIQUE NOT NULL CHECK(length(slug) >= 2),
    description TEXT DEFAULT '',
    color TEXT DEFAULT '#6b7280',
    icon TEXT DEFAULT 'folder',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Wikis table with category support
CREATE TABLE IF NOT EXISTS wikis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK(length(name) >= 2),
    slug TEXT UNIQUE NOT NULL CHECK(length(slug) >= 2),
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    description TEXT DEFAULT '',
    is_private BOOLEAN DEFAULT 0,
    cover_image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, category_id) 
);

-- Pages table with improved constraints
CREATE TABLE IF NOT EXISTS pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL CHECK(length(title) >= 1),
    content TEXT NOT NULL DEFAULT '',
    wiki_id INTEGER NOT NULL REFERENCES wikis(id) ON DELETE CASCADE,
    created_by INTEGER NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    slug TEXT NOT NULL CHECK(length(slug) >= 1),
    parent_id INTEGER REFERENCES pages(id) ON DELETE SET NULL,  -- For nested pages
    is_pinned BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (wiki_id, slug)
);

-- Page history with improved tracking (FIXED)
CREATE TABLE IF NOT EXISTS page_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id INTEGER NOT NULL REFERENCES pages(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    title TEXT NOT NULL,
    updated_by INTEGER NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comment TEXT,
    version INTEGER NOT NULL DEFAULT 0,  -- REMOVED EQUALS SIGN
    change_type TEXT CHECK(change_type IN ('create', 'edit', 'revert'))
);

-- Media table with additional metadata
CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid_filename TEXT NOT NULL UNIQUE,
    original_filename TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    file_size INTEGER NOT NULL CHECK(file_size > 0),
    wiki_id INTEGER NOT NULL REFERENCES wikis(id) ON DELETE CASCADE,
    uploaded_by INTEGER NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_path TEXT NOT NULL,
    alt_text TEXT,
    description TEXT,
    is_global BOOLEAN DEFAULT 0 
);

-- Page-media relationships
CREATE TABLE IF NOT EXISTS page_media (
    page_id INTEGER NOT NULL REFERENCES pages(id) ON DELETE CASCADE,
    media_id INTEGER NOT NULL REFERENCES media(id) ON DELETE CASCADE,
    display_order INTEGER DEFAULT 0,
    caption TEXT,
    PRIMARY KEY (page_id, media_id)
);

-- Category moderators (users who can manage wikis in a category)
CREATE TABLE IF NOT EXISTS category_moderators (
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    PRIMARY KEY (category_id, user_id)
);

-- Wiki tags for additional organization
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL CHECK(length(name) >= 2),
    color TEXT DEFAULT '#6b7280',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Wiki-tag relationships
CREATE TABLE IF NOT EXISTS wiki_tags (
    wiki_id INTEGER NOT NULL REFERENCES wikis(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (wiki_id, tag_id)
);

-- ====================== INDEXES ======================
-- User indexes
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_global_role ON users(global_role);

-- Category indexes
CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name);
CREATE INDEX IF NOT EXISTS idx_categories_slug ON categories(slug);

-- Wiki indexes
CREATE INDEX IF NOT EXISTS idx_wikis_slug ON wikis(slug);
CREATE INDEX IF NOT EXISTS idx_wikis_owner ON wikis(owner_id);
CREATE INDEX IF NOT EXISTS idx_wikis_category ON wikis(category_id);
CREATE INDEX IF NOT EXISTS idx_wikis_private ON wikis(is_private) WHERE is_private = 1;

-- Page indexes
CREATE UNIQUE INDEX IF NOT EXISTS idx_page_slugs
ON pages (wiki_id, slug);
CREATE INDEX IF NOT EXISTS idx_pages_wiki_slug ON pages(wiki_id, slug);
CREATE INDEX IF NOT EXISTS idx_pages_created_by ON pages(created_by);
CREATE INDEX IF NOT EXISTS idx_pages_parent ON pages(parent_id) WHERE parent_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_pages_pinned ON pages(is_pinned) WHERE is_pinned = 1;

-- Media indexes
CREATE INDEX IF NOT EXISTS idx_media_wiki ON media(wiki_id);
CREATE INDEX IF NOT EXISTS idx_media_filename ON media(uuid_filename);
CREATE INDEX IF NOT EXISTS idx_media_global ON media(is_global) WHERE is_global = 1;
CREATE INDEX IF NOT EXISTS idx_media_original_name ON media(original_filename);

-- History indexes
CREATE INDEX IF NOT EXISTS idx_page_history_page ON page_history(page_id);
CREATE INDEX IF NOT EXISTS idx_page_history_user ON page_history(updated_by);
CREATE INDEX IF NOT EXISTS idx_page_history_date ON page_history(updated_at);

-- ====================== TRIGGERS ======================
-- Automatically update timestamps
CREATE TRIGGER IF NOT EXISTS update_wiki_timestamp
AFTER UPDATE ON wikis
BEGIN
    UPDATE wikis SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_category_timestamp
AFTER UPDATE ON categories
BEGIN
    UPDATE categories SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Auto-increment version number for page history (FIXED)
CREATE TRIGGER IF NOT EXISTS increment_page_version
BEFORE INSERT ON page_history
FOR EACH ROW
BEGIN
    -- CORRECTED SYNTAX FOR SQLITE
    SELECT COALESCE(MAX(version), 0) + 1 
    INTO NEW.version 
    FROM page_history 
    WHERE page_id = NEW.page_id;
END;
