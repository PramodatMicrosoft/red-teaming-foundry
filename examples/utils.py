"""
Utility functions for Azure AI Red Team Evaluation.

This module contains helper functions used across the application,
such as displaying available attack strategies.
"""

from azure.ai.evaluation.red_team import AttackStrategy


def display_attack_strategies():
    """
    Display all available attack strategies in the Azure AI Evaluation SDK.
    
    This function lists all attack strategies that can be used when
    configuring red team scans. Strategies can be combined using
    AttackStrategy.Compose() for more complex attack patterns.
    """
    print("\n" + "=" * 70)
    print("🎯 Available Attack Strategies in Azure AI Evaluation SDK")
    print("=" * 70 + "\n")
    
    # Get all public attributes of AttackStrategy enum
    strategies = [attr for attr in dir(AttackStrategy) if not attr.startswith("_")]
    print(f"Total strategies: {len(strategies)}\n")
    
    for i, strategy in enumerate(strategies, 1):
        value = getattr(AttackStrategy, strategy)
        print(f"  {i:2}. {strategy}: {value}")
    
    print("\n" + "-" * 70)
    print("Tip: Use AttackStrategy.Compose([s1, s2]) to combine strategies")
    print("=" * 70)
