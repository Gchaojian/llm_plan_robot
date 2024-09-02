import os
import sys
import logging
import socket

from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI  # 修改这里以导入自定义的 OpenAI 客户端

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from gpt_client.gpt_client.prompts.prompt_template import QA_TEMPLATE_BAICHUAN
import gpt_client.gpt_client.commons.embedding_utils as eu
from gpt_client.gpt_client.commons.utils import *

logging.basicConfig(level=logging.INFO)


class GPTAssistant:
    """ Load ChatGPT config and your custom pre-prompts. """

    def __init__(self, verbose=False) -> None:
        
        logging.info("Loading keys...")
        cfg_file = os.path.join(os.path.dirname(__file__), '../commons/config_test.json')
        set_global_configs(cfg_file)
        logging.info(f"Done.")
        API_BASE = "https://api.lingyiwanwu.com/v1"

        logging.info("Initialize LLM...")
        # 修改这里初始化 OpenAI 客户端
        llm = ChatOpenAI(
            model="yi-large",
            base_url=API_BASE,
            temperature=0.1,
            max_tokens=2048,
        )
        logging.info(f"Done.")

        logging.info("Initialize tools...")
        embedding_model = eu.init_embedding_model()
        vector_store = eu.init_vector_store(embedding_model)
        logging.info(f"Done.")

        logging.info("Initialize chain...")
        chain_type_kwargs = {"prompt": QA_TEMPLATE_BAICHUAN, "verbose": verbose}
        self.conversation = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type='stuff',
            retriever=vector_store.as_retriever(search_kwargs={'k': 3}),
            chain_type_kwargs=chain_type_kwargs,
            return_source_documents=True
        )
        logging.info(f"Done.")

        os.system("clear")
        streaming_print_banner()

    def ask(self, question):
        result_dict = self.conversation(question)
        result = result_dict['result']
        return result


def main(args=None):
    IS_DUBUG = True
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    gpt = GPTAssistant(
        verbose=True,
    )
    if not IS_DUBUG:
        HOST = '192.168.3.26'
        PORT = 5001
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("Connected to server.")

    while True:
        question = input(colors.YELLOW + "用户💬> " + colors.ENDC)
        if question == "!quit" or question == "!exit":
            break
        if question == "!clear":
            os.system("clear")
            continue

        result = gpt.ask(question)  # Ask a question
        print(colors.GREEN + "机器人🤖> " + colors.ENDC + f"{result}")
        if not IS_DUBUG:
            s.sendall(result.encode())


if __name__ == '__main__':
    main()
