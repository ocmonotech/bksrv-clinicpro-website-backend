import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.product_page import ProductPage

SEED_DIR = Path(__file__).resolve().parents[2] / "seed" / "product-pages"


def seed_product_pages(db: Session):
    """Insert product hub pages from seed JSON when the table is empty."""
    if not SEED_DIR.exists():
        return

    existing_count = db.query(ProductPage).count()
    if existing_count:
        return

    for seed_file in sorted(SEED_DIR.glob("*.json")):
        payload = json.loads(seed_file.read_text(encoding="utf-8"))
        slug = payload.get("slug")
        if not slug:
            continue

        db.add(
            ProductPage(
                category=payload["category"],
                title=payload["title"],
                slug=slug,
                description=payload.get("description"),
                content=payload.get("content"),
                icon=payload.get("icon"),
                image=payload.get("image"),
                link=payload.get("link"),
                sort_order=payload.get("sort_order", 0),
                status=payload.get("status", "published"),
                meta_title=payload.get("meta_title"),
                meta_description=payload.get("meta_description"),
                meta_keywords=payload.get("meta_keywords"),
                canonical_url=payload.get("canonical_url"),
                og_image=payload.get("og_image"),
            )
        )

    db.commit()
