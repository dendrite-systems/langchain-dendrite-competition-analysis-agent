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
