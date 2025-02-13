"""
Discriminates between various types of message content.

"""

from typing import Annotated, Literal, Self

from pydantic import BaseModel, Field


class BaseContent(BaseModel):
    type: str

    def append(self, other: Self) -> None:
        raise ValueError(f"Cannot append content of {type(other)} to {type(self)}")


class TextContent(BaseContent):
    type: Literal["text"] = Field(default="text")
    text: str

    def append(self, other: Self) -> None:
        self.text += other.text


class ReasoningContent(BaseContent):
    type: Literal["reasoning"] = Field(default="reasoning")
    reasoning: str


class ImageContent(BaseContent):
    type: Literal["image"] = Field(default="image")
    mimetype: str
    data: bytes


class VideoContent(BaseContent):
    type: Literal["video"] = Field(default="video")
    mimetype: str
    data: bytes


class AudioContent(BaseContent):
    type: Literal["audio"] = Field(default="audio")
    mimetype: str
    data: bytes


Content = Annotated[
    TextContent | ReasoningContent | ImageContent | VideoContent | AudioContent,
    Field(discriminator="type"),
]
