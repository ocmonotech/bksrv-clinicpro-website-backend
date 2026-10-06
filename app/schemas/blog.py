from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.fields import (
    SCHEMA_MARKUP_FIELD,
    SchemaMarkup,
    schema_alias_config,
    schema_alias_response_config,
)


class BlogBase(BaseModel):
    model_config = schema_alias_config

    title: str = Field(min_length=1, max_length=255)
    slug: str | None = Field(default=None, max_length=255)
    excerpt: str | None = None
    content: str = Field(min_length=1)
    cover_image: str | None = Field(default=None, max_length=500)
    author: str | None = Field(default=None, max_length=100)
    category: str | None = Field(default="Resources", max_length=100)
    status: Literal["draft", "published"] = "draft"
    published_at: datetime | None = None
    meta_title: str | None = Field(default=None, max_length=255)
    meta_description: str | None = None
    meta_keywords: str | None = Field(default=None, max_length=500)
    canonical_url: str | None = Field(default=None, max_length=500)
    og_image: str | None = Field(default=None, max_length=500)
    robots: str | None = Field(default=None, max_length=50)
    schema_markup: SchemaMarkup = SCHEMA_MARKUP_FIELD


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    model_config = schema_alias_config

    title: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = Field(default=None, max_length=255)
    excerpt: str | None = None
    content: str | None = Field(default=None, min_length=1)
    cover_image: str | None = Field(default=None, max_length=500)
    author: str | None = Field(default=None, max_length=100)
    category: str | None = Field(default=None, max_length=100)
    status: Literal["draft", "published"] | None = None
    published_at: datetime | None = None
    meta_title: str | None = Field(default=None, max_length=255)
    meta_description: str | None = None
    meta_keywords: str | None = Field(default=None, max_length=500)
    canonical_url: str | None = Field(default=None, max_length=500)
    og_image: str | None = Field(default=None, max_length=500)
    robots: str | None = Field(default=None, max_length=50)
    schema_markup: SchemaMarkup = SCHEMA_MARKUP_FIELD


class BlogResponse(BlogBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = schema_alias_response_config
