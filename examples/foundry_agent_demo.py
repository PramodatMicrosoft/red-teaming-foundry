"""
Foundry Agent Demo with MCP for Microsoft Documentation.

This example demonstrates how to create an Azure AI Agent
that uses Model Context Protocol (MCP) to crawl Microsoft documentation
and answer user queries using the Microsoft Agent Framework.
"""

import asyncio
from azure.identity import AzureCliCredential
from agent_framework import MCPStreamableHTTPTool
from agent_framework.azure import AzureOpenAIResponsesClient

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION,
)


# ============================================================================
# MCP Configuration
# ============================================================================

# Microsoft Learn MCP endpoint for documentation access
MICROSOFT_DOCS_MCP_URL = "https://learn.microsoft.com/api/mcp"


async def run_foundry_agent_demo():
    """
    Run the Foundry Agent demo with MCP for Microsoft documentation.
    
    This demo creates an agent that can:
    - Search Microsoft documentation using MCP
    - Answer questions about Azure, Microsoft products, and services
    - Provide accurate, up-to-date information from official docs
    """
    print("\n" + "=" * 70)
    print("🤖 Foundry Agent Demo - MCP for Microsoft Documentation")
    print("=" * 70)
    
    # Validate configuration
    if not AZURE_OPENAI_ENDPOINT:
        raise ValueError("AZURE_OPENAI_ENDPOINT not set")
    if not AZURE_OPENAI_DEPLOYMENT:
        raise ValueError("AZURE_OPENAI_DEPLOYMENT or AZURE_OPENAI_DEPLOYMENT_NAME not set")
    
    print(f"\n📋 Configuration:")
    print(f"   Azure OpenAI Endpoint: {AZURE_OPENAI_ENDPOINT[:50]}...")
    print(f"   Model Deployment: {AZURE_OPENAI_DEPLOYMENT}")
    print(f"   MCP Server: {MICROSOFT_DOCS_MCP_URL}")
    
    # Create Azure OpenAI Responses client with Azure AD authentication
    credential = AzureCliCredential()
    
    responses_client = AzureOpenAIResponsesClient(
        credential=credential,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        api_version=AZURE_OPENAI_API_VERSION or "2024-12-01-preview",
    )
    
    # Define agent instructions
    agent_instructions = """
You are a helpful Microsoft documentation assistant. Your primary role is to help users 
find accurate information from official Microsoft documentation using the MCP tool.

Guidelines:
1. Always use the Microsoft Learn MCP tool to search for information
2. Provide accurate, up-to-date answers based on official documentation
3. Include relevant links or references when possible
4. If you cannot find the information, clearly state that
5. Focus on Azure, Microsoft 365, Windows, and other Microsoft products/services

When answering:
- Be concise but thorough
- Use bullet points for lists
- Include code examples when relevant
- Cite the documentation source
"""
    
    # Create the agent
    agent = responses_client.as_agent(
        name="Microsoft Docs Assistant",
        instructions=agent_instructions,
    )
    
    print(f"\n✅ Agent created: {agent.name}")
    
    # Interactive conversation loop with MCP
    print("\n" + "-" * 70)
    print("💬 Interactive Mode - Ask questions about Microsoft documentation")
    print("   Type 'exit' or 'quit' to end the session")
    print("-" * 70)
    
    # Connect to Microsoft Learn MCP server
    async with MCPStreamableHTTPTool(
        name="Microsoft Learn MCP",
        url=MICROSOFT_DOCS_MCP_URL,
    ) as mcp_tool:
        print(f"\n🔗 Connected to Microsoft Learn MCP server")
        
        while True:
            # Get user input
            try:
                user_input = input("\n🧑 You: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\n👋 Ending conversation session...")
                break
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Ending conversation session...")
                break
            
            # Process the query with MCP tool
            print("\n⏳ Searching Microsoft documentation...")
            
            try:
                result = await agent.run(user_input, tools=mcp_tool)
                print(f"\n🤖 Assistant: {result.text}")
            except Exception as e:
                print(f"\n❌ Error processing query: {e}")
    
    print("\n✅ Demo completed successfully!")
    print("=" * 70)


async def run_single_query_demo(query: str | None = None):
    """
    Run a single query demo (non-interactive mode).
    
    Args:
        query: Optional query string. If not provided, uses a default query.
    """
    default_query = "How do I create an Azure Storage account using Azure CLI?"
    query = query or default_query
    
    print("\n" + "=" * 70)
    print("🤖 Foundry Agent - Single Query Demo")
    print("=" * 70)
    
    print(f"\n📋 Query: {query}")
    
    # Create Azure OpenAI Responses client
    credential = AzureCliCredential()
    
    responses_client = AzureOpenAIResponsesClient(
        credential=credential,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        api_version=AZURE_OPENAI_API_VERSION or "2024-12-01-preview",
    )
    
    agent_instructions = """
You are a helpful Microsoft documentation assistant. Use the MCP tool to search 
Microsoft documentation and provide accurate, concise answers with code examples when relevant.
"""
    
    # Create agent
    agent = responses_client.as_agent(
        name="Docs Query Agent",
        instructions=agent_instructions,
    )
    
    print(f"\n⏳ Processing query with MCP tool...")
    
    # Connect to MCP and run query
    async with MCPStreamableHTTPTool(
        name="Microsoft Learn MCP",
        url=MICROSOFT_DOCS_MCP_URL,
    ) as mcp_tool:
        try:
            result = await agent.run(query, tools=mcp_tool)
            print(f"\n🤖 Response:\n{result.text}")
        except Exception as e:
            print(f"\n❌ Query failed: {e}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(run_foundry_agent_demo())
