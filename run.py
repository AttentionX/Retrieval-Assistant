import sys

from util import openai_api, process
from util.openai_api import customChatGPT, customGPT
import retrieval

def init_AI_Models():
    system = "You are a helpful assistant."
    system_model = customChatGPT("gpt-4", system)
    user_model = customGPT("gpt-4", system)
    return system_model, user_model

def main():
    file_path = './samples/papers/gpt-4.pdf'

    if len(sys.argv) == 2:
        file_path = sys.argv[1]

    fileType, fileContent = process.getFileInfo(file_path)

    system_model, user_model = init_AI_Models()

    retrieval_model = retrieval.Retrieval(fileContent, system_model, user_model, fileType)

    while True:
        question = input('Ask a question about the file: ')

        answer = retrieval_model.mainRetrieval(question)
        print('Answer:', answer)

if __name__ == "__main__":
    main()
