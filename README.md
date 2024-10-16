# Langchain + Dendrite = Use any website with your AI Agents

This repo showcases how to build a simple **Langchain** AI agent that can use a wide variety of websites as tools to in a cheap, fast and reliable way, using the [Dendrite](https://github.com/dendrite-systems/dendrite-python-sdk) Browser SDK.

The same tools can be used for building with [Langgraph](https://github.com/langchain-ai/langgraph)

## Overview

This Langchain OpenAI Tools Agent can:

1. Search for trademarks to determine if a trademark is available
2. Check the status of the OpenAI API
3. Look for new posts on Product Hunt

Streamlit is used to create a simple UI for interacting with the AI agent.

The purpose of this example is to showcase that any website can be used as a tool with Dendrite, even if authentication is required.

## Tools 

Below are all the tools used in this example:


### Extract API Status

![API Status Demo](https://github.com/dendrite-systems/langchain-docs-agent-example/tree/main/demos/APIStatusDemo.gif)

Allowing your AI agent to fetch strutured data is easy with Dendrite. Just prompt or define pydantic models to describe the data you want to extract.

Behind the scenes, Dendrite will create a script that will be stored and reused for all future requests, to increase performance and lower costs.

```python tools/openai_api_status.py
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
```

### Extract from Product Hunt and Send Email

![Product Hunt Tool Demo](https://github.com/dendrite-systems/langchain-docs-agent-example/tree/main/demos/EmailProductHuntDemo.gif)

You can do more than just extract data from websites. You can also authenticate and interact with them.

By giving our AI agent a send email tool, and a tool to extract data from Product Hunt, we can create an AI agent that can monitor Product Hunt for new posts and send an email when a new post is detected!

```python tools/email.py
from dendrite_sdk import AsyncDendrite
from langchain_core.tools import tool


@tool
async def send_email(email_address: str, subject: str, body: str):
    """This tool sends an email to the provided email address with the provided subject and body."""

    # Built in authentication! vvvvvvvvvvvvvvvvvvv
    async with AsyncDendrite(auth="mail.google.com") as client:
        await client.goto("https://mail.google.com/")
        await client.click("the compose button")
        await client.fill_fields(
            {"recipients": email_address, "subject": subject, "body": body}
        )
        await client.click("the send button")

```

```python tools/producthunt.py
from langchain_core.tools import tool
from dendrite_sdk import AsyncDendrite


@tool
async def get_all_product_hunt_posts() -> str:
    """Get's all the posts from product hunt from today"""
    async with AsyncDendrite() as client:
        await client.goto(f"https://www.producthunt.com/")
        await client.click("the see all of today's posts button")
        posts = await client.extract(
            "Get all today's posts from product hunt as a string containing name, desc, categories, upvotes and url"
        )
        return posts


@tool
async def read_more(url: str) -> str:
    """If you want to learn more about a producthunt product, call this function."""
    async with AsyncDendrite() as client:
        await client.goto(url)
        info = await client.extract(
            "Get all the description text about this product and the discussion and return as a string"
        )
        return info
```


### Trademark Search

![Trademark Search Tool Demo](https://github.com/dendrite-systems/langchain-docs-agent-example/tree/main/demos/TrademarkDemo.gif)

If you want to build an AI agent that can search for trademarks so it can help you quickly determine if a trademark is available, just give your AI agent a tool like this:

```python tools/search_trademarks.py
import asyncio
from dendrite_sdk import AsyncDendrite
from langchain_core.tools import tool


@tool
async def search_trademarks(trademark_search_name: str) -> str:
    """
    This tool does a trademark search the provided trademark name and will return the active trademarks
    so that you can determine if there are any conflicting trademarks.
    """
    client = AsyncDendrite()
    await client.goto("https://tmsearch.uspto.gov/search/search-information")
    await client.fill("the trademark name search bar", trademark_search_name)
    await client.press("Enter")
    await client.click("the 'dead' toggle to remove expired trademarks")
    await client.wait_for("all the trademarks to load")
    trademarks = await client.extract(
        "Get all the trademarks in the search results as a list of strings where each string contains the status and description of the trademark",
    )
    print("trademarks", trademarks)
    await client.close()
    return trademarks
```

## Getting Started

I highly suggest using Poetry to install and run this project.

Download Poetry [here](https://python-poetry.org/)

Start by cloning the repo:

```bash
git clone https://github.com/dendrite-systems/langchain-dendrite-example.git
```

To install the project, run the following command:

```bash
poetry install && poetry run dendrite install
```

To run the project, run the following command:

```bash
poetry run streamlit run agent.py
```

## Support

If you have any questions, please join our [Discord](https://discord.gg/4rsPTYJpFb)