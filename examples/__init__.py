"""
Examples package for Azure AI Red Team Evaluation.

This package contains individual scan examples that can be run
through the main runbook interface.
"""

from .basic_scan import run_basic_scan
from .intermediary_scan import run_intermediary_scan
from .advanced_scan import run_advanced_scan
from .utils import display_attack_strategies

# Note: foundry_agent_demo is imported separately as it uses a different SDK
# from .foundry_agent_demo import run_foundry_agent_demo, run_single_query_demo

__all__ = [
    "run_basic_scan",
    "run_intermediary_scan",
    "run_advanced_scan",
    "display_attack_strategies",
]
