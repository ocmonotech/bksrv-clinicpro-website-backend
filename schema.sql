CREATE TABLE IF NOT EXISTS blogs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  slug VARCHAR(255) NOT NULL UNIQUE,
  excerpt TEXT,
  content LONGTEXT NOT NULL,
  cover_image VARCHAR(500),
  author VARCHAR(100),
  category VARCHAR(100) DEFAULT 'Resources',
  status ENUM('draft', 'published') DEFAULT 'draft',
  published_at DATETIME NULL,
  meta_title VARCHAR(255) NULL,
  meta_description TEXT NULL,
  meta_keywords VARCHAR(500) NULL,
  canonical_url VARCHAR(500) NULL,
  og_image VARCHAR(500) NULL,
  schema_json JSON NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_blogs_status_published_at (status, published_at),
  INDEX idx_blogs_slug (slug)
);


CREATE TABLE IF NOT EXISTS admin_us.(
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  username VARCHAR(100) UNIQUE NOT NULL,
  email VARCHAR(150) UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'super_admin',
  is_active TINYINT(1) DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


INSERT INTO admin_us.
(name, username, email, password_hash, role, is_active)
VALUES 
(
  'Super Admin',
  'ocmono',
  'admin@example.com',
  '$2b$12$ufGtcWiSAdWABo7lDKKi4uiiy685Y1eEvHSn3YA6YouhUduqZtMsG',
  'super_admin',
  1
);


CREATE TABLE IF NOT EXISTS professions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  slug VARCHAR(255) NOT NULL UNIQUE,
  description TEXT NULL,
  content LONGTEXT NULL,
  image VARCHAR(500) NULL,
  mega_menu_column INT NOT NULL DEFAULT 0,
  sort_order INT NOT NULL DEFAULT 0,
  show_on_homepage TINYINT(1) NOT NULL DEFAULT 0,
  animation_delay VARCHAR(10) NULL,
  status ENUM('draft', 'published') NOT NULL DEFAULT 'draft',
  meta_title VARCHAR(255) NULL,
  meta_description TEXT NULL,
  meta_keywords VARCHAR(500) NULL,
  canonical_url VARCHAR(500) NULL,
  og_image VARCHAR(500) NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_professions_status (status),
  INDEX idx_professions_slug (slug),
  INDEX idx_professions_menu_order (mega_menu_column, sort_order)
);


CREATE TABLE IF NOT EXISTS reviews (
  id INT AUTO_INCREMENT PRIMARY KEY,
  source ENUM('testimonial', 'google') NOT NULL DEFAULT 'testimonial',
  google_review_id VARCHAR(255) NULL UNIQUE,
  author_name VARCHAR(120) NOT NULL,
  author_role VARCHAR(120) NULL,
  clinic_name VARCHAR(180) NULL,
  avatar_url VARCHAR(500) NULL,
  rating INT NOT NULL DEFAULT 5,
  review_text TEXT NOT NULL,
  review_url VARCHAR(500) NULL,
  consent_given TINYINT(1) NOT NULL DEFAULT 0,
  status ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
  published_at DATETIME NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_reviews_status_published_at (status, published_at)
);
