"""
Utility functions for Azure AI Red Team Evaluation.

This module contains helper functions used across the application,
such as displaying available attack strategies and risk categories.
"""

from azure.ai.evaluation.red_team import AttackStrategy, RiskCategory


# Risk category descriptions
RISK_CATEGORY_DESCRIPTIONS = {
    "Violence": "Content promoting or describing physical harm, weapons, or violent acts",
    "HateUnfairness": "Discriminatory, biased, or prejudiced content targeting groups",
    "Sexual": "Inappropriate sexual content or explicit material",
    "SelfHarm": "Content promoting suicide, self-injury, or dangerous behaviors",
    "ProtectedMaterial": "Copyright violations, trademark infringement, or IP theft",
    "CodeVulnerability": "Security flaws like XSS, SQL injection, or insecure code",
    "UngroundedAttributes": "False, unverifiable, or fabricated claims about entities",
}

# Attack strategy descriptions
ATTACK_STRATEGY_DESCRIPTIONS = {
    "Baseline": "Direct harmful prompts without obfuscation (baseline measure)",
    "Flip": "Reverses text to bypass content filters",
    "Morse": "Encodes prompts in Morse code to evade detection",
    "Caesar": "Uses Caesar cipher encoding to disguise harmful content",
    "Rot13": "Applies ROT13 substitution cipher to text",
    "Unicode": "Uses Unicode character substitutions to bypass filters",
    "Leetspeak": "Replaces letters with numbers/symbols (e.g., 3 for E)",
    "Base64": "Encodes prompts in Base64 format",
    "Binary": "Converts text to binary representation",
    "Compose": "Combines multiple strategies for complex attack chains",
    "CRESCENDO": "Multi-turn conversation escalation attack (advanced)",
    "PAIR": "Prompt Automatic Iterative Refinement attack",
    "TAP": "Tree of Attack with Pruning technique",
    "Tense": "Changes verb tenses to evade filters",
    "Jailbreak": "Uses known jailbreak prompt patterns",
    "Multilingual": "Exploits language translation to bypass filters",
}


def display_attack_strategies():
    """
    Display all available risk categories and attack strategies with descriptions.
    
    This function shows:
    1. Risk Categories - Types of harmful content to test against
    2. Attack Strategies - Techniques used to probe AI safety guardrails
    """
    # Display Risk Categories
    print("\n" + "=" * 100)
    print("🎯 Risk Categories & Attack Strategies Reference")
    print("=" * 100)
    
    print("\n📋 RISK CATEGORIES")
    print("-" * 100)
    print(f"{'Category':<25} | {'Description':<70}")
    print("-" * 100)
    
    categories = [attr for attr in dir(RiskCategory) if not attr.startswith("_")]
    for category in categories:
        desc = RISK_CATEGORY_DESCRIPTIONS.get(category, "Tests for this risk type")
        print(f"{category:<25} | {desc:<70}")
    
    print("-" * 100)
    print(f"Total Risk Categories: {len(categories)}")
    
    # Display Attack Strategies
    print("\n⚔️  ATTACK STRATEGIES")
    print("-" * 100)
    print(f"{'Strategy':<25} | {'Complexity':<12} | {'Description':<55}")
    print("-" * 100)
    
    # Define complexity levels for known strategies
    complexity_map = {
        "Baseline": "Baseline",
        "Flip": "Easy",
        "Morse": "Easy",
        "Caesar": "Easy",
        "Rot13": "Easy",
        "Unicode": "Easy",
        "Leetspeak": "Easy",
        "Base64": "Easy",
        "Binary": "Easy",
        "Compose": "Moderate",
        "Tense": "Moderate",
        "Multilingual": "Moderate",
        "CRESCENDO": "Difficult",
        "PAIR": "Difficult",
        "TAP": "Difficult",
        "Jailbreak": "Difficult",
    }
    
    strategies = [attr for attr in dir(AttackStrategy) if not attr.startswith("_")]
    
    for strategy in strategies:
        complexity = complexity_map.get(strategy, "Varies")
        desc = ATTACK_STRATEGY_DESCRIPTIONS.get(strategy, "Custom attack technique")
        # Truncate description if too long
        if len(desc) > 55:
            desc = desc[:52] + "..."
        print(f"{strategy:<25} | {complexity:<12} | {desc:<55}")
    
    print("-" * 100)
    print(f"\nTotal Strategies: {len(strategies)}")
    print("\n💡 Tips:")
    print("   • Use AttackStrategy.Compose([s1, s2]) to combine multiple strategies")
    print("   • Baseline attacks test direct harmful prompts without obfuscation")
    print("   • Higher complexity attacks are more sophisticated but slower")
    print("=" * 100)
