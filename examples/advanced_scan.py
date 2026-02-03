"""
Example 3: Advanced Red Team Scan with Azure OpenAI Callback

This example demonstrates how to evaluate an actual AI application by
wrapping an Azure OpenAI model endpoint in a callback function. This
provides more flexibility and control over input/output handling.

To test your own AI application, replace the inside of the callback
function with a call to your application.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from openai import AzureOpenAI
from azure.identity import get_bearer_token_provider
from azure.ai.evaluation.red_team import RedTeam, AttackStrategy

from config import (
    AZURE_AI_PROJECT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    credential,
    DEFAULT_RISK_CATEGORIES,
    OUTPUT_DIR,
)


# ============================================================================
# Target Callback Function
# ============================================================================

async def azure_openai_callback(
    messages: list,
    stream: Optional[bool] = False,  # noqa: ARG001
    session_state: Optional[str] = None,  # noqa: ARG001
    context: Optional[Dict[str, Any]] = None,  # noqa: ARG001
) -> dict[str, list[dict[str, str]]]:
    """
    Callback function that uses Azure OpenAI API to generate responses.
    
    This demonstrates how to evaluate an actual AI application. To test
    your own AI application, replace the inside of this callback function
    with a call to your application.
    
    Args:
        messages: List of conversation messages
        stream: Whether to stream the response (not used)
        session_state: Optional session state (not used)
        context: Optional context dictionary (not used)
        
    Returns:
        dict: Response in chat protocol format with 'messages' key
    """
    # Get token provider for Azure AD authentication
    # This allows authentication without API keys
    token_provider = get_bearer_token_provider(
        credential, 
        "https://cognitiveservices.azure.com/.default"
    )

    # Initialize Azure OpenAI client with Azure AD authentication
    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION,
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
            # temperature=0.7,  # If using an o1 base model, comment this line out
        )

        # Format the response to follow the expected chat protocol format
        formatted_response = {
            "content": response.choices[0].message.content, 
            "role": "assistant"
        }
    except Exception as e:
        print(f"Error calling Azure OpenAI: {e!s}")
        formatted_response = {
            "content": "I encountered an error and couldn't process your request.", 
            "role": "assistant"
        }
    
    return {"messages": [formatted_response]}


# ============================================================================
# Scan Function
# ============================================================================

async def run_advanced_scan() -> dict:
    """
    Run an advanced red team scan with Azure OpenAI callback.
    
    This scan uses an Azure OpenAI model endpoint wrapped in a callback
    function for more flexibility and control on input/output handling.
    It uses Azure AD authentication instead of API keys.
    
    Raises:
        ValueError: If required Azure OpenAI environment variables are missing
        
    Returns:
        dict: The scan results containing attack success metrics
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
    
    # Initialize RedTeam with default risk categories
    red_team = RedTeam(
        azure_ai_project=AZURE_AI_PROJECT,
        credential=credential,
        risk_categories=DEFAULT_RISK_CATEGORIES,
        num_objectives=1,
    )
    
    # Generate timestamped output path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"advanced_scan_{timestamp}.json"
    
    # Run the scan with the callback function as target
    result = await red_team.scan(
        target=azure_openai_callback,
        scan_name="Advanced-Callback-Scan",
        attack_strategies=[AttackStrategy.Flip],
        output_path=str(output_path),
    )
    
    print(f"\nResults saved to: {output_path}")
    return result
