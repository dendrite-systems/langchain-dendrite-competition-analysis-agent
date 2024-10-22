import asyncio
from typing import Annotated, TypedDict
import streamlit as st
from dotenv import load_dotenv, find_dotenv

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


env_path = find_dotenv()
load_dotenv(env_path)


from tools.email import send_email
from tools.producthunt import (
    get_all_product_hunt_posts,
    read_more_product_hunt,
)
from tools.hackernews import get_all_hackernews_posts, read_more_hackernews


tools = [
    get_all_product_hunt_posts,
    get_all_hackernews_posts,
    read_more_hackernews,
    read_more_product_hunt,
    send_email,
]


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools(tools)


async def chatbot(state: State):
    return {"messages": [await llm_with_tools.ainvoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")
graph = graph_builder.compile()


async def stream_graph_updates(user_input: str, messages: list):
    past_messages = [(msg["role"], msg["content"]) for msg in messages]
    past_messages.append(("user", user_input))

    content = await graph.ainvoke(
        {"messages": past_messages},
    )
    return content["messages"][-1].content


# Streamlit UI
def main():
    st.title("Competition Watch AI Agent")
    st.markdown(
        "Uses Langgraph for the AI agent and [Dendrite](https://dendrite.systems/) for the web interactions."
    )

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
                stream_graph_updates(prompt, st.session_state.messages)
            )
            message_placeholder.markdown(full_response)

        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )


if __name__ == "__main__":
    main()
