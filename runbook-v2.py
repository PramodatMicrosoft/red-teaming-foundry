"""
Azure AI Red Team Evaluation Runbook

This script provides examples for running red team security evaluations
against AI systems using Azure AI Evaluation SDK.

Usage:
    python runbook.py

Options:
    1. Basic Red Team Scan - Uses a callback function as target
    2. Intermediary Scan - Uses Azure OpenAI model configuration as target
    3. Advanced Scan - Uses Azure OpenAI model endpoint in a callback function
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from openai import AzureOpenAI

# Azure imports
from azure.identity import AzureCliCredential, get_bearer_token_provider
from azure.ai.evaluation.red_team import RedTeam, RiskCategory, AttackStrategy, SupportedLanguages
from azure.ai.projects import AIProjectClient

# Note: These are from an internal module - API may change in future versions
from azure.ai.evaluation._common.onedp.models import (
    AgentTaxonomyInput,
    AzureAIAgentTarget,
    DailyRecurrenceSchedule,
    EvaluationScheduleTask,
    EvaluationTaxonomy,
    RecurrenceTrigger,
    RiskCategory as ProjectsRiskCategory,
    Schedule,
)

# ============================================================================
# Configuration
# ============================================================================

# Load environment variables
load_dotenv()

# Initialize Azure credentials ('az login' required before running)
credential = AzureCliCredential()

# Azure AI Project information
AZURE_AI_PROJECT = os.environ.get("AZURE_PROJECT_ENDPOINT")
if AZURE_AI_PROJECT is None:
    raise ValueError("AZURE_PROJECT_ENDPOINT environment variable is required")

# Azure OpenAI deployment information
# Support both naming conventions (DEPLOYMENT and DEPLOYMENT_NAME)
AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT") or os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")

if AZURE_OPENAI_API_VERSION:
    os.environ["OPENAI_API_VERSION"] = AZURE_OPENAI_API_VERSION

# Output directory for scan results
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# Default risk categories for red team evaluation
DEFAULT_RISK_CATEGORIES = [
    RiskCategory.Violence,
    RiskCategory.HateUnfairness,
    RiskCategory.Sexual,
    RiskCategory.SelfHarm,
    RiskCategory.ProtectedMaterial,
    RiskCategory.CodeVulnerability,
    RiskCategory.UngroundedAttributes,
]

# ============================================================================
# Target Callback Functions
# ============================================================================

def financial_advisor_callback(query: str) -> str:
    """Simple callback function simulating a financial advisor assistant."""
    return (
        "I'm a financial advisor assistant. I can help with investment advice "
        "and financial planning within legal and ethical guidelines."
    )


async def azure_openai_callback(
    messages: list,
    stream: Optional[bool] = False,  # noqa: ARG001
    session_state: Optional[str] = None,  # noqa: ARG001
    context: Optional[Dict[str, Any]] = None,  # noqa: ARG001
) -> dict[str, list[dict[str, str]]]:
    """
    Callback function that uses Azure OpenAI API to generate responses.
    
    This demonstrates how to evaluate an actual AI application.
    To test your own AI application, replace the inside of this callback
    function with a call to your application.
    """
    # Get token provider for Azure AD authentication
    token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION or "2024-02-15-preview",
        azure_ad_token_provider=token_provider,
    )

    # Extract the latest message from the conversation history
    messages_list = [{"role": message.role, "content": message.content} for message in messages]
    latest_message = messages_list[-1]["content"]

    try:
        # Call the model
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "user", "content": latest_message},
            ],
            # max_tokens=500,  # If using an o1 base model, comment this line out
            max_completion_tokens=500,  # If using an o1 base model, uncomment this line
            # temperature=0.7,  # If using an o1 base model, comment this line out (temperature param not supported)
        )

        # Format the response to follow the expected chat protocol format
        formatted_response = {"content": response.choices[0].message.content, "role": "assistant"}
    except Exception as e:
        print(f"Error calling Azure OpenAI: {e!s}")
        formatted_response = {"content": "I encountered an error and couldn't process your request.", "role": "assistant"}
    return {"messages": [formatted_response]}

# ============================================================================
# Red Team Scan Examples
# ============================================================================

async def run_basic_scan() -> dict:
    """
    Example 1: Basic Red Team Scan with Callback Function
    
    This scan tests a simple callback function target with the Flip attack strategy.
    The key metric is Attack Success Rate (ASR) - percentage of attacks that 
    successfully elicit harmful content from your AI system.
    """
    print("\n" + "=" * 70)
    print("Running Basic Red Team Scan with Callback Function")
    print("=" * 70)
    
    red_team = RedTeam(
        azure_ai_project=AZURE_AI_PROJECT,
        credential=credential,
        risk_categories=DEFAULT_RISK_CATEGORIES,
        num_objectives=1,
    )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"basic_scan_{timestamp}.json"
    
    result = await red_team.scan(
        target=financial_advisor_callback,
        scan_name="Basic-Callback-Scan",
        attack_strategies=[AttackStrategy.Flip],
        output_path=str(output_path),
    )
    
    print(f"\nResults saved to: {output_path}")
    return result


async def run_intermediary_scan() -> dict:
    """
    Example 2: Intermediary Red Team Scan with Model Configuration
    
    This scan tests an Azure OpenAI model configuration as target.
    Uses the model config directly to test base/foundation models.
    Includes multi-language support (English) for broader coverage.
    """
    print("\n" + "=" * 70)
    print("Running Intermediary Red Team Scan with Model Configuration")
    print("=" * 70)
    
    # Validate required environment variables for model config
    if not all([AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_API_KEY]):
        raise ValueError(
            "Missing required environment variables for model configuration. "
            "Please set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, and AZURE_OPENAI_API_KEY."
        )
    
    # Define a model configuration to test base/foundation models
    # Include api_version to ensure proper communication with Azure OpenAI
    azure_oai_model_config = {
        "azure_endpoint": AZURE_OPENAI_ENDPOINT,
        "azure_deployment": AZURE_OPENAI_DEPLOYMENT,
        "api_key": AZURE_OPENAI_API_KEY,
        "api_version": AZURE_OPENAI_API_VERSION or "2024-02-15-preview",
    }
    
    # Create RedTeam instance with English language support
    red_team = RedTeam(
        azure_ai_project=AZURE_AI_PROJECT,
        credential=credential,
        language=SupportedLanguages.English,
        num_objectives=1,
    )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"intermediary_scan_{timestamp}.json"
    
    # Run the scan with model configuration as target
    result = await red_team.scan(
        target=azure_oai_model_config,
        scan_name="Intermediary-Model-Target-Scan",
        attack_strategies=[AttackStrategy.Flip],
        output_path=str(output_path),
    )
    
    print(f"\nResults saved to: {output_path}")
    return result


async def run_advanced_scan() -> dict:
    """
    Example 3: Advanced Red Team Scan with Azure OpenAI Callback
    
    This scan uses an Azure OpenAI model endpoint wrapped in a callback function
    for more flexibility and control on input/output handling.
    
    This demonstrates how to evaluate an actual AI application.
    To test your own AI application, replace the callback function internals.
    """
    print("\n" + "=" * 70)
    print("Running Advanced Red Team Scan with Azure OpenAI Callback")
    print("=" * 70)
    
    # Validate required environment variables
    if not all([AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT]):
        raise ValueError(
            "Missing required environment variables for advanced scan. "
            "Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT."
        )
    
    red_team = RedTeam(
        azure_ai_project=AZURE_AI_PROJECT,
        credential=credential,
        risk_categories=DEFAULT_RISK_CATEGORIES,
        num_objectives=1,
    )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"advanced_scan_{timestamp}.json"
    
    result = await red_team.scan(
        target=azure_openai_callback,
        scan_name="Advanced-Callback-Scan",
        attack_strategies=[AttackStrategy.Flip],
        output_path=str(output_path),
    )
    
    print(f"\nResults saved to: {output_path}")
    return result

# ============================================================================
# Utility Functions
# ============================================================================

def display_attack_strategies():
    """Display all available attack strategies in the Azure AI Evaluation SDK."""
    print("\n" + "=" * 70)
    print("🎯 Available Attack Strategies in Azure AI Evaluation SDK")
    print("=" * 70 + "\n")
    
    strategies = [attr for attr in dir(AttackStrategy) if not attr.startswith("_")]
    print(f"Total strategies: {len(strategies)}\n")
    
    for i, strategy in enumerate(strategies, 1):
        value = getattr(AttackStrategy, strategy)
        print(f"  {i:2}. {strategy}: {value}")
    
    print("\n" + "-" * 70)
    print("Tip: Use AttackStrategy.Compose([s1, s2]) to combine strategies")
    print("=" * 70)


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

    [4] Display Attack Strategies
        - List all available attack strategies

    [0] Exit
    """)
    print("=" * 70)


async def main():
    """Main entry point with interactive menu."""
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (0-4): ").strip()
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
            display_attack_strategies()
        elif choice == "0":
            print("\nExiting. Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please enter 0, 1, 2, 3, or 4.")
        
        input("\nPress Enter to continue...")


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    asyncio.run(main())


