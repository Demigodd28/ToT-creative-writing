from llama_cpp import Llama
from tot.prompts.text import *
import parameters

llm = Llama(
    model_path = "openhermes-2.5-neural-chat-7b-v3-1-7b.Q2_K.gguf",
    n_ctx=2048,
    # n_gpu_layers=-1
)

def Generator(llm, node):
    new_node ={}
    output = []

    prompt = cot_prompt.format(input = node[1]['answer'][0] + node[1]['answer'][1] + node[1]['answer'][2] + node[1]['answer'][3])

    for _ in range(5):
        ans_from_llm = {}
        filtered_ans = ""
        if node[0] == None:
            ans_from_llm = llm(
                            prompt,
                            max_tokens = 2048,
                            stop=["\n\n", "known"],
                            echo = False)
            ans_from_llm = ans_from_llm["choices"][0]["text"].split('Passage:')##left [plan:1.2.3.4., paragragh*4]
            filtered_ans = ans_from_llm[0]##chose [0]
        else:
            prompt += f"""the plan has been chose to be {node[0][0]['answer']}, then only write the passage according to the plan. Your output should be of the following format:
                    Passage:
                    Your passage here.
                    """

            ans_from_llm = llm(
                            prompt,
                            max_tokens = 2048,
                            stop=["\n\n", "known"],
                            echo = False)
            filtered_ans = ans_from_llm["choices"][0]["text"]##left paragragh*4
       
        new_node['id'] = parameters.id
        parameters.increase_id()
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
    best = ans_from_llm["choices"][0]["text"].split()
    for i in range(5):
        if best[4] == str(node[i]['id']):
            break
    new_node = node[i] 
    output.append(new_node)
    return output


if __name__ == '__main__':

    question = []  #input 4 sentence
    a = "It isn't difficult to do a handstand if you just stand on your hands."
    b = "It caught him off guard that space smelled of seared steak."
    c = "When she didn't like a guy who was trying to pick her up, she started using sign language."
    d = "Each person who knows you has a different perception of who you are."
    question.extend([a, b, c, d])

    root_node = {'id':parameters.id,
                'answer':question,
                'value':None,
                'parent_node':None,
                'ancester_value':None
                }
    parameters.increase_id()

    writing_plans = Generator(llm, [None, root_node])### Generator(llm, [plan, root_node])  no plan -->None
    best_plan = Evaluator(llm, writing_plans)

    passages = Generator(llm, [best_plan, root_node])
    best_passage = Evaluator(llm, passages)
    print(best_plan[0]['answer'])
    print(best_passage[0]['answer'])
