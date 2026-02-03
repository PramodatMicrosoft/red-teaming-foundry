"""
Example 2: Intermediary Red Team Scan with Model Configuration

This example demonstrates how to run a red team scan using an Azure OpenAI
model configuration as the target. This approach allows you to test
base/foundation models directly without wrapping them in a callback.

Use this when you want to evaluate the raw model's behavior before adding
application-level safety measures.
"""

from datetime import datetime

from azure.ai.evaluation.red_team import RedTeam, AttackStrategy, SupportedLanguages

from config import (
    AZURE_AI_PROJECT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    credential,
    OUTPUT_DIR,
)


# ============================================================================
# Scan Function
# ============================================================================

async def run_intermediary_scan() -> dict:
    """
    Run an intermediary red team scan with model configuration as target.
    
    This scan tests an Azure OpenAI model configuration directly, which is
    useful for evaluating base/foundation models. It includes support for
    multi-language testing.
    
    Raises:
        ValueError: If required Azure OpenAI environment variables are missing
        
    Returns:
        dict: The scan results containing attack success metrics
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
    # This configuration uses API key authentication
    azure_oai_model_config = {
        "azure_endpoint": AZURE_OPENAI_ENDPOINT,
        "azure_deployment": AZURE_OPENAI_DEPLOYMENT,
        "api_key": AZURE_OPENAI_API_KEY,
        "api_version": AZURE_OPENAI_API_VERSION,
    }
    
    # Create RedTeam instance with English language support
    # Change SupportedLanguages.English to other languages as needed
    red_team = RedTeam(
        azure_ai_project=AZURE_AI_PROJECT,
        credential=credential,
        language=SupportedLanguages.English,
        num_objectives=1,
    )
    
    # Generate timestamped output path
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
