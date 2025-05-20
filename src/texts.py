import os
import json
from typing import Union
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.memory import ConversationSummaryMemory
from langchain.chains.conversation.base import ConversationChain

from src import Elements


LLM = ChatOpenAI(model="gpt-4.1", max_tokens=1000)


class Texts(Elements):
    def __init__(self, project_path: str, slides: Elements, data: Union[str, list, None]):
        super().__init__(project_path, "texts", "txt")
        
        self.slides = slides
        self.generate_text = data == None
        self.data = data
        self.check_data()
        if self.generate_text:
            self.generate_texts_for_slides()

    def generate_texts_for_slides(self):
        memory = ConversationSummaryMemory(llm=LLM, return_messages=True)
        conversation = ConversationChain(llm=LLM, memory=memory, verbose=True)

        for i in range(len(self.slides)):
            self.generate_text_for_slide(conversation, i)
    
    def generate_text_for_slide(self, conversation: ConversationChain, index: int):
        if os.path.exists(self[index]):
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
        response = LLM.invoke([human_message]).content
        # response = conversation.predict(input=human_message)

        with open(self[index], "w") as file:
            file.write(response)

    def get_slide_prompt(self, index: int):
        if index == 0:
            return "Imagine you are a university professor starting a lecture. Introduce the topic clearly and engagingly, return only speakable text"
        elif index == len(self.slides) - 1:
            return "As a professor concluding the lecture, summarize the key points and encourage students to explore further, return only speakable text"
        else:
            return "Provide detailed but understandable content, return only speakable text"

    def check_data(self):
        if not self.data:
            return True
        if isinstance(self.data, str):
            if not os.path.exists(self.data):
                raise FileNotFoundError("The given data path is not found!")
            elif not self.data.endswith(".json"):
                raise ValueError("The data type must be json!")
            else:
                with open(self.data, "r") as file:
                    self.data = json.loads(file.read())
        if not isinstance(self.data, list):
            raise TypeError("Provided data type must be list or str, but received {}".format(type(self.data)))
        
        if len(self.data) != len(self.slides):
            raise ValueError("The size of slides and texts must be the same!")
        
        for index, text in enumerate(self.data):
            with open(self[index], "w") as file:
                file.write(text)
