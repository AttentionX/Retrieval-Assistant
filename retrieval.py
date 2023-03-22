import numpy as np
from functools import identity
import math

from util import openai_api, process
from util.openai_api import customChatGPT

class Retrieval:
    def __init__(self, sections, system_model:customChatGPT, user_model:customChatGPT, filetype='pdf', chat_history=[]):
        self.sections = sections
        self.filetype = filetype
        self.system_model = system_model
        self.user_model = user_model
        self.chat_history = chat_history

    def mainRetrieval(self, query):
        keywords = self.getKeywords(query)
        sections = self.searchByKeywords(self.sections, keywords)
        return self.answerFromSections(sections, query, self.user_model)

    def getKeywords(self, query):
        prompt = """
        Extract the keywords from the following query with a separator ; (refer to the following two examples)
        Query1: What is the GPT-3 architecture?
        Keywords: GPT-3; architecture
        Query2: What is the GPT-3 training data?
        Keywords: GPT-3; training data
        """
        api_prompt = f'{prompt}\nQuery: {query}\nKeywords: '
        keywords = self.system_model.chat(api_prompt).split('; ')
        return keywords

    def getMultiquestions(self, query, model:customChatGPT):
        prompt = """
        Extraact the questions from the following query with a separator ; (refer to the following examples)
        Query1: What is the GPT-3 architecture and what training data was used to train GPT-3?
        Questions: What is the GPT-3 architecture?; What is the GPT-3 training data?
        Query2: What is the GPT-3 architecture and what training data was used to train GPT-3 and what is the GPT-3 training data?
        Questions: What is the GPT-3 architecture?; What is the GPT-3 training data?
        Query3: What is the GPT-3 architecture?
        Questions: What is the GPT-3 architecture?
        """

    def searchByKeywords(sections, keywords):
        final_sections = None
        for keyword in keywords:
            score_tensor = process.operate_2d_tensor(sections, keyword, math.sqrt)
            if final_sections is None:
                final_sections = score_tensor
            else:
                final_sections = final_sections + score_tensor
        top_k = 3
        top_k_sections = process.find_highest_positions(final_sections, top_k)
        return [sections[row][col] for (row, col) in top_k_sections]

    def answerFromSections(self, sections, query, model:customChatGPT):
        prompt = """
        Answer the following question only referring to the given information
        """
        # While less than max length, append sections to prompt
        sections_string = ''
        i = 0
        while len(sections_string) + len('\n\n'+ sections[i]) < 2000:
            sections_string += '\n\n' + sections[i]
            i += 1
        api_prompt = f'Given Information:\n-----\n{sections_string}\n-----\n{prompt}\nQuestion: {query}\nAnswer: '
        self.chat_history.append({"role": "user", "content": api_prompt})

        answer = model.chat(self.chat_history)
        self.chat_history.append({"role": "assistant", "content": answer})
        return answer