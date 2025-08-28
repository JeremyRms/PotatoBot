import asyncio
from mcp_agent.core.fastagent import FastAgent
from tools_config import tools
from instructions import instruction

# Create the application
fast = FastAgent("GitHub Stats Agent")

# Define the agent
@fast.agent(
    name="github_stats_agent",
    instruction=instruction,
    servers=["github"],
    tools=tools,
    use_history=True,
    human_input=True,
)
async def main() -> None:
    async with fast.run() as agent:
        print("GitHub Stats Agent ready. Type your request:")
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
