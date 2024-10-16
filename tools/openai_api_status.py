from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from dendrite_sdk import AsyncDendrite


class ServiceStatus(BaseModel):
    name: str = Field(description="The name of the service.")
    status: str = Field(description="e.g 'operational' or 'partial outage'.")


class NewsItem(BaseModel):
    news: str = Field(description="The content of the news or incident update.")
    date: Optional[str] = Field(description="YYYY-MM-DD format.")


class APIStatus(BaseModel):
    services_status: list[ServiceStatus]
    news: list[NewsItem]


@tool
async def get_openai_api_status() -> APIStatus:
    """Get the current status of OpenAI's services."""
    async with AsyncDendrite() as client:
        await client.goto(f"https://status.openai.com/")
        service_status: APIStatus = await client.extract(
            "Get the current status of this service.",
            APIStatus,
        )
        return service_status
