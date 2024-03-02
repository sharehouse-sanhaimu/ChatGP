from fastapi import APIRouter
from fastapi.responses import Response
from chat_gpt.image_generation import image_generate_chatgpt


router = APIRouter()

@router.get("/{prayer}")
def make_car(prayer: str,text: str):
    car_img_binary = image_generate_chatgpt(text)

    return Response(content=car_img_binary, media_type="image/png")