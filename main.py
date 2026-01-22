from browser_use import Agent, ChatGoogle
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    llm = ChatGoogle(model="gemini-flash-latest")
    task = "I want you to create a new reciep with all the ingredients and steps to make a chocolate cake in sop module. https://qa-lyncs.pioapp.net/, login credentials are: qalyncs@gmail.com and password"
    agent = Agent(task=task, llm=llm)
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())