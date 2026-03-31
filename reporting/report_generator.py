import matplotlib.pyplot as plt
from datetime import datetime
import os

def generate_report(results):

    # Base project directory
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Results directory
    results_dir = os.path.join(base_dir, "Results")

    # Create folder if it doesn't exist
    os.makedirs(results_dir, exist_ok=True)
    print("Saving reports to:", results_dir)

    # -------------------------------
    # Test Statistics
    # -------------------------------
    total_tests = len(results)
    passed = sum(1 for r in results if r[1] == "PASSED")
    failed = sum(1 for r in results if r[1] == "FAILED")

    print("Total:", total_tests)
    print("Passed:", passed)
    print("Failed:", failed)

    # -------------------------------
    # Generate Pie Chart
    # -------------------------------
    labels = ["Passed", "Failed"]
    sizes = [passed, failed]

    plt.figure()
    plt.pie(sizes, labels=labels, autopct="%1.0f%%")
    plt.title("AI Database Test Results")

    chart_path = os.path.join(results_dir, "test_summary_chart.png")
    plt.savefig(chart_path)
    plt.close()

    print("Chart saved at:", chart_path)

    # -------------------------------
    # Generate HTML Report
    # -------------------------------
    report_path = os.path.join(results_dir, "db_test_report.html")

    with open(report_path, "w", encoding="utf-8") as f:

        f.write(f"""
<html>
<head>
<title>AI Database Testing Dashboard</title>
<style>
body {{font-family:Arial; margin:40px}}
table {{border-collapse:collapse; width:100%}}
th, td {{border:1px solid #ddd; padding:8px}}
th {{background:#4CAF50; color:white}}
.pass {{color:green; font-weight:bold}}
.fail {{color:red; font-weight:bold}}
</style>
</head>

<body>

<h1>AI Database Testing Dashboard</h1>
<p>Generated: {datetime.now()}</p>

<h2>Summary</h2>
<p>Total Tests: {total_tests}</p>
<p>Passed: {passed}</p>
<p>Failed: {failed}</p>

<h2>Test Chart</h2>
<img src="test_summary_chart.png" width="400">

<h2>Test Results</h2>

<table>
<tr>
<th>Test</th>
<th>Status</th>
<th>Details</th>
</tr>
""")

        for test, status, details, explanation in results:
            color = "pass" if status == "PASSED" else "fail"

            f.write(f"""
<tr>
<td>{test}</td>
<td class="{color}">{status}</td>
<td>{details}</td>
</tr>
""")

        f.write("</table>")

        f.write("<h2>Failed Records</h2>")

        for test, status, details, explanation in results:
            if status == "FAILED":
                f.write(f"""
<h3>{test}</h3>
<pre>{details}</pre>
<p><b>AI Explanation:</b> {explanation}</p>
<hr>
""")

        f.write("</body></html>")

    print("Report saved at:", report_path)