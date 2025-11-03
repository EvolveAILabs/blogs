#!/usr/bin/env python3
"""
Demonstration script for the Australian Executive Search Research Analyst Claude Skill.

This script shows how to:
1. Load a Position Description from a file
2. Invoke the au-executive-search Claude Skill
3. Parse and display the structured JSON output
4. Save the results to a file

Usage:
    python demo.py --pd-file example_pd.txt --output results.json
    python demo.py --pd-file example_pd.txt --output results.json --api-key YOUR_API_KEY
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import anthropic
except ImportError:
    print("Error: anthropic package not installed.")
    print("Install it with: pip install anthropic")
    sys.exit(1)


class ExecutiveSearchAnalyzer:
    """
    Wrapper class for the Australian Executive Search Research Analyst skill.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the analyzer with Claude API credentials.

        Args:
            api_key: Anthropic API key. If not provided, reads from ANTHROPIC_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.skill_name = "au-executive-search"

    def analyze_position_description(
        self,
        pd_text: str,
        model: str = "claude-sonnet-4-5-20250929"
    ) -> Dict[str, Any]:
        """
        Analyze a position description using the au-executive-search skill.

        Args:
            pd_text: The full text of the Position Description
            model: Claude model to use (default: claude-sonnet-4-5-20250929)

        Returns:
            Dictionary containing the structured research output

        Raises:
            ValueError: If the response cannot be parsed as JSON
            anthropic.APIError: If the API call fails
        """
        # Construct the prompt that invokes the skill
        prompt = f"Please analyze this Position Description using the au-executive-search skill:\n\n{pd_text}"

        try:
            # Call Claude API with the skill invocation
            response = self.client.messages.create(
                model=model,
                max_tokens=16000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract the response text
            response_text = response.content[0].text

            # Parse the JSON response
            try:
                result = json.loads(response_text)
                return result
            except json.JSONDecodeError as e:
                # Try to extract JSON from the response if it's wrapped in markdown
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    json_text = response_text[json_start:json_end].strip()
                    result = json.loads(json_text)
                    return result
                else:
                    raise ValueError(f"Could not parse JSON response: {e}\n\nResponse: {response_text[:500]}...")

        except anthropic.APIError as e:
            print(f"API Error: {e}")
            raise

    def save_results(self, results: Dict[str, Any], output_file: Path) -> None:
        """
        Save analysis results to a JSON file.

        Args:
            results: The analysis results dictionary
            output_file: Path to save the JSON output
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"✓ Results saved to: {output_file}")

    def print_summary(self, results: Dict[str, Any]) -> None:
        """
        Print a human-readable summary of the analysis results.

        Args:
            results: The analysis results dictionary
        """
        print("\n" + "="*80)
        print("AUSTRALIAN EXECUTIVE SEARCH RESEARCH ANALYSIS")
        print("="*80)

        # Hiring Organization
        hiring_org = results.get("hiring_org", {})
        print(f"\n📊 HIRING ORGANIZATION: {hiring_org.get('name', 'N/A')}")
        print(f"   ABN: {hiring_org.get('abn', 'N/A')}")
        print(f"   HQ: {hiring_org.get('hq_city', 'N/A')}")
        print(f"   Ownership: {hiring_org.get('ownership', 'N/A')}")
        print(f"   Primary Sectors: {', '.join(hiring_org.get('primary_sectors', []))}")

        # Role Context
        role_context = results.get("role_context", {})
        print(f"\n💼 ROLE: {role_context.get('title_from_pd', 'N/A')}")
        print(f"   Locations: {', '.join(role_context.get('locations_from_pd', []))}")

        # Sectors Analysis
        sectors = results.get("sectors", [])
        print(f"\n🎯 IDENTIFIED SECTORS: {len(sectors)}")
        for i, sector in enumerate(sectors, 1):
            print(f"\n   {i}. {sector.get('sector_name', 'N/A')}")
            print(f"      Rationale: {sector.get('rationale', 'N/A')[:100]}...")

            companies = sector.get("top_companies_by_revenue", [])
            print(f"      Top Companies ({len(companies)}):")
            for company in companies:
                revenue = company.get("revenue", {})
                print(f"         • {company.get('company_name', 'N/A')} - "
                      f"${revenue.get('amount_aud', 0):,.0f} AUD ({revenue.get('fiscal_year', 'N/A')})")

        # Strategic Insights
        insights = results.get("sector_insights", [])
        print(f"\n💡 STRATEGIC INSIGHTS: {len(insights)}")

        talent_mobility = [i for i in insights if i.get("insight_category") == "talent_mobility"]
        print(f"\n   Talent Mobility Patterns ({len(talent_mobility)}):")
        for insight in talent_mobility:
            print(f"      • {insight.get('insight_title', 'N/A')} [{insight.get('confidence', 'N/A').upper()}]")
            print(f"        {insight.get('detailed_analysis', 'N/A')[:150]}...")

        competitive = [i for i in insights if i.get("insight_category") == "competitive_positioning"]
        print(f"\n   Competitive Positioning ({len(competitive)}):")
        for insight in competitive:
            print(f"      • {insight.get('insight_title', 'N/A')} [{insight.get('confidence', 'N/A').upper()}]")
            print(f"        {insight.get('detailed_analysis', 'N/A')[:150]}...")

        # Overall Confidence
        print(f"\n📈 OVERALL CONFIDENCE: {results.get('confidence', 'N/A').upper()}")
        print(f"📅 GENERATED: {results.get('generated_at', 'N/A')}")

        # Limitations
        limitations = results.get("assumptions_and_limitations", [])
        if limitations:
            print(f"\n⚠️  ASSUMPTIONS & LIMITATIONS ({len(limitations)}):")
            for limitation in limitations[:3]:  # Show first 3
                print(f"      • {limitation}")
            if len(limitations) > 3:
                print(f"      ... and {len(limitations) - 3} more")

        print("\n" + "="*80 + "\n")


def main():
    """
    Main function to demonstrate the au-executive-search skill.
    """
    parser = argparse.ArgumentParser(
        description="Analyze Position Descriptions using Claude's AU Executive Search skill"
    )
    parser.add_argument(
        "--pd-file",
        type=Path,
        required=True,
        help="Path to Position Description text file"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("search_results.json"),
        help="Path to save JSON results (default: search_results.json)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="claude-sonnet-4-5-20250929",
        help="Claude model to use (default: claude-sonnet-4-5-20250929)"
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Only print summary, don't save to file"
    )

    args = parser.parse_args()

    # Validate input file
    if not args.pd_file.exists():
        print(f"Error: Position Description file not found: {args.pd_file}")
        sys.exit(1)

    # Read the Position Description
    print(f"📖 Reading Position Description from: {args.pd_file}")
    with open(args.pd_file, 'r', encoding='utf-8') as f:
        pd_text = f.read()

    print(f"   Length: {len(pd_text)} characters")

    # Initialize the analyzer
    try:
        analyzer = ExecutiveSearchAnalyzer(api_key=args.api_key)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Run the analysis
    print(f"\n🔍 Analyzing with Claude ({args.model})...")
    print("   This may take 1-2 minutes as the skill performs web research...\n")

    try:
        results = analyzer.analyze_position_description(pd_text, model=args.model)

        # Print summary
        analyzer.print_summary(results)

        # Save results unless summary-only
        if not args.summary_only:
            analyzer.save_results(results, args.output)
            print(f"\n✓ Full analysis saved to: {args.output}")

        print("\n✅ Analysis complete!")

    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
