import json
import asyncio
import requests
import websockets
from openai import OpenAI
from actions import ClickAction, TypeAction
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize OpenAI Client
client = OpenAI()

class OpenAIBrowserAgent:
    def __init__(self):
        self.ws_url = self._get_chrome_ws()
        # Define tools for OpenAI
        self.tools = [
            {"type": "function", "function": {"name": "ClickAction", "parameters": ClickAction.model_json_schema()}},
            {"type": "function", "function": {"name": "TypeAction", "parameters": TypeAction.model_json_schema()}}
        ]

    def _get_chrome_ws(self):
        """Automatically find the debugger URL on your Mac."""
        try:
            resp = requests.get("http://127.0.0.1:9222/json").json()
            return [t for t in resp if t['type'] == 'page'][0]['webSocketDebuggerUrl']
        except:
            raise Exception("Chrome not found! Run the Mac terminal command first.")

    async def send_cdp(self, method, params):
        """Phase 2: The Raw Wire (CDP)"""
        async with websockets.connect(self.ws_url) as ws:
            message = {"id": 1, "method": method, "params": params}
            await ws.send(json.dumps(message))
            return await ws.recv()

    async def run_step(self, goal, state):
        """Phase 4: The Reasoning Loop"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a web agent. Use tools to achieve the goal."},
                {"role": "user", "content": f"Goal: {goal}\nState: {state}"}
            ],
            tools=self.tools,
            tool_choice="required"
        )

        tool_call = response.choices[0].message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        
        # BRIDGE: Logic to map AI decision to Browser Protocol
        if tool_call.function.name == "ClickAction":
            print(f"🎯 OpenAI wants to click ID: {args['element_id']}")
            # In Phase 3, you'd look up coordinates. For now, we mock (500, 400)
            await self.send_cdp("Input.dispatchMouseEvent", {
                "type": "mousePressed", "x": 500, "y": 400, "button": "left", "clickCount": 1
            })
            await self.send_cdp("Input.dispatchMouseEvent", {
                "type": "mouseReleased", "x": 500, "y": 400, "button": "left", "clickCount": 1
            })

# --- EXECUTION ---
async def main():
    agent = OpenAIBrowserAgent()
    await agent.run_step("Click the search bar", "Current State: A search box is visible with label [5].")

if __name__ == "__main__":
    asyncio.run(main())