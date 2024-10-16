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
