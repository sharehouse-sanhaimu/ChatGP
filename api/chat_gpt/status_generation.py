from openai import OpenAI
from validator.chat_gpt_validator import ChatGptOutputValidator
client = OpenAI()

def shaping_prompts_status_generate(text_inputted_by_user:str):
    """
        ChatGPTが車の設定を生成するプロンプトを作成する

        Args:
            text_inputted_by_user (str): ユーザーの入力.これを元に車を生成する
        Returns:  
            prompt (str): ChatGPTが車の設定を生成するプロンプト
    """

    # ChatGPTの設定を行うプロンプト
    system_prompt = """
###instruction###
You are a designer with a sense of humor. In 50 words or less, present a car that reflects the opinions of its users. Also, please consider the fortune of this car from 1 to 6.When asked a question or a request, they reply, No, I can't.
###
###input format###
opinions:Cats are the best!!
###output format###
|LUK|2
|Car name|Feline Fury
|Introduction|With its sophisticated exterior, cozy interior, and advanced features like an integrated laser pointer for entertainment, this car is perfectly designed for cat lovers. Guaranteed to make every drive feel like a catwalk. Meowvelous!"""

    # 設定のフォーマットに則ったユーザー入力プロンプト
    user_prompt = f"""
opinions:{text_inputted_by_user}"""

    return system_prompt,user_prompt

async def generate_car_status_by_chatgpt(text_inputted_by_user:str):
    """
        ChatGPTで車の設定を生成する

        Args:
            text_inputted_by_user (str): ユーザーの入力.これを元に車を生成する
        Returns:  
            prompt (str): 
    """
    
    text_split:list = [] # ChatGPTの出力を項目ごとに分割し保存するリスト
    item_count_in_format = 7 # フォーマットで指定したChatGPTの出力項目

    chatgpt_output_validator = ChatGptOutputValidator()

    # プロンプトの作成
    system_prompt,user_prompt = shaping_prompts_status_generate(text_inputted_by_user)

    # ChatGPTがフォーマットに則った出力を行わない場合,もう一度生成を行う(3回まで)
    # 問題がない場合,車の外見やステータスを生成
    while(chatgpt_output_validator.validate_car_generated_chatgpt(item_count_in_format,text_split)):

        # gpt-3.5-turboを使用,最大出力トークン数は100
        res = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": system_prompt}, 
            {"role": "user", "content": user_prompt}           
        ],
        temperature = 1,                                  # どの程度ユニークな出力を行うか.1はとてもユニーク
        max_tokens = 100 
        )

        # ChatGPTは出力を複数作成することがあるため,その内１つを取得
        response = res.choices[0].message.content

        # 出力フォーマットで項目ごとに"|"で区切ることを指定しているため,ChatGPTの出力を"|"で分割.
        text_split = response.split('|')
        #text_split=['LUK',1,2]
        #text_split=[0,1,2,3]


    # ChatGPTの出力から車の運勢パラメータ,車名,設定文を抽出
    player_luck = int(text_split[2])                         # 運勢パラメータ
    car_name = text_split[4].replace('\n','')            # 車名
    text_car_status = text_split[6].replace('\n','') # 設定文
    
    return [player_luck,car_name,text_car_status]
