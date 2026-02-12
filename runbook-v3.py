"""
Azure AI Foundry Agent Demonstration Runbook

This script demonstrates Azure AI Foundry Agents using Model Context Protocol (MCP)
to search Microsoft documentation and answer user queries.

Usage:
    python runbook-v3.py

Options:
    1. Interactive Demo - Interactive conversation with MCP-powered agent
    2. Single Query Demo - Run a single query against Microsoft docs
"""

import asyncio

# Import foundry agent demo (uses Microsoft Agent Framework)
from examples.foundry_agent_demo import run_foundry_agent_demo, run_single_query_demo


# ============================================================================
# Menu Display
# ============================================================================

def display_menu():
    """Display the main menu options."""
    print("\n" + "=" * 70)
    print("       Azure AI Foundry Agent Demo - Main Menu")
    print("=" * 70)
    print("""
    This demo showcases Azure AI Foundry Agents with Model Context Protocol
    (MCP) to search and retrieve information from Microsoft documentation.

    Select an option:

    [1] Interactive Demo
        - Creates an Azure AI Agent with MCP tool
        - Connects to Microsoft Learn documentation
        - Interactive conversation mode (type 'exit' to quit)

    [2] Single Query Demo
        - Run a single query against Microsoft documentation
        - Quick demonstration of MCP capabilities

    [0] Exit
    """)
    print("=" * 70)


# ============================================================================
# Main Entry Point
# ============================================================================

async def main():
    """Main entry point with interactive menu."""
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (0-2): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nExiting...")
            break
        
        if choice == "1":
            await run_foundry_agent_demo()
            print("\n✅ Interactive demo completed!")
        elif choice == "2":
            # Optionally get custom query from user
            custom_query = input("\nEnter your query (or press Enter for default): ").strip()
            if custom_query:
                await run_single_query_demo(query=custom_query)
            else:
                await run_single_query_demo()
            print("\n✅ Single query demo completed!")
        elif choice == "0":
            print("\nExiting. Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please enter 0, 1, or 2.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    asyncio.run(main())
