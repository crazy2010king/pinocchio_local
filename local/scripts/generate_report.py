#!/usr/bin/env python3
"""
Report generation script for Pinocchio examples test runs.
Generates HTML and Markdown reports from run results.
"""

import os
import sys
import json
import glob
from datetime import datetime
from typing import List, Dict, Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "../test_results/reports")
LOGS_DIR = os.path.join(SCRIPT_DIR, "../test_results/logs")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "../test_results/reports")

def load_latest_results() -> Dict:
    """Load the latest run results file"""
    result_files = sorted(glob.glob(os.path.join(RESULTS_DIR, "run_results_*.json")), reverse=True)
    if not result_files:
        print("❌ No result files found. Run run_all_examples.sh first.")
        sys.exit(1)

    latest_file = result_files[0]
    print(f"📂 Loading latest results from: {latest_file}")

    with open(latest_file, 'r') as f:
        return {
            "file": latest_file,
            "data": json.load(f)
        }

def analyze_results(results: List[Dict]) -> Dict:
    """Analyze the results and generate statistics"""
    stats = {
        "total": len(results),
        "success": 0,
        "failed": 0,
        "timeout": 0,
        "skipped": 0,
        "by_category": {},
        "by_language": {},
        "avg_duration": 0,
        "max_duration": 0,
        "min_duration": float('inf')
    }

    total_duration = 0

    for res in results:
        status = res["status"]
        category = res["category"]
        language = res["language"]
        duration = res["duration"]

        # Update counters
        stats[status] += 1

        # Update category stats
        if category not in stats["by_category"]:
            stats["by_category"][category] = {"total": 0, "success": 0, "failed": 0, "timeout": 0, "skipped": 0}
        stats["by_category"][category]["total"] += 1
        stats["by_category"][category][status] += 1

        # Update language stats
        if language not in stats["by_language"]:
            stats["by_language"][language] = {"total": 0, "success": 0, "failed": 0, "timeout": 0, "skipped": 0}
        stats["by_language"][language]["total"] += 1
        stats["by_language"][language][status] += 1

        # Update duration stats
        if status == "success":
            total_duration += duration
            stats["max_duration"] = max(stats["max_duration"], duration)
            stats["min_duration"] = min(stats["min_duration"], duration)

    if stats["success"] > 0:
        stats["avg_duration"] = total_duration / stats["success"]

    if stats["total"] > 0:
        stats["success_rate"] = (stats["success"] / stats["total"]) * 100
    else:
        stats["success_rate"] = 0

    return stats

def generate_markdown_report(results: List[Dict], stats: Dict, timestamp: str) -> str:
    """Generate Markdown format report"""
    md = f"""# Pinocchio Examples Test Report
Generated on: {datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Summary Statistics
| Metric | Value |
|--------|-------|
| Total Examples | {stats['total']} |
| ✅ Success | {stats['success']} |
| ❌ Failed | {stats['failed']} |
| ⏱️  Timeout | {stats['timeout']} |
| ⏭️  Skipped | {stats['skipped']} |
| 📈 Success Rate | {stats['success_rate']:.1f}% |
| ⏱️  Average Duration | {stats['avg_duration']:.1f}s |
| ⏱️  Max Duration | {stats['max_duration']}s |
| ⏱️  Min Duration | {stats['min_duration']}s |

## 📈 Results by Category
"""

    for category, cat_stats in sorted(stats["by_category"].items()):
        success_rate = (cat_stats["success"] / cat_stats["total"]) * 100 if cat_stats["total"] > 0 else 0
        md += f"""
### {category.title()}
| Total | Success | Failed | Timeout | Skipped | Success Rate |
|-------|---------|--------|---------|---------|--------------|
| {cat_stats['total']} | {cat_stats['success']} | {cat_stats['failed']} | {cat_stats['timeout']} | {cat_stats['skipped']} | {success_rate:.1f}% |
"""

    md += """
## 📈 Results by Language
"""

    for language, lang_stats in sorted(stats["by_language"].items()):
        success_rate = (lang_stats["success"] / lang_stats["total"]) * 100 if lang_stats["total"] > 0 else 0
        md += f"""
### {language.upper()}
| Total | Success | Failed | Timeout | Skipped | Success Rate |
|-------|---------|--------|---------|---------|--------------|
| {lang_stats['total']} | {lang_stats['success']} | {lang_stats['failed']} | {lang_stats['timeout']} | {lang_stats['skipped']} | {success_rate:.1f}% |
"""

    md += """
## 📋 Detailed Results
| Example | Category | Language | Status | Duration | Log |
|---------|----------|----------|--------|----------|-----|
"""

    for res in sorted(results, key=lambda x: x["name"]):
        status_emoji = {
            "success": "✅",
            "failed": "❌",
            "timeout": "⏱️",
            "skipped": "⏭️"
        }.get(res["status"], "❓")

        log_link = f"[{os.path.basename(res['log_file'])}]({res['log_file']})"

        md += f"| {res['name']} | {res['category']} | {res['language']} | {status_emoji} {res['status']} | {res['duration']}s | {log_link} |\n"

    if stats["failed"] > 0 or stats["timeout"] > 0:
        md += """
## ❌ Failed Examples
"""
        for res in results:
            if res["status"] in ["failed", "timeout"]:
                md += f"\n### {res['name']}\n"
                md += f"- Status: {res['status']}\n"
                md += f"- Exit code: {res['exit_code']}\n"
                md += f"- Duration: {res['duration']}s\n"
                md += f"- Log file: {res['log_file']}\n"

                # Add last 10 lines of log
                try:
                    with open(res['log_file'], 'r') as f:
                        lines = f.readlines()[-10:]
                        md += "\n```\n" + "".join(lines) + "```\n"
                except Exception as e:
                    md += f"\nError reading log: {str(e)}\n"

    return md

def generate_html_report(md_content: str, timestamp: str) -> str:
    """Generate HTML format report from Markdown"""
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pinocchio Examples Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
        h1, h2, h3 { color: #2c3e50; }
        table { border-collapse: collapse; width: 100%; margin: 15px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; font-weight: bold; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .success { color: #27ae60; }
        .failed { color: #e74c3c; }
        .timeout { color: #f39c12; }
        .skipped { color: #95a5a6; }
        pre { background-color: #f8f8f8; padding: 15px; border-radius: 5px; overflow-x: auto; }
        .summary { background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
    </style>
</head>
<body>
    {{content}}
</body>
</html>"""

    # Convert markdown to simple HTML (basic conversion)
    import markdown
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

    return html_template.replace("{{content}}", html_content)

def main():
    print("=" * 60)
    print("Pinocchio Examples Report Generator")
    print("=" * 60)

    # Load results
    results_data = load_latest_results()
    results = results_data["data"]
    results_file = results_data["file"]

    # Extract timestamp from filename
    timestamp = os.path.basename(results_file).replace("run_results_", "").replace(".json", "")

    # Analyze results
    print("\n🔍 Analyzing results...")
    stats = analyze_results(results)

    # Generate Markdown report
    print("\n📝 Generating Markdown report...")
    md_report = generate_markdown_report(results, stats, timestamp)
    md_output_file = os.path.join(OUTPUT_DIR, f"test_report_{timestamp}.md")
    with open(md_output_file, 'w') as f:
        f.write(md_report)
    print(f"✅ Markdown report saved to: {md_output_file}")

    # Generate HTML report
    try:
        print("\n🌐 Generating HTML report...")
        html_report = generate_html_report(md_report, timestamp)
        html_output_file = os.path.join(OUTPUT_DIR, f"test_report_{timestamp}.html")
        with open(html_output_file, 'w') as f:
            f.write(html_report)
        print(f"✅ HTML report saved to: {html_output_file}")
    except ImportError:
        print("⚠️  Python markdown package not installed, skipping HTML report generation")
        print("💡 Install with: pip install markdown")

    print("\n🎉 Report generation complete!")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
