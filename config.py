"""
Shared configuration for Azure AI Red Team Evaluation.

This module contains all shared configuration, credentials, and constants
used across the different scan examples.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from azure.ai.evaluation.red_team import RiskCategory

# ============================================================================
# Load Environment Variables
# ============================================================================

load_dotenv()

# ============================================================================
# Azure Credentials
# ============================================================================

# Initialize Azure credentials ('az login' required before running)
credential = AzureCliCredential()

# ============================================================================
# Azure AI Project Configuration
# ============================================================================

AZURE_AI_PROJECT = os.environ.get("AZURE_PROJECT_ENDPOINT")
if AZURE_AI_PROJECT is None:
    raise ValueError("AZURE_PROJECT_ENDPOINT environment variable is required")

# ============================================================================
# Azure OpenAI Configuration
# ============================================================================

# Support both naming conventions (DEPLOYMENT and DEPLOYMENT_NAME)
AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT") or os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION") or "2024-02-15-preview"

# Set OpenAI API version environment variable
if AZURE_OPENAI_API_VERSION:
    os.environ["OPENAI_API_VERSION"] = AZURE_OPENAI_API_VERSION

# ============================================================================
# Output Configuration
# ============================================================================

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================================
# Default Risk Categories
# ============================================================================

DEFAULT_RISK_CATEGORIES = [
    RiskCategory.Violence,
    RiskCategory.HateUnfairness,
    RiskCategory.Sexual,
    RiskCategory.SelfHarm,
    RiskCategory.ProtectedMaterial,
    RiskCategory.CodeVulnerability,
    RiskCategory.UngroundedAttributes,
]
