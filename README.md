# Langchain + Dendrite = AI Agents than can use any website

This example repo contains a simple [LangChain](https://github.com/langchain-ai/langchain/tree/master) AI agent that can use a wide variety of websites using the [Dendrite Browser SDK](https://github.com/dendrite-systems/dendrite-python-sdk). (Same concepts apply to building a [LangGraph agent](https://github.com/langchain-ai/langgraph))

## Overview

This repo includes a Langchain OpenAI Tools Agent, with a streamlit UI, that has tools to:

1. Search for conflicting trademarks
2. Check the status of the OpenAI API
3. Look for new products on Product Hunt
4. Send emails

*(Very random choice of tools I know, but the purpose of this example is to showcase that any website can be used – even if authentication is required!)*

## Getting Started

I highly suggest using Poetry to install and run this project. Download Poetry [here](https://python-poetry.org/)

1. **Start by cloning the repo:**

```bash
git clone https://github.com/dendrite-systems/langchain-dendrite-example.git
```
```bash
cd langchain-dendrite-example
```

2. **Install the project:** Run the following command:

```bash
poetry install && poetry run dendrite install
```

or with pip

```bash
pip install -r requirements.txt && dendrite install
```

**Important:** Don't forget to run `dendrite install`, since this installs the browser binaries.

3. **Create a `.env` file**. It should contain an OpenAI and Dendrite API key.

Get a free Dendrite API key [here](https://dendrite.systems/create-account).

```
OPENAI_API_KEY=sk-Cs...
DENDRITE_API_KEY=sk_4b0...
```

4. **Run the project:**

```bash
poetry run streamlit run agent.py
```

or with pip

```bash
streamlit run agent.py
```

## Tools 

Below are all the custom tools provided to our AI agent:

---

### Extract API Status Tool

This tool uses Dendrite's `extract` function to get OpenAI's API status.

Behind the scenes, Dendrite will create a bs4 script that will be stored and reused for all future requests to increase speed and remove inference costs.

![API Status Demo](https://github.com/dendrite-systems/langchain-docs-agent-example/blob/main/demos/APIStatusDemo.gif)

`tools/openai_api_status.py`
```python
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

---

### Extract from Product Hunt Tool and Send Email Tool

You can do more than just extract data from websites. You can also authenticate and interact with them.

By giving our AI agent a send email tool and a tool to extract data from Product Hunt, we can create an AI agent that can monitor Product Hunt for new posts and send an email when a new post is detected!

For the email tool to work, you'll need to authenticate first via Dendrite Vault. [Read the Dendrite docs to learn how](https://docs.dendrite.systems/concepts/authentication).

![Product Hunt Tool Demo](https://github.com/dendrite-systems/langchain-docs-agent-example/blob/main/demos/EmailProductHuntDemo.gif)


`tools/email.py`
```python
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

`tools/producthunt.py`
```python
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

---

### Trademark Search Tool

If you want to build an AI agent that can search for trademarks so it can help you quickly determine if a trademark is available, just give your AI agent a tool like this:

![Trademark Search Tool Demo](https://github.com/dendrite-systems/langchain-docs-agent-example/blob/main/demos/TrademarkDemo.gif)

`tools/search_trademarks.py`
```python
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

## Contributing

If you have an idea for a cool tool that you'd like to add, create a pull request – contribution is warmly welcome!

## Support

If you have any questions, please join our [Discord](https://discord.gg/4rsPTYJpFb)
