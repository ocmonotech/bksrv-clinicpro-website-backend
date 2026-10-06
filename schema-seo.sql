-- SEO management tables (also auto-created on API startup)
CREATE TABLE IF NOT EXISTS seo_site_settings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  site_name VARCHAR(255) NOT NULL DEFAULT 'ClinicPro by ocmono',
  title_suffix VARCHAR(255) NULL,
  default_meta_description TEXT NULL,
  default_og_image VARCHAR(500) NULL,
  twitter_handle VARCHAR(100) NULL,
  robots_default VARCHAR(50) NOT NULL DEFAULT 'index,follow',
  google_site_verification VARCHAR(255) NULL,
  bing_site_verification VARCHAR(255) NULL,
  organization_schema JSON NULL,
  sitemap_enabled TINYINT(1) NOT NULL DEFAULT 1,
  robots_extra TEXT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS seo_pages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  path VARCHAR(500) NOT NULL,
  label VARCHAR(255) NULL,
  meta_title VARCHAR(255) NULL,
  meta_description TEXT NULL,
  meta_keywords VARCHAR(500) NULL,
  canonical_url VARCHAR(500) NULL,
  og_image VARCHAR(500) NULL,
  robots VARCHAR(50) NULL,
  schema_json JSON NULL,
  sitemap_include TINYINT(1) NOT NULL DEFAULT 1,
  sitemap_priority VARCHAR(10) NULL DEFAULT '0.7',
  sitemap_changefreq VARCHAR(20) NULL DEFAULT 'weekly',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uq_seo_pages_path (path)
);

CREATE TABLE IF NOT EXISTS seo_redirects (
  id INT AUTO_INCREMENT PRIMARY KEY,
  from_path VARCHAR(500) NOT NULL,
  to_path VARCHAR(1000) NOT NULL,
  status_code INT NOT NULL DEFAULT 301,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  note VARCHAR(500) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uq_seo_redirects_from_path (from_path)
);
