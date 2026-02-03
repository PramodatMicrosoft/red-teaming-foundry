"""
Azure AI Red Team Evaluation Runbook

This script provides examples for running red team security evaluations
against AI systems using Azure AI Evaluation SDK.

Usage:
    python runbook.py

Options:
    1. Basic Red Team Scan - Uses a callback function as target
    2. Intermediary Scan - Uses Azure OpenAI model configuration as target
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Azure imports
from azure.identity import AzureCliCredential
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

    [3] Display Attack Strategies
        - List all available attack strategies

    [0] Exit
    """)
    print("=" * 70)


async def main():
    """Main entry point with interactive menu."""
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (0-3): ").strip()
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
            display_attack_strategies()
        elif choice == "0":
            print("\nExiting. Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please enter 0, 1, 2, or 3.")
        
        input("\nPress Enter to continue...")


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    asyncio.run(main())


