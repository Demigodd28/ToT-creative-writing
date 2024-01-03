from llama_cpp import Llama
from parameters import *

llm = Llama(
    model_path = "openhermes-2.5-neural-chat-7b-v3-1-7b.Q2_K.gguf",
    n_ctx=2048,
    # n_gpu_layers=-1
)

def Generator(llm, node):
    new_node ={}
    output = []

    for _ in range(5):
        ans_from_llm = {}
        filtered_ans = ""
        if node[0] == None:
            prompt = cot_prompt_1.format(input = node[1]['answer'])
        else:
            prompt = cot_prompt_2.format(input = node[1]['answer'], plan = node[0])

        ans_from_llm = llm(
                            prompt,
                            max_tokens = 2048,
                            stop=["\n\n", "known"],
                            echo = False)
        filtered_ans = ans_from_llm["choices"][0]["text"]
        
        new_node['id'] = id
        increase_id()
        new_node['answer'] = [filtered_ans]
        new_node['value'] = None
        new_node['parent_node'] = node[1]['id']
        new_node['ancester_value'] = None

        output.append(new_node)
    return output

        

def Evaluator(llm, node):#node = []
    new_node = {}
    output = []
    best = []
    ans_from_llm = {}

    prompt  = vote_prompt + 'Choices: ' + node[0]['answer'][0] + node[1]['answer'][0] + node[2]['answer'][0] + node[3]['answer'][0] + node[4]['answer'][0]

    ans_from_llm = llm(
                prompt,
                max_tokens = 2048,
                stop=["\n\n", "known"],
                echo = False
            )
    best = ans_from_llm["choices"][0]["text"].split()##要想如何吐出好答案
    for i in range(5):
        if best[4] == str(node[i]['id']):
            break
    new_node = node[i] 
    output.append(new_node)
    return output


if __name__ == '__main__':

    with open('data_100_random_text.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()
    
    for i in range(100):
        root_node = {'id':id,
                    'answer':[data[i]],
                    'value':None,
                    'parent_node':None,
                    'ancester_value':None
                    }
        increase_id()

        writing_plans = Generator(llm, [None, root_node])### Generator(llm, [plan, root_node])  no plan -->None
        best_plan = Evaluator(llm, writing_plans)

        passages = Generator(llm, [best_plan, root_node])
        best_passage = Evaluator(llm, passages)
        with open('result.txt', 'w') as file:
            file.write('---------------------------')
            file.write(best_plan[0]['answer'][0])
            file.write(best_passage[0]['answer'][0])
            file.write('---------------------------')
            
    
