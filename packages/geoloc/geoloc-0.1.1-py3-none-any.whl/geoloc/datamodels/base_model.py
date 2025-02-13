from pydantic import BaseModel, ConfigDict


class ModelConfig(BaseModel):
    model_config = ConfigDict(extra='forbid', arbitrary_types_allowed=True,
                              defer_build=True, populate_by_name=True)
