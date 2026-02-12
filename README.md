# Azure AI Red Team Evaluation

A Python toolkit for running red team security evaluations against AI systems using the Azure AI Evaluation SDK.

## Overview

This project provides examples for testing AI systems against adversarial attacks to identify potential vulnerabilities. Red teaming helps ensure your AI applications are robust against attempts to elicit harmful, biased, or inappropriate content.

**Built on Microsoft's PyRIT**: The red teaming functionality leverages [PyRIT (Python Risk Identification Tool)](https://github.com/Azure/PyRIT), Microsoft's open-source framework for AI red teaming, through the Azure AI Evaluation SDK.

## Features

- **Basic Red Team Scan**: Quick evaluation using callback functions as targets
- **Intermediary Red Team Scan**: Evaluation using Azure OpenAI model configurations
- **Advanced Red Team Scan**: Uses Azure OpenAI in a callback function for real AI application testing
- **Foundry Agent Demo (MCP)**: Creates an Azure AI Foundry Agent that uses Model Context Protocol (MCP) to search Microsoft documentation and answer user queries
- **Multiple Risk Categories**: Test against violence, hate/unfairness, sexual content, self-harm, and more
- **Attack Strategies**: Flip, Compose, and various other attack patterns

## Prerequisites

- Python 3.10+
- Azure subscription with access to Azure AI services
- Azure CLI installed and authenticated (`az login`)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd red-teaming-foundry
   ```

2. **Create and activate virtual environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root:

```env
AZURE_PROJECT_ENDPOINT=<your-azure-ai-project-endpoint>
AZURE_OPENAI_ENDPOINT=<your-azure-openai-endpoint>
AZURE_OPENAI_DEPLOYMENT_NAME=<your-deployment-name>
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

## Usage

1. **Authenticate with Azure**:
   ```bash
   az login
   ```

### Red Team Evaluation (runbook-v2.py)

2. **Run red team evaluations**:
   ```bash
   python runbook-v2.py
   ```

3. **Select an option from the menu**:
   ```
   [1] Basic Red Team Scan
       - Uses callback function as target
       - Single attack strategy (Flip)
       - Quick evaluation for testing

   [2] Intermediary Red Team Scan  
       - Uses Azure OpenAI model configuration as target
       - Tests base/foundation models directly

   [3] Advanced Red Team Scan
       - Uses Azure OpenAI model endpoint in a callback function
       - Demonstrates how to evaluate actual AI applications
       - Uses Azure AD authentication (no API key required)

   [4] Display Attack Strategies
       - List all available attack strategies

   [0] Exit
   ```

### AI Foundry Agent Demo (runbook-v3.py)

4. **Run AI Agent demo with MCP**:
   ```bash
   python runbook-v3.py
   ```

5. **Select an option from the menu**:
   ```
   [1] Interactive Demo
       - Creates Azure AI Agent with MCP tool
       - Connects to Microsoft Learn documentation
       - Interactive conversation mode

   [2] Single Query Demo
       - Run a single query against Microsoft documentation
       - Quick demonstration of MCP capabilities

   [0] Exit
   ```

## Output

Scan results are saved to the `outputs/` directory with timestamped filenames:
- `outputs/basic_scan_YYYYMMDD_HHMMSS.json/`
- `outputs/intermediary_scan_YYYYMMDD_HHMMSS.json/`
- `outputs/advanced_scan_YYYYMMDD_HHMMSS.json/`

## Key Metrics

**Attack Success Rate (ASR)**: The percentage of attacks that successfully elicit harmful content from your AI system. Lower is better.

## Risk Categories

| Category | Description |
|----------|-------------|
| Violence | Content promoting or describing violence |
| HateUnfairness | Discriminatory or biased content |
| Sexual | Inappropriate sexual content |
| SelfHarm | Content promoting self-harm |
| ProtectedMaterial | Copyright or trademark violations |
| CodeVulnerability | Security vulnerabilities in code |
| UngroundedAttributes | False or unverifiable claims |

## Project Structure

```
red-teaming-foundry/
├── .env                     # Environment variables (not tracked)
├── .gitignore               # Git ignore rules
├── .venv/                   # Python virtual environment
├── config.py                # Shared configuration and constants
├── examples/                # Individual scan examples
│   ├── __init__.py          # Package exports
│   ├── basic_scan.py        # Example 1: Callback function target
│   ├── intermediary_scan.py # Example 2: Model configuration target
│   ├── advanced_scan.py     # Example 3: Azure OpenAI callback
│   ├── foundry_agent_demo.py# AI Agent with MCP for Microsoft docs
│   └── utils.py             # Utility functions
├── outputs/                 # Scan results directory
├── Archive/                 # Previous script versions
├── runbook-v2.py            # Red Team evaluation menu
├── runbook-v3.py            # AI Foundry Agent demo menu
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Notes

- Ensure the AI Foundry project MSI has `Storage Blob Data Owner` role on the associated storage account for uploading results
- Some risk categories are only available in cloud red teaming scenarios
- The SDK uses internal modules that may change in future versions

## Underlying Technology: PyRIT

This toolkit uses the **Azure AI Evaluation SDK** (`azure-ai-evaluation[redteam]`), which is built on top of Microsoft's open-source **PyRIT (Python Risk Identification Tool for generative AI)** framework.

### What is PyRIT?

PyRIT is Microsoft's open-source framework designed to help security professionals and machine learning engineers proactively identify risks in generative AI systems. Key features include:

| Feature | Description |
|---------|-------------|
| **Attack Strategy Orchestration** | Automates adversarial prompt generation and attack chains |
| **Multi-Modal Support** | Tests text, image, and multi-modal AI systems |
| **Extensible Architecture** | Pluggable converters, scorers, and attack strategies |
| **Risk Categories** | Built-in categories for violence, hate, sexual content, self-harm, etc. |
| **Memory System** | Tracks conversation history and attack results |

### How Azure AI Evaluation Uses PyRIT

The `azure-ai-evaluation[redteam]` package wraps PyRIT with:
- **Azure AI Project integration** - Seamless connection to Azure AI services
- **Cloud-based red teaming** - Scales attacks using Azure infrastructure
- **Simplified API** - High-level `RedTeam` class abstracts PyRIT complexity
- **Built-in attack strategies** - Flip, Compose, Morse, Caesar, and more

### Attack Strategies Available

| Strategy | Description | Complexity |
|----------|-------------|------------|
| `AttackStrategy.Flip` | Character/word flipping | Easy |
| `AttackStrategy.Morse` | Morse code encoding | Easy |
| `AttackStrategy.Caesar` | Caesar cipher encoding | Easy |
| `AttackStrategy.Compose` | Combines multiple strategies | Moderate |
| `AttackStrategy.CRESCENDO` | Multi-turn escalation | Difficult |
| `AttackStrategy.Baseline` | Direct harmful prompts | Baseline |

### PyRIT vs Azure AI Evaluation

| Aspect | PyRIT (Direct) | Azure AI Evaluation SDK |
|--------|----------------|------------------------|
| Installation | `pip install pyrit` | `pip install azure-ai-evaluation[redteam]` |
| Setup | Manual configuration | Azure project endpoint |
| Scalability | Local execution | Cloud-based scaling |
| Results | Local storage | Azure Storage integration |
| Best For | Research, custom attacks | Enterprise red teaming |

This project uses the **Azure AI Evaluation SDK** approach for enterprise-grade red teaming with Azure integration.

## Resources

- [PyRIT GitHub Repository](https://github.com/Azure/PyRIT)
- [PyRIT Documentation](https://azure.github.io/PyRIT/)
- [Azure AI Evaluation Documentation](https://learn.microsoft.com/azure/ai-studio/how-to/develop/evaluate-sdk)
- [Red Teaming Best Practices](https://learn.microsoft.com/azure/ai-services/openai/concepts/red-teaming)
- [Responsible AI Practices](https://www.microsoft.com/en-us/ai/responsible-ai)
