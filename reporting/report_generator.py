import matplotlib.pyplot as plt
from datetime import datetime
import os
import json
import subprocess
import sys

def generate_pdf_report(html_path, pdf_path):
    """Generate PDF from HTML report using wkhtmltopdf or alternative"""
    try:
        # Try using PyPDF or wkhtmltopdf
        import pdfkit
    
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'enable-local-file-access': None
        }
        pdfkit.from_file(html_path, pdf_path, options=options)
        print(f"PDF report generated: {pdf_path}")
        return True
    except ImportError:
        try:
            # Fallback: Try using subprocess with wkhtmltopdf
            subprocess.run(['wkhtmltopdf', html_path, pdf_path], check=True, capture_output=True)
            print(f"PDF report generated: {pdf_path}")
            return True
        except:
            print("Note: PDF generation requires pdfkit or wkhtmltopdf. Install with: pip install pdfkit")
            print("       For wkhtmltopdf, visit: https://wkhtmltopdf.org/")
            return False
    except Exception as e:
        print(f"PDF generation failed: {e}")
        return False

def calculate_metrics(results):
    """Calculate comprehensive test metrics"""
    total_tests = len(results)
    passed = sum(1 for r in results if r[1] == "PASSED")
    failed = sum(1 for r in results if r[1] == "FAILED")
    skipped = sum(1 for r in results if r[1] == "SKIPPED")
    
    success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
    failure_rate = (failed / total_tests * 100) if total_tests > 0 else 0
    
    return {
        'total': total_tests,
        'passed': passed,
        'failed': failed,
        'skipped': skipped,
        'success_rate': success_rate,
        'failure_rate': failure_rate
    }

def categorize_tests(results):
    """Categorize tests by suite"""
    categories = {
        'Data Quality': [],
        'ETL': [],
        'AML': [],
        'Edge Cases': [],
        'AI Generated': []
    }
    
    for test, status, details, explanation in results:
        test_lower = test.lower()
        if 'data quality' in test_lower or 'negative' in test_lower or 'transaction' in test_lower:
            categories['Data Quality'].append((test, status, details, explanation))
        elif 'etl' in test_lower or 'source' in test_lower or 'target' in test_lower:
            categories['ETL'].append((test, status, details, explanation))
        elif 'aml' in test_lower or 'fraud' in test_lower or 'suspicious' in test_lower or 'risk' in test_lower:
            categories['AML'].append((test, status, details, explanation))
        elif 'edge' in test_lower or 'orphan' in test_lower or 'zero' in test_lower or 'balance' in test_lower:
            categories['Edge Cases'].append((test, status, details, explanation))
        elif 'ai' in test_lower or 'generated' in test_lower:
            categories['AI Generated'].append((test, status, details, explanation))
    
    return {k: v for k, v in categories.items() if v}

def generate_charts(results, results_dir):
    """Generate professional charts for the report"""
    metrics = calculate_metrics(results)
    
    # Chart 1: Overall Test Results Pie Chart
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Pie chart
    labels = ['Passed', 'Failed', 'Skipped']
    sizes = [metrics['passed'], metrics['failed'], metrics['skipped']]
    colors = ['#4CAF50', '#FF6B6B', '#FFC107']
    explode = (0.05, 0.05, 0)
    
    axes[0].pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90, textprops={'fontsize': 11, 'weight': 'bold'})
    axes[0].set_title('Overall Test Results', fontsize=14, weight='bold', pad=20)
    
    # Bar chart
    test_categories = categorize_tests(results)
    cat_names = list(test_categories.keys())
    cat_passed = [sum(1 for t in test_categories[cat] if t[1] == 'PASSED') for cat in cat_names]
    cat_failed = [sum(1 for t in test_categories[cat] if t[1] == 'FAILED') for cat in cat_names]
    
    x = range(len(cat_names))
    width = 0.35
    
    axes[1].bar([i - width/2 for i in x], cat_passed, width, label='Passed', color='#4CAF50')
    axes[1].bar([i + width/2 for i in x], cat_failed, width, label='Failed', color='#FF6B6B')
    axes[1].set_ylabel('Number of Tests', fontsize=11, weight='bold')
    axes[1].set_title('Test Results by Category', fontsize=14, weight='bold', pad=20)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(cat_names, rotation=45, ha='right')
    axes[1].legend()
    axes[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    chart_path = os.path.join(results_dir, "test_summary_charts.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return chart_path

def generate_report(results, execution_time=None):
    """Generate professional stakeholder-ready HTML report"""
    
    # Base project directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(base_dir, "Results")
    os.makedirs(results_dir, exist_ok=True)
    
    # Track current time
    report_start_time = datetime.now()
    
    # Calculate metrics and categorize tests
    metrics = calculate_metrics(results)
    test_categories = categorize_tests(results)
    
    # Calculate execution metrics
    if metrics['total'] > 0:
        tests_per_second = metrics['total'] / max(1, execution_time) if execution_time else 0
    else:
        tests_per_second = 0
    
    print("Generating Professional Test Report...")
    print(f"Total Tests: {metrics['total']} | Passed: {metrics['passed']} | Failed: {metrics['failed']}")
    print(f"Success Rate: {metrics['success_rate']:.1f}%")
    if execution_time:
        print(f"Execution Time: {execution_time:.2f}s | Performance: {tests_per_second:.2f} tests/sec")
    
    # Generate charts
    chart_path = generate_charts(results, results_dir)
    print("Charts saved at:", chart_path)
    
    # Determine risk level
    if metrics['success_rate'] >= 95:
        risk_level = "LOW"
        risk_color = "#4CAF50"
        risk_bg = "#E8F5E9"
    elif metrics['success_rate'] >= 80:
        risk_level = "MEDIUM"
        risk_color = "#FFC107"
        risk_bg = "#FFF8E1"
    else:
        risk_level = "HIGH"
        risk_color = "#FF6B6B"
        risk_bg = "#FFEBEE"
    
    # Generate HTML Report
    report_path = os.path.join(results_dir, "db_test_report.html")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Database Testing - Executive Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        .header {{
            background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.8em;
            margin-bottom: 10px;
            letter-spacing: 1.5px;
            font-weight: 600;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .metadata {{
            background: #f9f9f9;
            padding: 20px 40px;
            border-bottom: 2px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 20px;
        }}
        
        .metadata-item {{
            flex: 1;
            min-width: 200px;
        }}
        
        .metadata-label {{
            font-size: 0.9em;
            color: #666;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .metadata-value {{
            font-size: 1.3em;
            color: #1a237e;
            font-weight: bold;
            margin-top: 5px;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .executive-summary {{
            background: linear-gradient(135deg, #f5f5f5 0%, #eeeeee 100%);
            padding: 30px;
            border-left: 5px solid #1a237e;
            margin-bottom: 40px;
            border-radius: 4px;
        }}
        
        .executive-summary h2 {{
            color: #1a237e;
            margin-bottom: 15px;
            font-size: 1.5em;
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .metric-box {{
            background: white;
            padding: 20px;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
            border-top: 4px solid #1a237e;
        }}
        
        .metric-box.success {{
            border-top-color: #4CAF50;
        }}
        
        .metric-box.danger {{
            border-top-color: #FF6B6B;
        }}
        
        .metric-box.warning {{
            border-top-color: #FFC107;
        }}
        
        .metric-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #1a237e;
            margin: 10px 0;
        }}
        
        .metric-label {{
            font-size: 0.95em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .metric-percentage {{
            font-size: 1.8em;
            font-weight: bold;
            margin-top: 5px;
        }}
        
        .success {{ color: #4CAF50; }}
        .danger {{ color: #FF6B6B; }}
        .warning {{ color: #FFC107; }}
        
        .risk-assessment {{
            padding: 25px;
            margin-bottom: 40px;
            border-radius: 6px;
            border-left: 5px solid;
        }}
        
        .risk-assessment h3 {{
            margin-bottom: 10px;
            font-size: 1.2em;
        }}
        
        .risk-assessment p {{
            font-size: 0.95em;
        }}
        
        .charts-section {{
            margin-bottom: 40px;
        }}
        
        .charts-section h2 {{
            color: #1a237e;
            margin-bottom: 25px;
            font-size: 1.5em;
            border-bottom: 3px solid #1a237e;
            padding-bottom: 10px;
        }}
        
        .chart-image {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .category-section {{
            margin-bottom: 35px;
        }}
        
        .category-title {{
            background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 4px;
            margin-bottom: 15px;
            font-size: 1.2em;
            font-weight: bold;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        th {{
            background-color: #f5f5f5;
            color: #1a237e;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            border-bottom: 3px solid #1a237e;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        tr:hover {{
            background-color: #f9f9f9;
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        .status-pass {{
            color: white;
            background-color: #4CAF50;
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: bold;
            display: inline-block;
            text-transform: uppercase;
            font-size: 0.85em;
        }}
        
        .status-fail {{
            color: white;
            background-color: #FF6B6B;
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: bold;
            display: inline-block;
            text-transform: uppercase;
            font-size: 0.85em;
        }}
        
        .status-skip {{
            color: white;
            background-color: #FFC107;
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: bold;
            display: inline-block;
            text-transform: uppercase;
            font-size: 0.85em;
        }}
        
        .details-column {{
            font-size: 0.9em;
            color: #666;
            max-width: 400px;
        }}
        
        .recommendations {{
            background: #E3F2FD;
            padding: 25px;
            border-left: 5px solid #2196F3;
            margin-bottom: 30px;
            border-radius: 4px;
        }}
        
        .recommendations h3 {{
            color: #1565C0;
            margin-bottom: 15px;
            font-size: 1.2em;
        }}
        
        .recommendations ul {{
            margin-left: 20px;
        }}
        
        .recommendations li {{
            margin-bottom: 10px;
            font-size: 0.95em;
            line-height: 1.6;
        }}
        
        .footer {{
            background: #f5f5f5;
            padding: 30px 40px;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        
        .footer-divider {{
            border-top: 1px solid #ddd;
            margin: 15px 0;
            padding-top: 15px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            margin-right: 5px;
        }}
        
        .badge-passed {{
            background: #E8F5E9;
            color: #2E7D32;
        }}
        
        .badge-failed {{
            background: #FFEBEE;
            color: #C62828;
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>

<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>AI Database Testing Report</h1>
            <p>Enterprise Test Management & Quality Assurance</p>
        </div>
        
        <!-- Metadata -->
        <div class="metadata">
            <div class="metadata-item">
                <div class="metadata-label">Report Date</div>
                <div class="metadata-value">{datetime.now().strftime('%B %d, %Y')}</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Report Time</div>
                <div class="metadata-value">{datetime.now().strftime('%H:%M:%S')}</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Total Tests Executed</div>
                <div class="metadata-value">{metrics['total']}</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Success Rate</div>
                <div class="metadata-value" style="color: #4CAF50;">{metrics['success_rate']:.1f}%</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Execution Time</div>
                <div class="metadata-value">{f'{execution_time:.2f}s' if execution_time else 'N/A'}</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Performance</div>
                <div class="metadata-value">{f'{tests_per_second:.2f} tests/sec' if tests_per_second else 'N/A'}</div>
            </div>
        </div>
        
        <!-- Content -->
        <div class="content">
            <!-- Executive Summary -->
            <div class="executive-summary">
                <h2>Executive Summary</h2>
                <p style="margin-bottom: 20px; font-size: 1em; line-height: 1.8;">
                    This comprehensive testing report provides an overview of all database quality assurance tests 
                    conducted across multiple test suites. The testing framework validates data integrity, ETL processes, 
                    AML compliance, and edge case handling to ensure system reliability and regulatory adherence.
                </p>
                
                <div class="summary-grid">
                    <div class="metric-box success">
                        <div class="metric-label">Tests Passed</div>
                        <div class="metric-number" style="color: #4CAF50;">{metrics['passed']}</div>
                        <div class="metric-percentage success">{(metrics['passed']/max(1, metrics['total'])*100):.1f}%</div>
                    </div>
                    <div class="metric-box {('danger' if metrics['failed'] > 0 else 'success')}">
                        <div class="metric-label">Tests Failed</div>
                        <div class="metric-number" style="color: {'#FF6B6B' if metrics['failed'] > 0 else '#4CAF50'};">{metrics['failed']}</div>
                        <div class="metric-percentage {'danger' if metrics['failed'] > 0 else 'success'}">{(metrics['failed']/max(1, metrics['total'])*100):.1f}%</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Tests Skipped</div>
                        <div class="metric-number" style="color: #FFC107;">{metrics['skipped']}</div>
                        <div class="metric-percentage warning">{(metrics['skipped']/max(1, metrics['total'])*100):.1f}%</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Overall Status</div>
                        <div class="metric-number" style="color: {risk_color}; font-size: 1.8em;">
                            <span style="background: {risk_bg}; padding: 10px 15px; border-radius: 4px;">
                                {risk_level} RISK
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Risk Assessment -->
            <div class="risk-assessment" style="background: {risk_bg}; border-color: {risk_color};">
                <h3 style="color: {risk_color};">Risk Assessment: {risk_level}</h3>
                <p>
                    Based on a {metrics['success_rate']:.1f}% success rate, the current system status is rated as <strong>{risk_level} RISK</strong>.
                    {('All critical tests are passing. The system is production-ready.' if risk_level == 'LOW' else 
                      'Review required items below before proceeding to production.' if risk_level == 'MEDIUM' else
                      'Critical issues require immediate attention before production deployment.')}
                </p>
            </div>
            
            <!-- Performance Metrics -->
            <div style="background: linear-gradient(135deg, #E3F2FD 0%, #E1F5FE 100%); padding: 30px; margin-bottom: 30px; border-radius: 6px; border-left: 5px solid #1565C0;">
                <h3 style="color: #0D47A1; margin-bottom: 20px; font-size: 1.2em;">Performance Metrics</h3>
                <div class="summary-grid">
                    <div class="metric-box" style="border-top-color: #1565C0;">
                        <div class="metric-label">Execution Time</div>
                        <div class="metric-number" style="color: #1565C0;">{f'{execution_time:.2f}s' if execution_time else 'N/A'}</div>
                        <div style="font-size: 0.9em; color: #666; margin-top: 5px;">seconds</div>
                    </div>
                    <div class="metric-box" style="border-top-color: #1565C0;">
                        <div class="metric-label">Performance</div>
                        <div class="metric-number" style="color: #1565C0;">{f'{tests_per_second:.2f}' if tests_per_second else 'N/A'}</div>
                        <div style="font-size: 0.9em; color: #666; margin-top: 5px;">tests/second</div>
                    </div>
                    <div class="metric-box" style="border-top-color: #1565C0;">
                        <div class="metric-label">Avg Test Time</div>
                        <div class="metric-number" style="color: #1565C0;">{f'{(execution_time / max(1, metrics["total"]) * 1000):.0f}ms' if execution_time else 'N/A'}</div>
                        <div style="font-size: 0.9em; color: #666; margin-top: 5px;">milliseconds</div>
                    </div>
                    <div class="metric-box" style="border-top-color: #1565C0;">
                        <div class="metric-label">Test Coverage</div>
                        <div class="metric-number" style="color: #1565C0;">{metrics['total']}</div>
                        <div style="font-size: 0.9em; color: #666; margin-top: 5px;">total tests</div>
                    </div>
                </div>
            </div>
            
            <!-- Charts Section -->
            <div class="charts-section">
                <h2>Visual Analysis</h2>
                <img src="test_summary_charts.png" alt="Test Summary Charts" class="chart-image">
            </div>
            
            <!-- Test Results by Category -->
            <h2 style="color: #1a237e; margin: 40px 0 25px; font-size: 1.5em; border-bottom: 3px solid #1a237e; padding-bottom: 10px;">
                Test Results by Category
            </h2>
""")

        # Add test results by category
        for category, tests in test_categories.items():
            if tests:
                category_passed = sum(1 for t in tests if t[1] == 'PASSED')
                category_total = len(tests)
                category_rate = (category_passed / category_total * 100) if category_total > 0 else 0
                
                f.write(f"""
            <div class="category-section">
                <div class="category-title">
                    {category}
                    <span style="float: right; font-size: 0.8em;">
                        {category_passed}/{category_total} Passed ({category_rate:.0f}%)
                    </span>
                </div>
                <table>
                    <tr>
                        <th>Test Name</th>
                        <th>Status</th>
                        <th>Details</th>
                    </tr>
""")
                
                for test, status, details, explanation in tests:
                    status_class = f"status-{status.lower()}"
                    f.write(f"""
                    <tr>
                        <td><strong>{test}</strong></td>
                        <td><span class="{status_class}">{status}</span></td>
                        <td class="details-column">{details}</td>
                    </tr>
""")
                
                f.write("""
                </table>
            </div>
""")
        
        # Recommendations
        f.write("""
            <div class="recommendations">
                <h3>Recommendations & Next Steps</h3>
                <ul>
""")
        
        if metrics['failed'] > 0:
            f.write(f"""
                    <li><strong>Critical:</strong> Address {metrics['failed']} failing test(s) immediately before production deployment.</li>
""")
        
        if metrics['success_rate'] < 95:
            f.write("""
                    <li>Conduct root cause analysis for all failed tests and implement corrective actions.</li>
                    <li>Increase test coverage to improve system reliability and confidence.</li>
""")
        else:
            f.write("""
                    <li>Maintain current testing standards and continue monitoring system performance.</li>
""")
        
        f.write(f"""
                    <li>Schedule regular regression testing to ensure ongoing data quality.</li>
                    <li>Review and update test cases based on business logic changes.</li>
                    <li>Document all test results for compliance and audit purposes.</li>
                </ul>
            </div>
            
            <!-- Footer -->
            <div class="footer">
                <p><strong>Report Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <div class="footer-divider"></div>
                <p>This report is confidential and intended for authorized stakeholders only.</p>
                <p>For questions or additional information, please contact the QA team.</p>
                <p style="margin-top: 10px; font-size: 0.85em; color: #999;">
                    AI Database Testing Framework v1.0 | Enterprise Edition
                </p>
            </div>
        </div>
    </div>
</body>
</html>
""")
    
    
    print("Professional HTML report generated at:", report_path)
    
    # Attempt to generate PDF version
    pdf_path = report_path.replace('.html', '.pdf')
    if generate_pdf_report(report_path, pdf_path):
        print(f"Professional PDF report generated at: {pdf_path}")
    
    return report_path
