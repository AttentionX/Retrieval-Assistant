import numpy as np
import math
from itertools import chain

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
        sections = self.searchByKeywords(keywords)
        return self.answerFromSections(sections, query, self.user_model)

    def getKeywords(self, query):
        prompt = """
        Extract the keywords from the following query with a separator ; (refer to the following two examples)

        Examples:
        Query1: What is the GPT-3 architecture?
        Keywords: GPT-3; architecture
        Query2: What is the GPT-3 training data?
        Keywords: GPT-3; training data

        """

        api_prompt = f'{prompt}\nQuery: {query}\nKeywords: '
        # api_prompt = [{"role": "user", "content": api_prompt}]
        keywords = self.system_model.chat(api_prompt).split('; ')
        print('Query:', query)

        keywords = [keyword for keyword in keywords if keyword != '']
        keywords = [keyword[:-1] if (keyword[-1] == '.' or keyword[-1] == "?") else keyword for keyword in keywords]
        keywords = [keyword.strip().lower() for keyword in keywords]
        
        keywords_final = list(chain(*[keyword.split(' ') for keyword in keywords]))

        print('Keywords:', keywords_final)
        return keywords_final

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

    def searchByKeywords(self, keywords):
        sections = self.sections
        max_col_len = len(max(sections, key=len))
        print('retrieval.py, searchByKeywords, max sections in one page:', max_col_len)
        
        sections = np.array([np.pad(row, (0,max_col_len-len(row)), 'constant', constant_values='0') for row in sections])
        print('retrieval.py, searchByKeywords, document sections shape:', sections.shape)
        
        final_sections = None
        for keyword in keywords:
            score_tensor = process.operate_2d_tensor(sections, keyword, np.sqrt)
            if final_sections is None:
                final_sections = score_tensor
            else:
                final_sections = final_sections + score_tensor
        # print('retrieval.py, searchByKeywords, document sections shape', final_sections.shape)
        top_k = len(keywords) if len(keywords) > 3 else 3
        top_k_sections = process.find_highest_positions(final_sections, top_k)
        print('retrieval.py, searchByKeywords, top selections:', top_k_sections)
        i = 0
        print('References')
        for (row, col) in top_k_sections:
            print(f'[{i+1}]', f"P. {row+1} Sec. {col+1}")
            i += 1
        # exit()
        return [sections[row][col] for (row, col) in top_k_sections]

    def answerFromSections(self, sections, query, model:customChatGPT):
        prompt = """
        Answer the following question only referring to the given information. Cite your sources if necessary by referring to the source number (ex. [1]) in your response (in the middle of the sentence).
        """
        # While less than max length, append sections to prompt
        sections_string = ''
        i = 0
        max_length_context = 5000
        while i < len(sections) and len(sections_string) + len('\n\n'+ sections[i]) < max_length_context:
            sections_string += f'\n\n[{i+1}] ' + sections[i]
            i += 1
        api_prompt = f'Given Information:\n-----\n{sections_string}\n-----\n{prompt}\nQuestion: {query}\nAnswer: '
        # self.chat_history.append({"role": "user", "content": api_prompt})

        answer = model.chat(api_prompt)
        # self.chat_history.append({"role": "assistant", "content": answer})
        return answer