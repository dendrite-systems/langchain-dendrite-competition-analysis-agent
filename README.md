![Dendrite Demo (1)](https://github.com/user-attachments/assets/ac96d6d1-29c0-4680-8168-08440a862d24)

This example repo contains a simple [LangChain](https://github.com/langchain-ai/langchain/tree/master) AI agent that can help us detect competitors by using a variety of websites with the [Dendrite Browser SDK](https://github.com/dendrite-systems/dendrite-python-sdk). (Same concepts apply to building a [LangGraph agent](https://github.com/langchain-ai/langgraph))



## Overview/Features
Repo contains:
- Langchain OpenAI Tools Agent
- Pretty Streamlit UI
- Tool to extract and read about the latest posts on
  - Product Hunt
  - Hacker News
- Tool to log into Outlook and send emails

## Prerequisites

To run this yourself locally, you'll need the following:

- Python v. 3.9+
- An OpenAI API key
- A free [Dendrite API key](https://dendrite.systems/create-account)
- The [Dendrite Vault Chrome Extension](https://chromewebstore.google.com/detail/dendrite-vault/faflkoombjlhkgieldilpijjnblgabnn) if you want to authenticate your agent to use your email.

Pro tip:
- [Install Poetry package manager](https://python-poetry.org/)

## Getting Started

1. **Download this repo:**

    ```bash
    git clone https://github.com/dendrite-systems/langchain-dendrite-example.git
    ```
    ```bash
    cd langchain-dendrite-example
    ```

2. **Install packages** – Don't forget `dendrite install` since this installs the browser binaries

    ```bash
    # with poetry
    poetry install && poetry run dendrite install
    ```
    
    ```bash
    # with pip
    pip install -r requirements.txt && dendrite install
    ```

3. **Create a `.env` file** – Get a free Dendrite API key [here](https://dendrite.systems/create-account).

    ```
    OPENAI_API_KEY=sk-Cs...
    DENDRITE_API_KEY=sk_4b0...
    ```

4. **Run the project:**
    
    ```bash
    # with poetry
    poetry run streamlit run agent.py
    ```
    ```bash
    # with pip
    streamlit run agent.py
    ```

5. **Try it out**, try sending the message:
   ```bash
   Hi, I'm building an AI tool called FooBar. Please find any new potential competitors and summarise them.
   ```

   To send emails, your agent needs to be authorized to use your Outlook account first. Here's how:
   
   1. Install the [Dendrite Vault Chrome Extension](https://chromewebstore.google.com/detail/dendrite-vault/faflkoombjlhkgieldilpijjnblgabnn)
   2. Log into Outlook in your browser
   3. Open the Dendrite vault extension
   4. Press "Authenticate on outlook.com"

   You should now be able to prompt the following:
   
   ```bash
   Hi, I'm building an AI tool called FooBar. Please find any new potential competitors and summarise them. Send the summaries to me via [enter email here].
   ```


## Contributing

Have any cool ideas for features/improvements, create a pull request – contribution is warmly welcome! :)

(I'd personally love to see chainlit added, I don't have time to add it now though)

## Support

If you have any questions or need help, please join the [Dendrite Discord](https://discord.gg/4rsPTYJpFb)
