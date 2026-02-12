"""
Azure AI Red Team Evaluation Runbook

This script provides an interactive menu to run red team security evaluations
against AI systems using Azure AI Evaluation SDK.

Usage:
    python runbook-v2.py

Options:
    1. Basic Red Team Scan - Uses a callback function as target
    2. Intermediary Scan - Uses Azure OpenAI model configuration as target
    3. Advanced Scan - Uses Azure OpenAI model endpoint in a callback function
    4. Foundry Agent Demo - MCP-powered agent for Microsoft documentation
    5. Display Attack Strategies - List all available strategies
"""

import asyncio

# Import scan functions from examples package
from examples import (
    run_basic_scan,
    run_intermediary_scan,
    run_advanced_scan,
    display_attack_strategies,
)
# Import foundry agent demo separately (uses different SDK)
from examples.foundry_agent_demo import run_foundry_agent_demo


# ============================================================================
# Menu Display
# ============================================================================

def display_menu():
    """Display the main menu options."""
    print("\n" + "=" * 70)
    print("       Azure AI Red Team Evaluation - Main Menu")
    print("=" * 70)
    print("""
    Select an option:

    [1] Basic Red Team Scan
        - Uses callback function as target
        - Single attack strategy (Flip)
        - Quick evaluation for testing

    [2] Intermediary Red Team Scan  
        - Uses Azure OpenAI model configuration as target
        - Multi-language support (English)
        - Tests base/foundation models directly

    [3] Advanced Red Team Scan
        - Uses Azure OpenAI model endpoint in a callback function
        - Demonstrates how to evaluate actual AI applications
        - Uses Azure AD authentication (no API key required)

    [4] Foundry Agent Demo (MCP)
        - Creates Azure AI Foundry Agent with MCP tool
        - Crawls Microsoft documentation to answer queries
        - Interactive conversation mode

    [5] Display Attack Strategies
        - List all available attack strategies

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
            choice = input("\nEnter your choice (0-5): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nExiting...")
            break
        
        if choice == "1":
            result = await run_basic_scan()
            print("\n✅ Basic scan completed!")
        elif choice == "2":
            result = await run_intermediary_scan()
            print("\n✅ Intermediary scan completed!")
        elif choice == "3":
            result = await run_advanced_scan()
            print("\n✅ Advanced scan completed!")
        elif choice == "4":
            await run_foundry_agent_demo()
            print("\n✅ Foundry Agent demo completed!")
        elif choice == "5":
            display_attack_strategies()
        elif choice == "0":
            print("\nExiting. Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please enter 0, 1, 2, 3, 4, or 5.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    asyncio.run(main())


