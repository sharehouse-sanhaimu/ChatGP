import random
from fastapi import  HTTPException,status
from transformers import GPT2Tokenizer

class ChatGptOutputValidator():
    def __init__(self) -> None:
        self.error_count = 0
        
    def _luk_is_number(self,output_chatgpt:str) -> bool:
        """
        ChatGPTが出力した車のlukが数字になっているか確認
        3回失敗したらエラーを出力
        Args:
            result (list): ChatGPTの出力を分割して格納したリスト.
            error_count (int): フォーマットに従わない出力が行われた回数
        Returns:
            bool: returnは正常/異常(0/1)
        Raises:
            HTTP_408_REQUEST_TIMEOUT: ChatGPTが LUK(int)|NAME(str)|TEXT(str) のフォーマットに従っていない.
        """
        # lukが数値になっているか?
        try:
            _ = int(output_chatgpt)
            
            return True
        except:
            print("generated luck value:" + str(output_chatgpt))

            return False

    def _is_correct_gpt_output(self,item_count_in_format:int,output_chatgpt:list) -> bool:
        """
        ChatGPTが出力した項目の数がフォーマットに則っているか確認する
        3回失敗したらエラーを出力
        Args:
            result (list): ChatGPTの出力を項目事に分割して格納したリスト
            item_count_in_format (int): フォーマットで指定した出力項目の数
            error_count (int): フォーマットに従わない出力が行われた回数
        Returns:
            bool: returnは正常/異常(0/1)
        Raises:
            HTTP_408_REQUEST_TIMEOUT: ChatGPTの出力がフォーマットに則っていない
        """
        # 出力された項目の数が指定のものと一致すか. 一致/不一致(True/False)
        # 判定を行うたびにerror_countを増加させ,4回になった際に408エラーを発生.
        if len(output_chatgpt) == item_count_in_format:
            return True
        else:
            print("Number of items output:"+str(len(output_chatgpt))+",Output_text" + str(output_chatgpt))

            return False

    def validate_car_generated_chatgpt(self,item_count_in_format:int,output_chatgpt:list):
        print(output_chatgpt)
        if not(self._is_correct_gpt_output(item_count_in_format,output_chatgpt)):
            self.error_count += 1

        elif not(self._luk_is_number(output_chatgpt[2])):
            self.error_count += 1

        else:
            return False


        if self.error_count >= 4:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="ChatGPT output does not follow the format",
            )
        
        return True

    def validate_scenario_generated_by_chatgpt(self,item_count_in_format:int,output_chatgpt:list):
        print(output_chatgpt)
        if not(self._is_correct_gpt_output(item_count_in_format,output_chatgpt)):
            self.error_count += 1
        else:
            return False

        if self.error_count >= 4:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="ChatGPT output does not follow the format",
            )
        
        return True



tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def validate_token_count(text:str,token_num:int) -> bool:
    
    """
        ユーザーの入力トークン数が上限を超えていないかのチェック
        上限を超えるとエラーを出力
        Args:
            text (str): ユーザーの入力
            token_num (int): トークンの上限
        Returns:
            bool: returnは正常/異常(1/0)
        Raises:
            HTTP_400_BAD_REQUEST: ユーザーの入力がトークンの上限を超えた.
    """
    # ChatGPTで処理する場合のトークン数をカウント
    # 指定した上限を超えた場合400エラーを発生
    tokens = tokenizer.tokenize(text)
    if len(tokens) <= token_num:
        return True
    else:
        print("text_inputted_by_user:"+text)
        print("token_num:"+str(token_num))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of tokens has exceeded the input limit.",
        )



