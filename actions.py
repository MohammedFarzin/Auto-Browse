from pydantic import BaseModel, Field

class ClickAction(BaseModel):
    """Click on a specific element identified by a label ID."""
    element_id: int = Field(description="The unique number from the visual label.")

class TypeAction(BaseModel):
    """Type text into an input field."""
    element_id: int
    text: str = Field(description="The content to type into the field.")
    press_enter: bool = Field(default=True, description="Press enter after typing?")