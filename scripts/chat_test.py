import base64

from pdf2image import convert_from_path
from PIL import Image
from manual_qa_bot.index_manager import IndexManager
from manual_qa_bot.chat import ChatModel


def rag_search(query: str):
    rag = IndexManager().create_index("test")
    results = rag.search(query, k=1)
    return results


query = "インクルードファイルの設定について教えて。"
results = rag_search(query)

page_images = convert_from_path("data/sh081933c.pdf", dpi=200)
target_image: Image.Image = page_images[results[0]["page_num"] - 1]

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": query},
        ],
    }
]

model = ChatModel()
print(model.chat(messages, images=[target_image]))
