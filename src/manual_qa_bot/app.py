import streamlit as st
from pdf2image import convert_from_path
from PIL import Image

from manual_qa_bot.chat import ChatModel
from manual_qa_bot.index_manager import IndexManager


def app():
    st.title("Manual QA Bot")
    rag_data_dir = st.text_input("RAG Data Directory", value="data/")
    rag_index_name = st.text_input("RAG Index Name", value="test")
    if "chat_model" not in st.session_state:
        st.session_state.chat_model = ChatModel()
    if "rag" not in st.session_state:
        st.session_state.rag = None
    if "page_images" not in st.session_state:
        st.session_state.page_images = None

    if st.button("Create Index"):
        with st.spinner("Creating index..."):
            st.session_state.rag = IndexManager().create_index(rag_index_name, rag_data_dir)
            st.session_state.page_images = convert_from_path("data/sh081933c.pdf", dpi=200)
        st.success("Index created successfully")

    if st.session_state.rag is not None:
        chat_model = st.session_state.chat_model
        rag = st.session_state.rag
        page_images = st.session_state.page_images

        messages_container = st.container()
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            messages_container.chat_message(message["role"]).markdown(message["content"])

        prompt = st.chat_input("Ask something about the file.")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            messages_container.chat_message("user").markdown(prompt)
            rag_results = rag.search(prompt, k=1)
            target_image: Image.Image = page_images[rag_results[0]["page_num"] - 1]
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image"},
                        {"type": "text", "text": prompt},
                    ],
                }
            ]
            with st.spinner("Thinking..."):
                response = chat_model.chat(messages, images=[target_image])
            messages_container.chat_message("assistant").markdown("以下のページが該当しました。")
            messages_container.chat_message("assistant").image(target_image)
            messages_container.chat_message("assistant").markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        print(st.session_state.messages)
