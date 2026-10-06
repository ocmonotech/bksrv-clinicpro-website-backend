from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.fields import (
    SCHEMA_MARKUP_FIELD,
    SchemaMarkup,
    schema_alias_config,
    schema_alias_response_config,
)

ProductPageCategory = Literal["apps-tools", "practice-types", "multi-clinic"]
ProductPageStatus = Literal["draft", "published"]


class ProductPageBase(BaseModel):
    model_config = schema_alias_config

    category: ProductPageCategory
    title: str = Field(min_length=1, max_length=255)
    slug: str | None = Field(default=None, max_length=255)
    description: str | None = None
    content: str | None = None
    icon: str | None = Field(default=None, max_length=100)
    image: str | None = Field(default=None, max_length=500)
    link: str | None = Field(default=None, max_length=500)
    sort_order: int = Field(default=0, ge=0)
    status: ProductPageStatus = "draft"
    meta_title: str | None = Field(default=None, max_length=255)
    meta_description: str | None = None
    meta_keywords: str | None = Field(default=None, max_length=500)
    canonical_url: str | None = Field(default=None, max_length=500)
    og_image: str | None = Field(default=None, max_length=500)
    robots: str | None = Field(default=None, max_length=50)
    schema_markup: SchemaMarkup = SCHEMA_MARKUP_FIELD


class ProductPageCreate(ProductPageBase):
    pass


class ProductPageUpdate(BaseModel):
    model_config = schema_alias_config

    category: ProductPageCategory | None = None
    title: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(default=None, max_length=255)
    description: str | None = None
    content: str | None = None
    icon: str | None = Field(default=None, max_length=100)
    image: str | None = Field(default=None, max_length=500)
    link: str | None = Field(default=None, max_length=500)
    sort_order: int | None = Field(default=None, ge=0)
    status: ProductPageStatus | None = None
    meta_title: str | None = Field(default=None, max_length=255)
    meta_description: str | None = None
    meta_keywords: str | None = Field(default=None, max_length=500)
    canonical_url: str | None = Field(default=None, max_length=500)
    og_image: str | None = Field(default=None, max_length=500)
    robots: str | None = Field(default=None, max_length=50)
    schema_markup: SchemaMarkup = SCHEMA_MARKUP_FIELD


class ProductPageResponse(ProductPageBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = schema_alias_response_config


class ProductPageMenuItem(BaseModel):
    title: str
    description: str | None = None
    link: str
    icon: str | None = None


class ProductPageMegaMenuResponse(BaseModel):
    apps_tools: list[ProductPageMenuItem]
    practice_types: list[ProductPageMenuItem]
    multi_clinic: list[ProductPageMenuItem]
