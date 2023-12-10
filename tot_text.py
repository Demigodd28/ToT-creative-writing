from llama_cpp import Llama
from tot.prompts.text import *
import os

def Generator(llm, node):
    new_node ={}
    output = []

    prompt = cot_prompt.format(input = node[0] + node[1] + node[2] + node[3])

    for i in range(5):
        new_node['id'] = id
        new_node['answer'] = llm(
                                prompt,
                                max_tokens = 2048,
                                echo = False
                            )
        new_node['value'] = None
        new_node['parent_node'] = current_node['id']
        new_node['ancester_value'] = None

        output.append(new_node)
        id += 1
    return output

        

def Evaluator(llm, node):#node = []
    new_node = {}
    output = []

    prompt  = vote_prompt + 'Choices: ' + node[0] + node[1] + node[2] + node[3] + node[4]

    best = llm(
                prompt,
                max_tokens = 2048,
                echo = False
            )
    for i in range(5):
        if best == node[i]['id']:
            break
    new_node = node[i] 
    output.append(new_node)
    return output


if __name__ == '__main__':
    llm = Llama(
        model_path=".\models\openhermes-2.5-neural-chat-7b-v3-1-7b.Q8_0.gguf", #model的路徑(要包含副檔名)
        n_ctx=2048, #text的長度上限，llama-cpp的預設上限為2048，但default為512
        n_gpu_layers=-1, #要分擔給GPU的layer數量，-1為全部
    )

    question = []  #input 4 sentence
    a = input()
    b = input()
    c = input()
    d = input()
    question.extend([a, b, c, d])

    root_node = {'id':0,
                'answer':question,
                'value':None,
                'parent_node':None,
                'ancester_value':None
                }

    current_node = root_node
    id = 1
    writing_plans = Generator(llm, question)###不需要plan以外的文字
    best_plan = Evaluator(llm, writing_plans)

    current_node = best_plan[0]
    id = 6
    passages = Generator(llm, question)### 已經有plan 了，不需要passage以外的文字
    best_passage = Evaluator(llm, passages) 
