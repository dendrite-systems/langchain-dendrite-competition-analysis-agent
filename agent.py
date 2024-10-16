import asyncio
import streamlit as st


from dotenv import load_dotenv, find_dotenv
import asyncio
import streamlit as st
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI

from tools.email import send_email
from tools.producthunt import get_all_product_hunt_posts, read_more
from tools.search_trademarks import search_trademarks
from tools.openai_api_status import get_openai_api_status

load_dotenv(find_dotenv())


# Competition agent – easy to build, useful


tools = [
    get_openai_api_status,
    search_trademarks,
    get_all_product_hunt_posts,
    read_more,
    send_email,
]

prompt = hub.pull("hwchase17/openai-tools-agent")
llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


async def process_user_input(user_input, chat_history):
    command = {
        "input": user_input,
        "chat_history": chat_history,
    }
    response = await agent_executor.ainvoke(command)
    return response["output"]


# Streamlit UI
def main():
    st.title("AI Agent Chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What would you like me to do?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            full_response = asyncio.run(
                process_user_input(prompt, st.session_state.messages)
            )
            message_placeholder.markdown(full_response)

        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )


if __name__ == "__main__":
    main()
