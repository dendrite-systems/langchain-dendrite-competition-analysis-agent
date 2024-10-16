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
