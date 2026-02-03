# Azure AI Red Team Evaluation

A Python toolkit for running red team security evaluations against AI systems using the Azure AI Evaluation SDK.

## Overview

This project provides examples for testing AI systems against adversarial attacks to identify potential vulnerabilities. Red teaming helps ensure your AI applications are robust against attempts to elicit harmful, biased, or inappropriate content.

## Features

- **Basic Red Team Scan**: Quick evaluation using callback functions as targets
- **Intermediary Red Team Scan**: Advanced evaluation using Azure OpenAI model configurations
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

2. **Run the evaluation tool**:
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

   [3] Display Attack Strategies
       - List all available attack strategies

   [0] Exit
   ```

## Output

Scan results are saved to the `outputs/` directory with timestamped filenames:
- `outputs/basic_scan_YYYYMMDD_HHMMSS.json/`
- `outputs/intermediary_scan_YYYYMMDD_HHMMSS.json/`

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
├── .env                 # Environment variables (not tracked)
├── .gitignore           # Git ignore rules
├── .venv/               # Python virtual environment
├── Archive/             # Previous script versions
├── outputs/             # Scan results directory
├── runbook-v2.py        # Main evaluation script
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Notes

- Ensure the AI Foundry project MSI has `Storage Blob Data Owner` role on the associated storage account for uploading results
- Some risk categories are only available in cloud red teaming scenarios
- The SDK uses internal modules that may change in future versions

## Resources

- [Azure AI Evaluation Documentation](https://learn.microsoft.com/azure/ai-services/)
- [Red Teaming Best Practices](https://learn.microsoft.com/azure/ai-services/openai/concepts/red-teaming)
