"""
Example 1: Basic Red Team Scan with Callback Function

This example demonstrates a basic red team scan using a simple callback
function as the target. It's useful for quick testing and understanding
the fundamental concepts of red teaming.

The key metric is Attack Success Rate (ASR) - percentage of attacks that
successfully elicit harmful content from your AI system.
"""

from datetime import datetime

from azure.ai.evaluation.red_team import RedTeam, AttackStrategy

from config import (
    AZURE_AI_PROJECT,
    credential,
    DEFAULT_RISK_CATEGORIES,
    OUTPUT_DIR,
)


# ============================================================================
# Target Callback Function
# ============================================================================

def financial_advisor_callback(query: str) -> str:
    """
    Simple callback function simulating a financial advisor assistant.
    
    This is a placeholder target for testing. In a real scenario, you would
    replace this with a call to your actual AI application or service.
    
    Args:
        query: The user's input query
        
    Returns:
        A response string from the simulated assistant
    """
    return (
        "I'm a financial advisor assistant. I can help with investment advice "
        "and financial planning within legal and ethical guidelines."
    )


# ============================================================================
# Scan Function
# ============================================================================

async def run_basic_scan() -> dict:
    """
    Run a basic red team scan with a callback function target.
    
    This scan tests a simple callback function target with the Flip attack
    strategy. The Flip strategy attempts to reverse the meaning of prompts
    to elicit harmful responses.
    
    Returns:
        dict: The scan results containing attack success metrics
    """
    print("\n" + "=" * 70)
    print("Running Basic Red Team Scan with Callback Function")
    print("=" * 70)
    
    # Initialize RedTeam with default risk categories
    red_team = RedTeam(
        azure_ai_project=AZURE_AI_PROJECT,
        credential=credential,
        risk_categories=DEFAULT_RISK_CATEGORIES,
        num_objectives=1,
    )
    
    # Generate timestamped output path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"basic_scan_{timestamp}.json"
    
    # Run the scan
    result = await red_team.scan(
        target=financial_advisor_callback,
        scan_name="Basic-Callback-Scan",
        attack_strategies=[AttackStrategy.Flip],
        output_path=str(output_path),
    )
    
    print(f"\nResults saved to: {output_path}")
    return result
