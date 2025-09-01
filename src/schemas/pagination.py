from pydantic import BaseModel, Field


class PaginationModel(BaseModel):
    limit: int = Field(5, gt = 0, le = 100, description = "Per Page")
    offset: int = Field(0, ge = 0, description = "Page Offset")


