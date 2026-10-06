from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import engine
from app.models.seo import SeoPage, SeoSiteSettings

DEFAULT_PAGES = [
    {"path": "/", "label": "Home", "sitemap_priority": "1.0", "sitemap_changefreq": "daily"},
    {"path": "/about", "label": "About", "sitemap_priority": "0.6", "sitemap_changefreq": "monthly"},
    {"path": "/price", "label": "Pricing", "sitemap_priority": "0.8", "sitemap_changefreq": "weekly"},
    {"path": "/contact", "label": "Contact", "sitemap_priority": "0.5", "sitemap_changefreq": "monthly"},
    {"path": "/features", "label": "Features", "sitemap_priority": "0.8", "sitemap_changefreq": "weekly"},
    {"path": "/blog", "label": "Blog", "sitemap_priority": "0.8", "sitemap_changefreq": "daily"},
    {"path": "/security", "label": "Security", "sitemap_priority": "0.5", "sitemap_changefreq": "monthly"},
    {"path": "/integrations", "label": "Integrations", "sitemap_priority": "0.7", "sitemap_changefreq": "weekly"},
    {"path": "/apps-and-tools", "label": "Apps & Tools", "sitemap_priority": "0.7", "sitemap_changefreq": "weekly"},
    {"path": "/practice-types", "label": "Practice Types", "sitemap_priority": "0.7", "sitemap_changefreq": "weekly"},
    {"path": "/multi-clinic", "label": "Multi Clinic", "sitemap_priority": "0.7", "sitemap_changefreq": "weekly"},
    {"path": "/professions", "label": "Professions", "sitemap_priority": "0.7", "sitemap_changefreq": "weekly"},
]

ENTITY_SEO_COLUMNS = {
    "blogs": [
        ("robots", "VARCHAR(50) NULL"),
    ],
    "professions": [
        ("robots", "VARCHAR(50) NULL"),
        ("schema_json", "JSON NULL"),
    ],
    "integrations": [
        ("robots", "VARCHAR(50) NULL"),
        ("schema_json", "JSON NULL"),
    ],
    "product_pages": [
        ("robots", "VARCHAR(50) NULL"),
        ("schema_json", "JSON NULL"),
    ],
}


def _table_exists(connection, table_name: str) -> bool:
    result = connection.execute(
        text(
            """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = DATABASE() AND table_name = :table_name
            """
        ),
        {"table_name": table_name},
    )
    return bool(result.scalar())


def _column_exists(connection, table_name: str, column_name: str) -> bool:
    result = connection.execute(
        text(
            """
            SELECT COUNT(*)
            FROM information_schema.columns
            WHERE table_schema = DATABASE()
              AND table_name = :table_name
              AND column_name = :column_name
            """
        ),
        {"table_name": table_name, "column_name": column_name},
    )
    return bool(result.scalar())


def migrate_entity_seo_columns() -> None:
    with engine.begin() as connection:
        for table_name, columns in ENTITY_SEO_COLUMNS.items():
            if not _table_exists(connection, table_name):
                continue
            for column_name, column_type in columns:
                if _column_exists(connection, table_name, column_name):
                    continue
                connection.execute(
                    text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
                )


def seed_seo_defaults(db: Session) -> None:
    settings = db.query(SeoSiteSettings).first()
    if not settings:
        db.add(
            SeoSiteSettings(
                site_name="ClinicPro by ocmono",
                title_suffix="ClinicPro by ocmono",
                default_meta_description=(
                    "ClinicPro by ocmono provides comprehensive clinic management with "
                    "appointments, EMR, billing, and revenue tracking in one platform."
                ),
                default_og_image="/assets/img/logo/logo-black.png",
                twitter_handle="@clinicpro",
                robots_default="index,follow",
                organization_schema={
                    "@context": "https://schema.org",
                    "@type": "Organization",
                    "name": "ClinicPro by ocmono",
                    "url": "https://clinicpro.cc",
                    "logo": "https://clinicpro.cc/assets/img/logo/logo-black.png",
                },
                sitemap_enabled=True,
                robots_extra="Disallow: /admin\nDisallow: /api",
            )
        )

    existing_paths = {row.path for row in db.query(SeoPage.path).all()}
    for page in DEFAULT_PAGES:
        if page["path"] in existing_paths:
            continue
        db.add(
            SeoPage(
                path=page["path"],
                label=page["label"],
                sitemap_include=True,
                sitemap_priority=page["sitemap_priority"],
                sitemap_changefreq=page["sitemap_changefreq"],
            )
        )

    db.commit()
