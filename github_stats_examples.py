"""
GitHub Statistics Agent - Example Usage Patterns

This file demonstrates various ways to use the GitHub Statistics Agent
for gathering and analyzing GitHub data and statistics.
"""

import asyncio
from mcp_agent.core.fastagent import FastAgent
from tools_config import tools
from instructions import instruction

# Create the application
fast = FastAgent("GitHub Statistics Examples")

# Define the agent
@fast.agent(
    name="github_stats_agent",
    instruction=instruction,
    servers=["github"],
    tools=tools
)
async def main():
    async with fast.run() as agent:
        print("GitHub Statistics Agent Examples")
        print("=" * 50)
        
        # Example 1: Repository Statistics
        print("\n1. Repository Statistics Example:")
        await agent("Analyze the statistics for repository 'microsoft/vscode' including stars, forks, contributors, and recent activity")
        
        # Example 2: Contributor Analysis
        print("\n2. Contributor Analysis Example:")
        await agent("Get the top 10 contributors for the 'facebook/react' repository and analyze their contribution patterns")
        
        # Example 3: Issue and PR Trends
        print("\n3. Issue and PR Trends Example:")
        await agent("Analyze the issue and pull request trends for 'tensorflow/tensorflow' over the last 3 months")
        
        # Example 4: Language Distribution
        print("\n4. Language Distribution Example:")
        await agent("Compare the programming language distribution across repositories in the 'microsoft' organization")
        
        # Example 5: Search and Discovery
        print("\n5. Search and Discovery Example:")
        await agent("Search for repositories related to 'machine learning' with more than 1000 stars and analyze their common characteristics")
        
        # Example 6: Workflow Analytics
        print("\n6. Workflow Analytics Example:")
        await agent("Analyze the GitHub Actions workflow success rates for 'actions/runner' repository")
        
        # Example 7: Release Analysis
        print("\n7. Release Analysis Example:")
        await agent("Compare release frequency and patterns between 'nodejs/node' and 'python/cpython' repositories")
        
        # Example 8: Community Engagement
        print("\n8. Community Engagement Example:")
        await agent("Analyze community engagement metrics for 'kubernetes/kubernetes' including issue response times and PR review patterns")

if __name__ == "__main__":
    asyncio.run(main())
