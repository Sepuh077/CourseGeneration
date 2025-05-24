import os
import json
from typing import Union
from langchain.schema import HumanMessage
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

from src import Elements


LLM = ChatOpenAI(model="gpt-4.1", temperature=0.7, max_tokens=180)


class Texts(Elements):
    def __init__(self, video_course, slides: Elements, data: Union[str, list, None] = None):
        super().__init__(video_course, "texts", "txt")
        
        self.slides = slides
        self.check_data(data)

    def generate_texts_for_slides(self):
        memory = ConversationSummaryMemory(llm=LLM, return_messages=True)

        for i in range(len(self.slides)):
            self.generate_text_for_slide(memory, i, send_msg=True)
    
    def regenerate_text(self, index: int):
        if index >= len(self):
            raise IndexError("Index is out of range!")
        memory = ConversationSummaryMemory(llm=LLM, return_messages=True)

        for i in range(index):
            self.generate_text_for_slide(memory, i)
        return self.generate_text_for_slide(memory, index, overwrite=True)
    
    def generate_text_for_slide(self, memory: ConversationSummaryMemory, index: int, overwrite: bool = False, send_msg: bool = False):
        if os.path.exists(self[index]) and not overwrite:
            text = self.get(index)
            if text:
                memory.chat_memory.add_ai_message(text)
            if send_msg:
                self.send_skip_msg(index)
            return

        base64_str = self.slides.get_base64(index)
        prompt = [
            {
                "type": "text", 
                "text": self.get_slide_prompt(index)
            },
            {
                "type": "image_url", 
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_str}"
                }
            },
        ]

        human_message = HumanMessage(content=prompt)

        full_chat = memory.chat_memory.messages + [human_message]

        try:
            response = LLM.invoke(full_chat)
        except Exception as exc:
            self.send_error_msg(index)
            raise exc

        memory.chat_memory.add_ai_message(response)

        return self.write(index, response.content, send_msg)

    def generate_text_for_slide_without_memory(self, index: int, overwrite: bool = False):
        if os.path.exists(self[index]) and not overwrite:
            return
        base64_str = self.slides.get_base64(index)
        prompt = [
            {
                "type": "text", 
                "text": self.get_slide_prompt(-1)
            },
            {
                "type": "image_url", 
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_str}"
                }
            },
        ]

        human_message = HumanMessage(content=prompt)

        response = LLM.invoke([human_message])

        return self.write(index, response.content)

    def get_slide_prompt(self, index: int):
        """
        To get the default prompt (for middle pages) index = -1 can be assigned
        """
        if index == 0:
            return "Imagine you are a university presenter starting a lecture. Introduce the topic clearly and engagingly in under 150 tokens without cutting off mid-sentence and return only speakable text"
        elif index == len(self.slides) - 1:
            return "As a presenter concluding the lecture, summarize the key points and encourage students to explore further in under 150 tokens without cutting off mid-sentence"
        else:
            return "As a presenter, provide detailed but understandable content of this slide, return only speakable text in under 150 tokens without cutting off mid-sentence"

    def check_data(self, data):
        if not data:
            return True
        if isinstance(data, str):
            if not os.path.exists(data):
                raise FileNotFoundError("The given data path is not found!")
            elif not data.endswith(".json"):
                raise ValueError("The data type must be json!")
            else:
                with open(data, "r") as file:
                    data = json.loads(file.read())
        if not isinstance(data, list):
            raise TypeError("Provided data type must be list or str, but received {}".format(type(data)))
        
        for index, text in enumerate(data):
            if text:
                self.write(index, text)
    
    def write(self, index: int, text: str, send_msg: bool = False):
        text = text.strip()
        if send_msg:
            self.send_message(text, index)
        with open(self[index], "w") as file:
            file.write(text)
        
        return text

    def get(self, index: int):
        if os.path.exists(self[index]):
            with open(self[index], "r") as file:
                return file.read()
        return ''
