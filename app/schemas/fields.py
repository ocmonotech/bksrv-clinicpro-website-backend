from typing import Any

from pydantic import AliasChoices, ConfigDict, Field

# Avoid shadowing BaseModel.schema_json while keeping the wire/ORM key "schema_json".
SCHEMA_MARKUP_FIELD = Field(
    default=None,
    validation_alias=AliasChoices("schema_json", "schema_markup"),
    serialization_alias="schema_json",
)

SchemaMarkup = dict[str, Any] | None

schema_alias_config = ConfigDict(
    populate_by_name=True,
    serialize_by_alias=True,
)

schema_alias_response_config = ConfigDict(
    from_attributes=True,
    populate_by_name=True,
    serialize_by_alias=True,
)
