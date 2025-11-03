# Australian Executive Search Research Analyst - Claude Skill

A comprehensive Claude Skill for executive search research in Australia. This skill analyzes Position Descriptions (PDs) and produces detailed, source-backed research on hiring organizations, target sectors, top companies, and strategic insights for executive recruitment.

## Overview

This skill transforms Position Descriptions into actionable executive search intelligence by:

- **Researching the hiring organization**: Company details, ABN, ownership, sectors, and recent news
- **Identifying target sectors**: Australian industry segments where equivalent roles are found
- **Ranking top companies**: Top 3 organizations per sector by revenue with citations
- **Generating strategic insights**: Evidence-based analysis on talent mobility and competitive positioning
- **Maintaining Australia-only scope**: All data, companies, and sectors are Australian-focused

## Features

### 🎯 Precision & Source-Backed Research
- Every revenue figure includes citations from primary sources (annual reports, ASX filings)
- All company data normalized to AUD with source transparency
- Confidence scoring for every insight (HIGH/MEDIUM/LOW)

### 🇦🇺 Australia-Focused
- ANZSIC-aligned sector classifications
- Australian company entities prioritized
- Recent news and appointments from Australian sources

### 📊 Structured JSON Output
- Machine-readable format for integration with recruitment systems
- Consistent schema for automated processing
- Detailed assumptions and limitations tracking

### 💡 Strategic Intelligence
- **Talent Mobility Patterns**: Analysis of recent (18-24 months) executive movements
- **Competitive Positioning**: How organizations compete for talent based on recent evidence

## Installation

### Prerequisites

1. **Claude Code CLI** or **Anthropic API access**
2. **Python 3.8+** (for the demo script)
3. **Anthropic Python SDK**:
   ```bash
   pip install anthropic
   ```

### Skill Setup

1. **Clone or copy this skill** into your Claude Code skills directory:
   ```bash
   mkdir -p .claude/skills/
   cp -r au-executive-search .claude/skills/
   ```

2. **Verify the skill is recognized**:
   ```bash
   # Using Claude Code CLI
   claude skills list
   # You should see "au-executive-search" in the list
   ```

3. **Set your API key** (if using the demo script):
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

## Usage

### Option 1: Using Claude Code CLI

You can invoke this skill directly in conversation with Claude Code:

```bash
# Start Claude Code
claude

# Then in the conversation:
> Please use the au-executive-search skill to analyze this Position Description:
> [paste your PD here]
```

### Option 2: Using the Demo Script

The included `demo.py` script provides a convenient way to analyze PDs from files:

```bash
# Basic usage with the example PD
python demo.py --pd-file example_pd.txt --output results.json

# Using a custom API key
python demo.py --pd-file my_pd.txt --output my_results.json --api-key sk-ant-...

# Print summary only (don't save to file)
python demo.py --pd-file example_pd.txt --summary-only

# Use a specific Claude model
python demo.py --pd-file example_pd.txt --model claude-opus-4-20250514
```

### Option 3: Programmatic Usage

```python
from pathlib import Path
from demo import ExecutiveSearchAnalyzer

# Initialize
analyzer = ExecutiveSearchAnalyzer(api_key="your-api-key")

# Read PD
with open("position_description.txt", "r") as f:
    pd_text = f.read()

# Analyze
results = analyzer.analyze_position_description(pd_text)

# Access structured data
hiring_org = results["hiring_org"]["name"]
sectors = results["sectors"]
insights = results["sector_insights"]

# Print summary
analyzer.print_summary(results)

# Save results
analyzer.save_results(results, Path("output.json"))
```

## Output Structure

The skill returns a JSON object with the following structure:

```json
{
  "hiring_org": {
    "name": "Company Name",
    "abn": "12345678901",
    "hq_city": "Sydney",
    "ownership": "private",
    "primary_sectors": ["Renewable Energy", "Infrastructure"],
    "summary": "Detailed company overview...",
    "important_criteria": ["Must-have requirement 1", "..."],
    "recent_relevant_news": [...],
    "citations": ["https://..."]
  },
  "role_context": {
    "title_from_pd": "Chief Financial Officer",
    "locations_from_pd": ["Sydney", "Melbourne"],
    "sector_terms_from_pd": ["renewable energy", "infrastructure"]
  },
  "sectors": [
    {
      "sector_name": "Renewable Energy",
      "rationale": "CFO roles in this sector require...",
      "top_companies_by_revenue": [
        {
          "rank": 1,
          "company_name": "Company A",
          "revenue": {
            "amount_aud": 5000000000.00,
            "fiscal_year": "FY2024",
            "source_url": "https://...",
            "source_type": "annual_report"
          },
          "recent_relevant_news": [...]
        }
      ]
    }
  ],
  "sector_insights": [
    {
      "insight_category": "talent_mobility",
      "insight_title": "Cross-sector CFO movements accelerating",
      "detailed_analysis": "Evidence shows...",
      "alignment_to_pd_vision": "This aligns with the PD's requirement for...",
      "supporting_data_points": [...],
      "implications_for_search": "Target candidates from...",
      "confidence": "high",
      "confidence_rationale": "Based on 5 recent appointments..."
    },
    // ... 3 more insights (2 talent_mobility, 2 competitive_positioning total)
  ],
  "assumptions_and_limitations": ["..."],
  "generated_at": "2025-11-03",
  "confidence": "high"
}
```

## Example Usage

### Input: Position Description

```text
POSITION DESCRIPTION
Chief Financial Officer (CFO)

ORGANIZATION: Sustainable Energy Solutions Australia Pty Ltd
LOCATION: Sydney, NSW

[... full PD text ...]
```

### Output: Research Analysis

The skill will produce:

1. **Hiring Organization Research**
   - Company name, ABN, ownership structure
   - Primary sectors and recent news
   - Important criteria extracted from PD

2. **Sector Identification** (e.g., for CFO role)
   - Renewable Energy
   - Utilities
   - Infrastructure & Construction
   - Private Equity
   - Banking & Finance

3. **Top 3 Companies per Sector** (by revenue)
   - Complete with revenue figures, sources, and recent news
   - Latest executive appointments in equivalent roles

4. **Strategic Insights**
   - 2× Talent Mobility insights (e.g., "Energy sector CFOs increasingly moving from Big 4 banking")
   - 2× Competitive Positioning insights (e.g., "Private equity-backed renewables firms competing with ASX-listed players")

## Configuration

### Customizing the Skill

You can modify the skill behavior by editing `skill.md`:

- **Change confidence thresholds**: Adjust the HIGH/MEDIUM/LOW criteria
- **Add sector filters**: Restrict or expand the sectors considered
- **Modify output fields**: Add custom fields to the JSON schema
- **Adjust research depth**: Change the number of companies per sector

### Model Selection

The skill works best with these Claude models:

- **Claude Sonnet 4.5** (default): Best balance of speed, cost, and quality
- **Claude Opus 4**: Maximum quality for critical searches (slower, more expensive)
- **Claude Haiku 4**: Faster, lower cost for high-volume processing

## Data Quality & Validation

### Revenue Data Sources (Prioritized)

1. **Primary sources** (preferred):
   - Annual reports (investor.company.com.au)
   - ASX filings (asx.com.au)
   - Company registry (ASIC)
   - Official press releases

2. **Secondary sources** (when primary unavailable):
   - IBISWorld industry reports
   - Reputable financial media (AFR, Bloomberg)

### Validation Rules

- ✅ Every revenue figure MUST have a citation URL
- ✅ All URLs must be absolute (https://...)
- ✅ JSON must parse without errors
- ✅ Exactly 4 strategic insights (2 mobility, 2 competitive)
- ✅ All evidence from last 18-24 months

## Limitations & Assumptions

The skill will document limitations such as:

- **Data availability**: When recent revenue data isn't publicly available
- **Sector ambiguity**: When role could fit multiple interpretations
- **News recency**: When latest news is older than 6 months
- **Private companies**: When detailed financials aren't disclosed
- **Currency conversion**: When using estimated exchange rates

These are tracked in the `assumptions_and_limitations` array.

## Troubleshooting

### Common Issues

**Issue**: "No API key provided"
- **Solution**: Set `ANTHROPIC_API_KEY` environment variable or pass `--api-key` flag

**Issue**: "Could not parse JSON response"
- **Solution**: The skill might have included explanation text. The demo script will attempt to extract JSON from markdown code blocks.

**Issue**: "Timeout during web research"
- **Solution**: Increase the `max_tokens` parameter or use a faster model

**Issue**: "Few companies returned per sector"
- **Solution**: This is documented in `assumptions_and_limitations`. Some sectors may have limited Australian players.

### Getting Help

For issues with:
- **The skill itself**: Check the `skill.md` configuration
- **Claude Code**: Visit [Claude Code documentation](https://docs.claude.com)
- **API errors**: Check [Anthropic API status](https://status.anthropic.com)

## Advanced Usage

### Batch Processing

Process multiple PDs in batch:

```python
from pathlib import Path
from demo import ExecutiveSearchAnalyzer

analyzer = ExecutiveSearchAnalyzer()

pd_files = Path("./position_descriptions").glob("*.txt")
for pd_file in pd_files:
    with open(pd_file) as f:
        pd_text = f.read()

    results = analyzer.analyze_position_description(pd_text)

    output_file = Path(f"./results/{pd_file.stem}_analysis.json")
    analyzer.save_results(results, output_file)
    print(f"Processed: {pd_file.name}")
```

### Custom Filtering

Filter results for specific criteria:

```python
# Get only HIGH confidence insights
high_confidence_insights = [
    insight for insight in results["sector_insights"]
    if insight["confidence"] == "high"
]

# Get companies with revenue > $1B AUD
large_companies = []
for sector in results["sectors"]:
    for company in sector["top_companies_by_revenue"]:
        if company["revenue"]["amount_aud"] > 1_000_000_000:
            large_companies.append(company)
```

### Integration with ATS/CRM

Export for recruitment systems:

```python
import csv

# Export companies to CSV for ATS import
companies = []
for sector in results["sectors"]:
    for company in sector["top_companies_by_revenue"]:
        companies.append({
            "Company": company["company_name"],
            "Sector": sector["sector_name"],
            "Revenue_AUD": company["revenue"]["amount_aud"],
            "Source": company["revenue"]["source_url"]
        })

with open("target_companies.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=companies[0].keys())
    writer.writeheader()
    writer.writerows(companies)
```

## File Structure

```
.claude/skills/au-executive-search/
├── skill.md              # Main skill configuration
├── README.md            # This file
├── demo.py              # Demonstration script
├── example_pd.txt       # Example Position Description
└── requirements.txt     # Python dependencies (optional)
```

## Version History

- **v1.0.0** (2025-11-03): Initial release
  - Australia-focused executive search research
  - Revenue-based company rankings
  - Strategic insights on talent mobility & competitive positioning
  - Structured JSON output with confidence scoring

## License

This skill is provided as-is for use with Claude Code and the Anthropic API.

## Contributing

To improve this skill:

1. Test with various Position Descriptions
2. Document edge cases in `assumptions_and_limitations`
3. Refine sector definitions for Australian context
4. Improve revenue data source prioritization
5. Enhance insight generation logic

## Related Skills

- **Company Research**: Deep-dive research on a single organization
- **Market Mapping**: Comprehensive mapping of an entire sector
- **Candidate Profiling**: LinkedIn/public profile analysis

---

**Need help?** Open an issue or contact the skill maintainer.
