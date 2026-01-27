from pydantic import BaseModel, Field
from typing import Literal
from google import genai
from google.genai import types
import websockets
import json
from dotenv import load_dotenv

load_dotenv()

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

class ClickAction(BaseModel):
    element_id: int = Field(..., description="The ID of the element to click")

class TypeAction(BaseModel):
    element_id: int = Field(..., description="The ID of the element to type into")
    text: str = Field(..., description="The text to type into the element")
    press_enter: bool = Field(False, description="Whether to press enter after typing")






async def run_agent_loop(goal, compressed_state):
    messages = [
        {
            "role": "system",
            "content": """
            Analyse the state and pick the best action to take to achieve the goal.
            """
        },
        {
            "role": "user",
            "content": f"""
            Goal: {goal}
            State: {compressed_state}
            """
        }

    ]


    chat = client.chats.create(
        model="gemini-2.0-flash", # Use the latest flash model for speed
        config=types.GenerateContentConfig(
            system_instruction="You are a web agent. Use tools to reach the goal.",
            tools=[ClickAction, TypeAction]
        )
    )



async def bridge_to_browser(response_part):
    if response_part.function_call:
        name = response_part.function_call.name
        args = response_part.function_call.args

        if name == "ClickAction":
            x, y = get_coordinates(args["element_id"])

            cdp_message = {
                "id": 1,
                "method": "Input.dispatchMouseEvent",
                "params": {
                    "type": "mousePressed",
                    "x": x,
                    "y": y,
                    "button": "left",
                    "clickCount": 1
                }
            }

            await websocket.send(json.dumps(cdp_message))

