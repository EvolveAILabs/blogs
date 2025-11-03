# Quick Start Guide

Get up and running with the Australian Executive Search Research Analyst skill in 5 minutes.

## Step 1: Install Dependencies

```bash
pip install anthropic
```

## Step 2: Set Your API Key

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Or on Windows:
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

## Step 3: Run the Example

```bash
cd .claude/skills/au-executive-search
python demo.py --pd-file example_pd.txt --output results.json
```

This will:
- Read the example Position Description (CFO at a renewable energy company)
- Analyze it using the skill
- Print a summary to your terminal
- Save full JSON results to `results.json`

## Step 4: View Your Results

```bash
# View the summary in terminal (already printed)

# Or view the full JSON output
cat results.json | python -m json.tool | less

# Or open in your editor
code results.json  # VS Code
```

## What You'll Get

The analysis includes:

1. **Hiring Organization Details**
   - Company name, ABN, ownership, HQ
   - Recent news and primary sectors

2. **Target Sectors** (3-6 sectors)
   - Where to find qualified candidates
   - Rationale for each sector

3. **Top 3 Companies per Sector**
   - Ranked by revenue with citations
   - Latest news for each company
   - Current equivalent roles (e.g., current CFOs)

4. **Strategic Insights** (exactly 4)
   - 2 on talent mobility patterns
   - 2 on competitive positioning
   - Each with confidence scores and evidence

## Next Steps

### Use Your Own Position Description

```bash
# Create your PD file
echo "Your position description here..." > my_pd.txt

# Analyze it
python demo.py --pd-file my_pd.txt --output my_results.json
```

### Integrate with Your Code

```python
from demo import ExecutiveSearchAnalyzer

analyzer = ExecutiveSearchAnalyzer()
results = analyzer.analyze_position_description(your_pd_text)

# Access the data
hiring_org = results["hiring_org"]["name"]
sectors = [s["sector_name"] for s in results["sectors"]]
insights = results["sector_insights"]
```

### Use in Claude Code

```bash
# In Claude Code CLI
claude

# Then chat with Claude:
> Use the au-executive-search skill to analyze this PD:
> [paste your Position Description]
```

## Common Options

```bash
# Show summary only (don't save file)
python demo.py --pd-file example_pd.txt --summary-only

# Use a specific model
python demo.py --pd-file example_pd.txt --model claude-opus-4-20250514

# Specify custom output location
python demo.py --pd-file example_pd.txt --output ~/Documents/search_results.json
```

## Troubleshooting

**"No API key provided"**
- Make sure you set `ANTHROPIC_API_KEY` environment variable

**"ModuleNotFoundError: No module named 'anthropic'"**
- Run `pip install anthropic`

**Takes too long**
- This is normal! The skill performs web research which can take 1-2 minutes
- For faster results, use `--model claude-sonnet-4-5-20250929` (default)

## Example Output Structure

```json
{
  "hiring_org": {
    "name": "Sustainable Energy Solutions Australia Pty Ltd",
    "abn": "...",
    "ownership": "private",
    "summary": "..."
  },
  "sectors": [
    {
      "sector_name": "Renewable Energy",
      "top_companies_by_revenue": [
        {
          "rank": 1,
          "company_name": "AGL Energy Limited",
          "revenue": {
            "amount_aud": 12500000000.00,
            "fiscal_year": "FY2024",
            "source_url": "https://..."
          }
        }
      ]
    }
  ],
  "sector_insights": [...],
  "confidence": "high"
}
```

## Need Help?

- Read the full [README.md](README.md) for detailed documentation
- Check the [skill.md](skill.md) for the prompt configuration
- Review [example_pd.txt](example_pd.txt) for PD formatting tips

---

**Ready to analyze your Position Descriptions!** 🚀
