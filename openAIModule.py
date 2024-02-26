# Open API Module

from openai import OpenAI
import os


class OpenAIModule():

    def __init__(self):
        key = "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"
        self.client = OpenAI(api_key=key)
        self.system_message = [{"role": "system", "content": "You are a kindly helpful friend."}]

    def generate_reply(self, user_input):
        try:
            messages = self.system_message + [{"role": "user", "content": user_input}]
            botResponce = self.client.chat.completions.create(model="gpt-3.5-turbo",messages=messages)
            reply = botResponce.choices[0].message.content
            return reply
        except Exception as e:
            return "Something Went Wrong Please Try Again"

