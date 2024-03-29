from openai import OpenAI
from validator.chat_gpt_validator import ChatGptOutputValidator
from models import RaceModeratorModel


client = OpenAI()

def shaping_prompts_rece_moderator(race_moderator_model:RaceModeratorModel):
    """
        ChatGPTにレースのシナリオを生成させるプロンプトを作成

        Args:
            ending_model (RaceModeratorModel):レースに参加している車の情報
        Returns:  
            prompt (str): ChatGPTがレースの進行を行うためのプロンプト
    """

    # ChatGPTの設定を行うプロンプト
    prompt_system = f"""
You are the live commentator for the Race Cup.
You will give the names of the four participating cars, their current standings and the events that have occurred.
Predict the outcome of the event and any changes in the standings and output them according to the format.

###car_data###
car_name:{race_moderator_model.second_car_name}
instruction:{race_moderator_model.second_car_instruction}

car_name:{race_moderator_model.fourth_car_name}
car_instruction:{race_moderator_model.fourth_car_instruction}

car_name:{race_moderator_model.first_car_name}
car_instruction:{race_moderator_model.first_car_instruction}

car_name:{race_moderator_model.third_car_name}
car_instruction:{race_moderator_model.third_car_instruction}

###input format###
**race position**
|1th|{race_moderator_model.second_car_name}
|2nd|{race_moderator_model.third_car_name}
|3rd|{race_moderator_model.first_car_name}
|4th|{race_moderator_model.fourth_car_name}
|event|Actions of {race_moderator_model.first_car_name}:I'm going to crash into the car in front of me by accelerating!

###event###
{race_moderator_model.first_car_name} just rammed into the car in front!

###output format###
|1th|{race_moderator_model.second_car_name}
|2nd|{race_moderator_model.first_car_name}
|3rd|{race_moderator_model.third_car_name}
|4th|{race_moderator_model.fourth_car_name}
|result|Oops! {race_moderator_model.first_car_name} hit the car in front of him! What a wild ride! {race_moderator_model.first_car_name} in front of him spun wide!"""

    # 設定のフォーマットに則ったユーザー入力プロンプト
    prompt_user = f"""
**race position**
|1th|{race_moderator_model.first_car_name}
|2nd|{race_moderator_model.second_car_name}
|3rd|{race_moderator_model.third_car_name}
|4th|{race_moderator_model.fourth_car_name}
|event|Actions of {race_moderator_model.player_car_name}:{race_moderator_model.event}"""

    return prompt_system,prompt_user



def generate_race_scenario(race_moderator_model:RaceModeratorModel):
    """
        ChatGPTがユーザーの入力を受け取り,その入力を元にシナリオを作成する

        Args:
            ending_model (RaceModeratorModel):レースに参加している車の情報
        Returns:  
            text_scenario (str): ChatGPTが生成したシナリオ文
            first (str): １位の車名
            second (str): ２位の車名
            third (str): ３位の車名
            fourth (str): ４位の車名
    """

    text_split:list = [] # ChatGPTの出力を項目ごとに分割し保存するリスト
    item_count_in_format:int = 11 # フォーマットで指定したChatGPTの出力項目

    chatgpt_output_validator = ChatGptOutputValidator()

    # ChatGPTがフォーマットに則った出力を行わない場合,もう一度生成を行う(3回まで)
    # 問題がない場合レースのシナリオを生成する
    while(chatgpt_output_validator.validate_scenario_generated_by_chatgpt(item_count_in_format,text_split)):
        prompt_system,prompt_user = shaping_prompts_rece_moderator(race_moderator_model)

        # gpt-3.5-turboを使用,最大出力トークン数は200
        res = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system","content":prompt_system}, 
            {"role": "user", "content": prompt_user}         
            ],
        temperature = 1, # どの程度ユニークな出力を行うか.1はとてもユニーク
        max_tokens = 200  
        )

        # ChatGPTは出力を複数作成することがあるため,その内１つを取得
        response = res.choices[0].message.content  

        # 出力フォーマットで項目ごとに"|"で区切ることを指定しているため,ChatGPTの出力を"|"で分割.
        text_split = response.split('|')
        #text_split=[i for i in range(8)]

    # ChatGPTの出力から順位とイベントを抽出
    first = text_split[2].replace('\n','')
    second = text_split[4].replace('\n','')
    third = text_split[6].replace('\n','')
    fourth = text_split[8].replace('\n','')
    text_scenario = text_split[10].replace('\n','')
    
    return text_scenario,first,second,third,fourth