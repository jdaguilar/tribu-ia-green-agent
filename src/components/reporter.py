"""Reporting and artifact management for the Code Agent Benchmark."""

from a2a.server.tasks import TaskUpdater
from a2a.types import Part, TextPart, DataPart
from models import BenchmarkResult


class BenchmarkReporter:
    """Handles result formatting and artifact generation."""

    @staticmethod
    def generate_summary(benchmark_result: BenchmarkResult) -> str:
        """Create a human-readable summary of the benchmark results."""
        summary = f"""
Benchmark Complete!

Results:
- Total Tasks: {benchmark_result.total_tasks}
- Passed: {benchmark_result.tasks_passed}
- Failed: {benchmark_result.tasks_failed}
- Average Score: {benchmark_result.average_score:.2%}
"""
        
        # Add execution time statistics if available
        if benchmark_result.total_execution_time_seconds is not None:
            summary += f"- Total Execution Time: {benchmark_result.total_execution_time_seconds:.2f}s\n"
        if benchmark_result.average_execution_time_seconds is not None:
            summary += f"- Average Execution Time per Task: {benchmark_result.average_execution_time_seconds:.2f}s\n"
        
        summary += "\nTask Breakdown:\n"
        for result in benchmark_result.task_results:
            status = "✓" if result.passed else "✗"
            time_str = ""
            if result.agent_execution_time_seconds is not None:
                time_str = f" ({result.agent_execution_time_seconds:.2f}s)"
            summary += f"\n{status} {result.task_title}: {result.score:.2%}{time_str}"

        return summary

    @staticmethod
    async def add_artifacts(
        updater: TaskUpdater, benchmark_result: BenchmarkResult, summary: str
    ):
        """Add benchmark result artifacts to the task updater."""
        await updater.add_artifact(
            parts=[
                Part(root=TextPart(text=summary)),
                Part(root=DataPart(data=benchmark_result.model_dump())),
            ],
            name="Benchmark Results",
        )
