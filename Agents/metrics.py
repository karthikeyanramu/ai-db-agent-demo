"""
Performance metrics tracking for AI Database Agent
Tracks test execution time, success rates, and performance
"""

import time
from datetime import datetime
from config.logger import setup_logger

logger = setup_logger(__name__)


class Metrics:
    """Track performance metrics for AI agent"""
    
    def __init__(self, test_name="AI Agent Test"):
        """
        Initialize metrics tracker
        
        Args:
            test_name: Name of the test/run
        """
        self.test_name = test_name
        self.start_time = None
        self.end_time = None
        self.results = {
            "test_name": test_name,
            "timestamp": datetime.now().isoformat(),
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "skipped_tests": 0,
            "execution_time": 0,
            "tests_per_second": 0,
            "success_rate": 0.0,
            "details": []
        }
    
    def start(self):
        """Start timing the test execution"""
        self.start_time = time.time()
        logger.info(f"Starting metrics tracking for: {self.test_name}")
    
    def end(self):
        """End timing and calculate metrics"""
        if self.start_time is None:
            logger.warning("Metrics tracking was not started")
            return
        
        self.end_time = time.time()
        self.results["execution_time"] = round(self.end_time - self.start_time, 3)
        
        # Calculate metrics
        total = self.results["total_tests"]
        
        if total > 0:
            self.results["success_rate"] = round(
                (self.results["passed_tests"] / total) * 100, 2
            )
            
            if self.results["execution_time"] > 0:
                self.results["tests_per_second"] = round(
                    total / self.results["execution_time"], 2
                )
        
        logger.info(f"Metrics tracking completed for: {self.test_name}")
    
    def record_test(self, test_name, passed, message="", duration=0):
        """
        Record a single test result
        
        Args:
            test_name: Name of the test
            passed: Whether test passed (True/False/None for skipped)
            message: Optional message/details
            duration: Optional test duration in seconds
        """
        self.results["total_tests"] += 1
        
        test_detail = {
            "test_name": test_name,
            "passed": passed,
            "message": message,
            "duration": duration
        }
        
        if passed is True:
            self.results["passed_tests"] += 1
            logger.debug(f"✓ Test passed: {test_name}")
        elif passed is False:
            self.results["failed_tests"] += 1
            logger.debug(f"✗ Test failed: {test_name} - {message}")
        else:
            self.results["skipped_tests"] += 1
            logger.debug(f"- Test skipped: {test_name}")
        
        self.results["details"].append(test_detail)
    
    def record_tests(self, tests):
        """
        Record multiple test results
        
        Args:
            tests: List of test dictionaries with keys: 
                  'name', 'passed', 'result' (optional)
        """
        for test in tests:
            name = test.get("name", "Unknown")
            passed = test.get("passed", False)
            result = test.get("result", "")
            
            self.record_test(name, passed, result)
    
    def get_summary(self):
        """
        Get metrics summary
        
        Returns:
            Dictionary with all metrics
        """
        return self.results
    
    def print_summary(self):
        """Print formatted metrics summary to console"""
        summary = self.get_summary()
        
        print("\n" + "="*50)
        print(f"TEST EXECUTION SUMMARY: {summary['test_name']}")
        print("="*50)
        print(f"Timestamp: {summary['timestamp']}")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"  ✓ Passed: {summary['passed_tests']}")
        print(f"  ✗ Failed: {summary['failed_tests']}")
        print(f"  - Skipped: {summary['skipped_tests']}")
        print(f"Success Rate: {summary['success_rate']}%")
        print(f"Execution Time: {summary['execution_time']}s")
        
        if summary['tests_per_second'] > 0:
            print(f"Performance: {summary['tests_per_second']} tests/second")
        
        print("="*50 + "\n")
    
    def export_json(self):
        """
        Export metrics as JSON-compatible dictionary
        
        Returns:
            Dictionary ready for JSON serialization
        """
        return self.results


class TestMetricsTracker:
    """Track metrics for all test types"""
    
    def __init__(self):
        """Initialize all test metrics"""
        self.data_quality_metrics = Metrics("Data Quality Tests")
        self.etl_metrics = Metrics("ETL Tests")
        self.aml_metrics = Metrics("AML Tests")
        self.edge_case_metrics = Metrics("Edge Case Tests")
        self.overall_metrics = Metrics("Overall Test Suite")
    
    def get_all_metrics(self):
        """Get all test metrics"""
        return {
            "data_quality": self.data_quality_metrics.get_summary(),
            "etl": self.etl_metrics.get_summary(),
            "aml": self.aml_metrics.get_summary(),
            "edge_case": self.edge_case_metrics.get_summary(),
            "overall": self.overall_metrics.get_summary()
        }
    
    def print_all_summaries(self):
        """Print all test summaries"""
        self.data_quality_metrics.print_summary()
        self.etl_metrics.print_summary()
        self.aml_metrics.print_summary()
        self.edge_case_metrics.print_summary()
        self.overall_metrics.print_summary()
