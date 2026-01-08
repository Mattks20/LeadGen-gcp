<<<<<<< HEAD
# PROJECT_NAME

> REPLACE: Update PROJECT_NAME and PROJECT_DESCRIPTION throughout this file

PROJECT_DESCRIPTION

## After Copying This Template

- [ ] Find/replace `PROJECT_NAME` with your project name
- [ ] Update `PROJECT_DESCRIPTION` in README.md and pyproject.toml
- [ ] Copy `.env.example` to `.env` and configure your values
- [ ] Run `.\scripts\install-dev.ps1`
- [ ] Run `.\scripts\test.ps1` to verify setup
- [ ] Delete example code in `ks_kb/api/routes_api.py`
- [ ] Start building!

## Quick Start

### 1. Install Dependencies

```powershell
.\scripts\install-dev.ps1
```

### 2. Configure Environment

```powershell
# Copy the example environment file
cp .env.example .env

# Edit .env with your values
notepad .env
```

### 3. Run the Application

```powershell
# Run in development mode with auto-reload
.\scripts\run.ps1 -Reload

# Or run on a custom port
.\scripts\run.ps1 -Port 3000 -Reload
```

### 4. Visit Your Application

Open your browser to [http://localhost:8000](http://localhost:8000)

## Development

### Running Tests

```powershell
# Run all tests
.\scripts\test.ps1

# Run with verbose output
.\scripts\test.ps1 -Verbose
```

### Code Quality

```powershell
# Check code quality
.\scripts\lint.ps1

# Auto-fix issues
.\scripts\lint.ps1 -Fix

# Format code
.\scripts\format.ps1

# Run all pre-commit checks
.\scripts\check.ps1
```

### Available Scripts

Run `.\scripts\help.ps1` to see all available commands and usage examples.

## Project Structure

```
.
├── docs/                   # Documentation and architectural guides
│   ├── 00_problem_brief.md     # Project context and requirements
│   ├── 01_requirements.md      # Detailed specifications
│   ├── 02_workflow.md          # Operational workflows
│   ├── 03_data_model.md        # Data contracts
│   ├── 04_integrations.md      # External service integrations
│   └── 99_ai_instructions.md   # AI coding guidelines
├── scripts/                # Development and operational scripts
├── ks_kb/                    # Source code
│   ├── api/                    # HTTP routes and endpoints
│   ├── domain/                 # Pure business logic
│   ├── integrations/           # External service clients
│   ├── models/                 # Data schemas (Pydantic)
│   ├── static/                 # CSS and static assets
│   ├── templates/              # HTML templates
│   ├── utils/                  # Cross-cutting concerns
│   ├── webapp/                 # Application entry point
│   └── workflows/              # Orchestration logic
└── tests/                  # Test suite
```

## Architecture

This project follows a layered architecture:

- **API Layer** (ks_kb/api/`): HTTP routes and request/response handling
- **Workflow Layer** (`ks_kb/workflows/`): Orchestration and business processes
- **Domain Layer** (`ks_kb/domain/`): Pure business logic (no I/O)
- **Model Layer** (`ks_kb/models/`): Data contracts and validation
- **Integration Layer** (`ks_kb/integrations/`): External service communication

See [`docs/99_ai_instructions.md`](docs/99_ai_instructions.md) for detailed architectural guidelines.

## Contributing

Before committing:

1. Run `.\scripts\check.ps1` to ensure all tests pass and code meets quality standards
2. Update documentation if you've changed functionality
3. Add tests for new features

## License

REPLACE: Add your license information here
=======
# Project Lumina: Modular AI Lead Generation Engine

A cost-effective, automated lead discovery pipeline that uses multi-model consensus scoring and hot-swappable configuration to adapt to different industries and client needs.

## Vision

Project Lumina enables you to pivot your lead generation strategy by simply changing a JSON configuration file. No code changes required to target different industries, pain points, or ideal customer profiles.

## Features

- **Hot-Swappable Configuration**: Change `config/icp_current.json` to target any industry
- **Multi-Model Consensus**: Leads are scored by both Claude and a secondary AI model
- **Google Sheets Integration**: Use Sheets as your UI and database
- **Cost-Optimized**: Uses the right AI model for each task to minimize costs
- **Async Architecture**: Built on Python async/await for performance

## Architecture

```
/config/
  icp_current.json          # ICP targeting parameters (the modular brain)

/core/
  discovery.py              # AI-powered lead discovery
  scoring.py                # Multi-model consensus scoring
  workspace.py              # Google Sheets integration

/credentials/
  service-account.json      # Google Service Account (GITIGNORED)

/plans/
  implementation.md         # Implementation roadmap
```

## Quick Start

### 1. Prerequisites

- Python 3.10+
- Google Cloud Project with Sheets API enabled
- Service Account with Sheets access
- API keys for Anthropic, OpenAI, and/or Google AI

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd LeadGen

# Install dependencies
pip install -r requirements.txt
```

### 3. Google Sheets Setup

#### Create a Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable the **Google Sheets API**
4. Navigate to **IAM & Admin > Service Accounts**
5. Create a new service account
6. Create a JSON key for the service account
7. Download the JSON file

#### Save Credentials

```bash
# Create credentials folder
mkdir credentials

# Save your service account JSON
# Place the downloaded JSON file at: credentials/service-account.json
```

#### Create and Share Google Sheet

1. Create a new Google Sheet
2. Share it with your service account email (found in the JSON file)
3. Give the service account **Editor** permissions
4. Copy the spreadsheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
   ```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
# Google Sheets
GOOGLE_SHEET_ID=your_spreadsheet_id_here

# AI Model API Keys
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
GOOGLE_AI_API_KEY=your_google_ai_key_here
```

### 5. Test the Connection

```bash
# Test Google Sheets authentication
python -m core.workspace --test
```

If successful, you should see:
```
✓ Google Sheets connection successful!
✓ Sheet structure created successfully!
```

This will also create the standard sheet structure:
- **Leads** tab: For storing discovered leads
- **Logs** tab: For execution history and errors

## Configuration

### ICP Configuration File

Edit [`config/icp_current.json`](config/icp_current.json) to define your ideal customer profile:

```json
{
  "industry": "B2B SaaS",
  "company_size": "10-500 employees",
  "pain_points": [
    "Manual lead qualification processes",
    "High cost of traditional sales prospecting"
  ],
  "decision_makers": [
    "VP of Sales",
    "Chief Revenue Officer"
  ],
  "geographic_focus": [
    "United States",
    "Canada"
  ],
  "tech_stack": [
    "Salesforce",
    "HubSpot"
  ],
  "buying_signals": [
    "Recently hired sales leaders",
    "Raised Series A/B funding"
  ]
}
```

**To switch industries**: Simply edit this file. No code changes needed.

## Usage

### Lead Discovery

```bash
# Run the discovery pipeline
python -m core.discovery
```

### Lead Scoring

```bash
# Score existing leads with consensus
python -m core.scoring
```

## Development Rules

See [`.claude.md`](.claude.md) for detailed development guidelines including:

- Modularity principles
- Multi-model consensus scoring rules
- Error handling requirements
- Cost optimization strategies
- Code organization standards

## Roadmap

- [x] Project setup and authentication
- [ ] Gemini-powered lead discovery
- [ ] Claude consensus scoring
- [ ] Secondary model integration (GPT-4o/Gemini)
- [ ] Batch operations for Sheets
- [ ] Error logging and monitoring
- [ ] Rate limiting and retry logic
- [ ] End-to-end integration tests

## Cost Optimization

Project Lumina uses a tiered AI model approach:

1. **Discovery**: Gemini 2.0 Flash (cheapest)
2. **Primary Scoring**: Claude 3.5 Sonnet (balanced)
3. **Secondary Scoring**: GPT-4o or Gemini 2.0
4. **Edge Cases**: Claude Opus (most capable)

## Security

- **Never commit credentials** to version control
- Service account JSON is gitignored
- Use environment variables for API keys
- Follow principle of least privilege for service account

## Troubleshooting

### Connection Failed

If `python -m core.workspace --test` fails:

1. Verify `credentials/service-account.json` exists
2. Check that `GOOGLE_SHEET_ID` is set in `.env`
3. Ensure service account email has Editor access to the sheet
4. Confirm Google Sheets API is enabled in your GCP project

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## Contributing

This is Project Lumina's foundation. Future modules:
- Discovery engine (`core/discovery.py`)
- Scoring engine (`core/scoring.py`)
- Model integrations
- Cloud deployment configurations

## License

Proprietary - Project Lumina Team

## Support

For issues or questions, refer to the implementation plan in [`plans/implementation.md`](plans/implementation.md).
>>>>>>> 0a6f8cc902cefbe07b5028bbc460361dfc614a13
