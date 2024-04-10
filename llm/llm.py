from ctransformers import AutoModelForCausalLM, AutoConfig
from langchain.llms import CTransformers
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import box
import yaml


# Import config vars
with open('config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))

config = AutoConfig.from_pretrained("TheBloke/Mistral-7B-Instruct-v0.1-GGUF")
# Explicitly set the max_seq_len
config.max_seq_len = 4096
config.max_answer_len= 2048

def setup_llm():
    llm = CTransformers(model=cfg.MODEL_BIN_PATH,
                        model_type=cfg.MODEL_TYPE,
                        max_new_tokens=cfg.MAX_NEW_TOKENS,
                        temperature=cfg.TEMPERATURE,
                        context_length=cfg.CONTEXT_LENGTH,
                        # config=config,
                        callbacks=[StreamingStdOutCallbackHandler()]
    )

    # llm = AutoModelForCausalLM.from_pretrained("TheBloke/Llama-2-7B-GGUF",
    #                                             model_file=cfg.MODEL_BIN_PATH,
    #                                             # model_type=cfg.MODEL_TYPE,
    #                                             model_type="llama",
    #                                             max_new_tokens=cfg.MAX_NEW_TOKENS,
    #                                             temperature=cfg.TEMPERATURE,
    #                                             context_length=cfg.CONTEXT_LENGTH,
    #                                             gpu_layers=0,
    #                                             callbacks=[StreamingStdOutCallbackHandler()]
    # )

    # llm = CTransformers(model=cfg.MODEL_BIN_PATH,
    #                     model_type=cfg.MODEL_TYPE,
    #                     max_new_tokens=cfg.MAX_NEW_TOKENS,
    #                     temperature=cfg.TEMPERATURE,
    #                     context_length=cfg.CONTEXT_LENGTH,
    #                     # callbacks=[StreamingStdOutCallbackHandler()]
    # )


    # llm = AutoModelForCausalLM.from_pretrained("TheBloke/Mistral-7B-v0.1-GGUF",
    #                                            model_file="mistral-7b-v0.1.Q5_K_M.gguf",
    #                                            model_type="mistral",
    #                                            gpu_layers=0,
    #                                            config=config
    #                                            )

    print(llm)

    return llm
