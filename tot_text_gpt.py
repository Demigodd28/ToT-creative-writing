from parameters import *
import random
from openai import OpenAI
import re
import time

llm = OpenAI(
    api_key = OPENAI_API_KEY
)

def Generator(llm, node):
    new_node ={}
    output = []
    ##
    a = node[1]['answer'][0].split('. ')
    a = [sentence.strip() for sentence in a if sentence.strip()]
    for i in range(len(a)):
        a[i] += '.'
    ##put rootnode['answer'] into a 4 elements list
        
    for _ in range(5):
        ans_from_llm = {}
        filtered_ans = ""

        for i in range(4):    
            if node[0] == None:###no plan
                user_content = user_cotprompt_1.format(input = a[i])
                ans_from_llm = llm.chat.completions.create(
                    model = 'gpt-3.5-turbo-1106',
                    messages = [
                        {"role": "user", "content": user_content}
                    ]
                )
                filtered_ans += ans_from_llm.choices[0].message.content + "\n"
                # print('ok\t')
            else:
                ##
                b = node[0][0]['answer'][0].split('. ')
                b = [sentence.strip() for sentence in b if sentence.strip()]
                for j in range(len(b)):
                    b[j] += '.'
                ##put plan['answer'] into a 4 elements list
                    
                user_content = user_cotprompt_2.format(input = a[i], plan = b[i])

                check_1 = False        
                for _ in range(5):      
                    if check_1 == False:
                        ans_from_llm = llm.chat.completions.create(
                            model = 'gpt-3.5-turbo-1106',
                            messages = [
                                {"role": "user", "content": user_content}
                            ]
                        )
                        check_1 = check(ans_from_llm.choices[0].message.content, a[i])
                    else: break
                # print(ans_from_llm.choices[0].message.content + '\n\n')    
                filtered_ans += ans_from_llm.choices[0].message.content + "\n"
                # print('ok\t')
        
        new_node['id'] = id
        increase_id()
        new_node['answer'] = [filtered_ans]
        new_node['value'] = None
        new_node['parent_node'] = node[1]['id']
        new_node['ancester_value'] = None

        output.append(new_node)
        print('@')
    return output

        

def Evaluator(llm, node):#node = []
    new_node = {}
    output = []
    best = []
    ans_from_llm = {}

    ans_from_llm = llm.chat.completions.create(
            model = 'gpt-3.5-turbo-1106',
            messages = [
                {"role": "system", "content": system_voteprompt},
                {"role": "user", "content": user_voteprompt + 'Choices: ' + node[0]['answer'][0] + node[1]['answer'][0] + node[2]['answer'][0] + node[3]['answer'][0] + node[4]['answer'][0]}
            ]
        )
    best = ans_from_llm.choices[0].message.content.split()##暫時用random解決問題

    if len(best) == 5:    
        for i in range(5):
            if best[4] == str(node[i]['id']):
                break
        new_node = node[i]
    else:
        new_node = node[random.randint(0, 4)]
    output.append(new_node)
    return output


def check(text, input_data):
    fragment_1 = text.replace(', ', '. ')
    # print(fragment_1)
    fragments_1 = fragment_1.split('. ')
    # print(fragments_1)

    for i in range(len(fragments_1)):
        fragments_1[i] = fragments_1[i].strip()

    if fragments_1[-1] in input_data:
        return True
    else:
        return False


if __name__ == '__main__':
    start = time.time()
    with open('data_100_random_text.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()
    
    root_node = {
        'id':id,
        'answer':[data[0]],
        'value':None,
        'parent_node':None,
        'ancester_value':None
    }
    increase_id()

    writing_plans = Generator(llm, [None, root_node])### Generator(llm, [plan, root_node])  no plan -->None
    best_plan = Evaluator(llm, writing_plans)

    passages = Generator(llm, [best_plan, root_node])
    best_passage = Evaluator(llm, passages)
    with open('GPT_result.txt', 'w') as file:### open new txt
        file.write(root_node['answer'][0])
        file.write('\n...........................\n')
        file.write(best_plan[0]['answer'][0])
        file.write('\n--- --- --- --- --- --- ---\n')
        file.write(best_passage[0]['answer'][0])
        file.write('\n---------------------------\n')
    finish = time.time()
    print(finish - start)    
    # for i in range(1, 3):
    #     root_node = {
    #         'id':id,
    #         'answer':[data[i]],
    #         'value':None,
    #         'parent_node':None,
    #         'ancester_value':None
    #     }
    #     increase_id()

    #     writing_plans = Generator(llm, [None, root_node])
    #     best_plan = Evaluator(llm, writing_plans)

    #     passages = Generator(llm, [best_plan, root_node])
    #     best_passage = Evaluator(llm, passages)
    #     with open('result.txt', 'a') as file:### continue writing in txt
    #         file.write(best_plan[0]['answer'][0])
    #         file.write('--- ---')
    #         file.write(best_passage[0]['answer'][0])
    #         file.write('\n---------------------------\n')
            
    
