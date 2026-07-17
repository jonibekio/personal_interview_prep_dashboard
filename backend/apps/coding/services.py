"""
Code execution service layer.

Currently returns mock results. In production, integrate with:
- Judge0 API (https://judge0.com)
- Docker Sandbox
- Kubernetes Job
"""
from .models import Submission, TestCase


def run_code(submission: Submission) -> dict:
    """
    Execute code against test cases and return results.

    TODO: Replace with actual execution engine (Judge0 / Docker).
    """
    test_cases = submission.challenge.test_cases.order_by("order")
    total = test_cases.count()
    passed = 0
    results = []

    for tc in test_cases:
        # Mock: always pass for now
        passed += 1
        results.append({
            "input": tc.input_data,
            "expected": tc.expected_output,
            "passed": True,
        })

    submission.test_cases_total = total
    submission.test_cases_passed = passed
    submission.runtime_ms = 120  # Mock
    submission.memory_mb = 14.2  # Mock

    if passed == total:
        submission.status = "accepted"
        submission.output = f"All {total} test cases passed."
    else:
        submission.status = "wrong_answer"
        submission.output = f"{passed}/{total} test cases passed."

    submission.save()

    return {
        "status": submission.status,
        "runtime_ms": submission.runtime_ms,
        "memory_mb": submission.memory_mb,
        "test_cases_passed": passed,
        "test_cases_total": total,
        "output": submission.output,
        "results": results,
    }


def execute_submission(submission: Submission) -> dict:
    """
    Run a single submission (used by both /run and /submit endpoints).
    """
    submission.status = "running"
    submission.save(update_fields=["status"])

    try:
        return run_code(submission)
    except Exception as e:
        submission.status = "runtime_error"
        submission.output = str(e)
        submission.save(update_fields=["status", "output"])
        return {
            "status": "runtime_error",
            "output": str(e),
        }
