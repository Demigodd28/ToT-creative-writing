from llama_cpp import Llama

#設定Llama model
llm = Llama(
    model_path=".\models\openhermes-2.5-neural-chat-7b-v3-1-7b.Q8_0.gguf", #model的路徑(要包含副檔名)
    n_ctx=2048, #text的長度上限，llama-cpp的預設上限為2048，但default為512
    n_gpu_layers=-1, #要分擔給GPU的layer數量，-1為全部
)


#prompt到llm
create_completion = llm(
      "Q: Name the planets in the solar system? A: ", # Prompt
      max_tokens = 2048, #控制generate token的上限(不會超過model token limit)
      stop=["\n\n", "known"], #碰到哪些str的時候要停止(已知openhermes在generate下一個問題前會有"\n\n"作為開頭)
      echo = False, #輸出時要不要先複述一遍prompt的內容
      repeat_penalty = 1.1, #越高輸出重複性越低, default = 1.1
      temperature = 0.8, #越高越隨機, default = 0.8
      #temperature: (多樣性低but關聯性高) 0 <==> 1 (多樣性高but關聯性低)
      top_k = 40, #依照可能性留下最多k個token作為下一個token的選擇, default = 40
      #top-k sampling: 將candidates照機率排序，留下k個後隨機取一作為next token
      top_p = 0.9, #越高輸出多樣性越高, default = 0.9
      #top-p sampling: 留下數個機率相加最接近top_p值的candidate, 取條件機率作為新的權重後取樣
) #create_completion亦可用output取代


#印出response
print(create_completion)
{ #這些都會印出, 至少我還沒找到刪掉的方法
  "id": "cmpl-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "object": "text_completion",
  "created": 1679561337,
  "model": "./models/7B/llama-model.gguf",
  "choices": [
    {
      "text": "Q: Name the planets in the solar system? A: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune and Pluto.",
      #text會是需要留下的部分
      "index": 0,
      "logprobs": None,
      "finish_reason": "stop" #為何停止generate(遇到stop的str = 'stop', 到達長度上限 = 'length')
    }
  ],
  #計算token使用量
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 28,
    "total_tokens": 42
  }
}