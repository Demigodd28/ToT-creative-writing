from parameters import *
import random
from openai import OpenAI

llm = OpenAI(
    api_key = OPENAI_API_KEY
)

def Generator(llm, node):
    new_node ={}
    output = []

    for _ in range(5):
        ans_from_llm = {}
        filtered_ans = ""
        if node[0] == None:
            system_content = system_cotprompt_1
            user_content = user_cotprompt_1.format(input = node[1]['answer'])
        else:
            system_content = system_cotprompt_2
            user_content = user_cotprompt_2.format(input = node[1]['answer'], plan = node[0])

        ans_from_llm = llm.chat.completions.create(
            model = 'gpt-3.5-turbo-1106',
            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ]
        )
        filtered_ans = ans_from_llm.choices[0].message.content
        
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


if __name__ == '__main__':

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
    with open('result.txt', 'w') as file:### open new txt
        file.write(best_plan[0]['answer'][0])
        file.write('\n--- --- --- --- --- --- ---\n')
        file.write(best_passage[0]['answer'][0])
        file.write('\n---------------------------\n')
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
            
    
