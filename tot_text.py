from llama_cpp import Llama
from openai import OpenAI
from parameters import *
import random
import time
import re
from datetime import date
import os

llm_1 = Llama(
    model_path = "openhermes-2.5-mistral-7b.Q8_0.gguf",
    n_ctx=2048,
    # n_gpu_layers=-1    
)

llm_2 = OpenAI(
    api_key = OPENAI_API_KEY
)

def Generator(llm, node):
    new_node ={}
    output = []
        
    for _ in range(5):## k=5
        ans_from_llm = {}
        filtered_ans = ""
        
        if node[0] == None:
            prompt = cot_prompt_1.format(input = node[1]['answer'])   
            ans_from_llm = llm(
                prompt,
                max_tokens = 1600,
                stop=["\n\n", "known"],
                echo = False,
                repeat_penalty = 1.1,
                temperature = 0.7,
                top_k = 40,
                top_p = 0.9,
            )
            filtered_ans = ans_from_llm["choices"][0]["text"].replace("Plans:\n", "")
        else:                          
            prompt = cot_prompt_2.format(input = node[1]['answer'], plan = node[0][0]['answer'][0])
            check_1 = False        
            for _ in range(5):      
                if check_1 == False:
                    ans_from_llm = llm(
                        prompt,
                        max_tokens = 1600,
                        stop=["\n\n", "known"],
                        echo = False,
                        repeat_penalty = 1.1,
                        temperature = 0.7,
                        top_k = 40,
                        top_p = 0.9,
                    )
                    check_1 = check(ans_from_llm["choices"][0]["text"], node[1]['answer'][0])
                else: break 
            filtered_ans = ans_from_llm["choices"][0]["text"] + "\n"
        
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
        max_tokens = 1800,
        stop=["\n\n", "known"],
        echo = False,
        repeat_penalty = 1.1,
        temperature = 0.7,
        top_k = 40,
        top_p = 0.9,
    )
    best = ans_from_llm["choices"][0]["text"].split()##暫時用random解決

    if len(best) == 5:    
        for i in range(5):
            if best[4] == str(node[i]['id']):
                break
        new_node = node[i]
    else:
        new_node = node[random.randint(0, 4)]
    output.append(new_node)
    return output

def Grade(llm, text):
    scores = []
    completion_tokens = 0
    prompt_tokens = 0

    for _ in range(5):# grade for 5 times
        try:
            ans_from_llm = llm.chat.completions.create(
                model='gpt-4-0613',
                messages=[
                    {"role": "user", "content": score_prompt + text}
                ]
            )
            
            completion_tokens += ans_from_llm.usage.completion_tokens
            prompt_tokens += ans_from_llm.usage.prompt_tokens

            filtered_ans = ans_from_llm.choices[0].message.content
            match = re.search(r'\d+', filtered_ans)

            if match and match.group().isdigit():
                scores.append(int(match.group()))
        except Exception as e:
            print(f"An error occurred during grading: {e}")

    average_score = sum(scores) / len(scores) if scores else 0
    return [average_score, [completion_tokens, prompt_tokens]]

def check(text, input_data):##examine if last sentence is matched input
    fragment_1 = text.replace(', ', '. ')
    fragments_1 = fragment_1.split('. ')

    # print(len(fragments_1))
    for i in range(len(fragments_1)):
        fragments_1[i] = fragments_1[i].strip()

    if fragments_1[-1] in input_data:
        return True
    else:
        return False


if __name__ == '__main__':
    
    score_list = []
    with open('data_100_random_text.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()

    folder_name = f'Result {date.today()}'## build new folder 'Result 2024-01-22'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    for i in range(4, 7):
        start = time.time()
        file_name = f'{folder_name}/result_{i}.txt'    
        root_node = {
            'id':id,
            'answer':[data[i]],
            'value':None,
            'parent_node':None,
            'ancester_value':None
        }
        increase_id()

        writing_plans = Generator(llm_1, [None, root_node])### Generator(llm, [plan, root_node])  no plan -->None
        best_plan = Evaluator(llm_1, writing_plans)

        passages = Generator(llm_1, [best_plan, root_node])
        best_passage = Evaluator(llm_1, passages)

        graded = Grade(llm_2, best_passage[0]['answer'][0])
        score = graded[0]
        completion_token = graded[1][0]
        prompt_token = graded[1][1]

        with open(file_name, 'w', encoding='utf-8') as file:### open new txt
            file.write(root_node['answer'][0])
            file.write('\n...........................\n')
            file.write(best_plan[0]['answer'][0])
            file.write('\n--- --- --- --- --- --- ---\n')
            file.write(best_passage[0]['answer'][0])
            file.write('\n---------------------------\n')
            file.write(f"\n\nThe coherent score is {score}")
            file.write(f"\nGraded completion token = {completion_token}")
            file.write(f"\nGraded prompt token = {prompt_token}")
        
        finish = time.time()
        with open(file_name, 'a', encoding = 'utf-8') as file:
            file.write(f"\n\nGenerated time = {finish - start}")

        score_list.append(score)
        print(finish - start)
    print(score_list)
