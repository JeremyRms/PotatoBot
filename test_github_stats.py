"""
Test script to verify GitHub MCP server configuration and basic statistics functionality.
"""

import asyncio
import os
from mcp_agent.core.fastagent import FastAgent

import yaml
from env_loader import ensure_github_token

def check_github_token():
    """Check if GitHub token is set in fastagent.secrets.yaml or env, try to load it if missing."""
    # Try to ensure token into environment first
    ensured = ensure_github_token(verbose=False)
    if ensured:
        print("✅ GITHUB_TOKEN available for use")
        return True

    secrets_path = "fastagent.secrets.yaml"
    token = None
    if os.path.exists(secrets_path):
        with open(secrets_path, "r") as f:
            try:
                secrets = yaml.safe_load(f)
                token = secrets.get("GITHUB_TOKEN")
            except Exception as e:
                print(f"⚠️  Warning: Could not parse {secrets_path}: {e}")
    if not token:
        print("⚠️  Warning: GITHUB_TOKEN not found in fastagent.secrets.yaml or environment")
        print("   Add it to your secrets file as:\n   GITHUB_TOKEN: your_token_here")
        return False
    print("✅ GitHub token found in fastagent.secrets.yaml")
    return True

async def test_github_connection():
    """Test basic GitHub MCP server connection."""
    try:
        # Ensure token before creating the agent
        ensure_github_token()

        fast = FastAgent("GitHub Test")
        
        @fast.agent(
            name="test_agent",
            instruction="You are a test agent to verify GitHub MCP server connectivity.",
            servers=["github"]
        )
        async def main():
            async with fast.run() as agent:
                print("🔍 Testing GitHub MCP server connection...")
                
                # Test basic repository information
                result = await agent("Get basic information about the 'AlphJeremyRms/PotatoBot' repository")
                print("✅ GitHub MCP server connection successful!")
                print(f"📋 Result: {result}")
                return result
        
        # Call the main function and return its result
        return await main()
                
    except Exception as e:
        print(f"❌ Error connecting to GitHub MCP server: {e}")
        return None

async def test_statistics_tools():
    """Test specific statistics tools."""
    try:
        # Ensure token before creating the agent
        ensure_github_token()

        fast = FastAgent("Statistics Test")
        
        @fast.agent(
            name="stats_test_agent",
            instruction="You are a test agent to verify GitHub statistics tools.",
            servers=["github"]
        )
        async def main():
            async with fast.run() as agent:
                print("📊 Testing GitHub statistics tools...")
                
                # Test repository statistics
                result = await agent("Get the star count, fork count, and language for 'JeremyRms/PotatoBot' repository")
                print("✅ Statistics tools working!")
                print(f"📊 Statistics Result: {result}")
                return result
        
        # Call the main function and return its result
        return await main()
                
    except Exception as e:
        print(f"❌ Error testing statistics tools: {e}")
        return None

async def main():
    """Run all tests."""
    print("🧪 GitHub Statistics Agent Test Suite")
    print("=" * 50)
    
    # Make sure token is loaded into the environment for downstream processes
    if ensure_github_token():
        print("🔐 Using GITHUB_TOKEN from environment")
    else:
        print("⚠️  Proceeding without GITHUB_TOKEN; private repo queries will likely fail")
    
    print("\n" + "=" * 50)
    
    # Test connection
    connection_result = await test_github_connection()
    if connection_result:
        print(f"✅ Connection test completed successfully")
    
    print("\n" + "=" * 50)
    
    # Test statistics tools
    # stats_result = await test_statistics_tools()
    # if stats_result:
    #     print(f"✅ Statistics test completed successfully")
    
    # print("\n" + "=" * 50)
    print("🎉 Test suite completed!")

if __name__ == "__main__":
    asyncio.run(main())
