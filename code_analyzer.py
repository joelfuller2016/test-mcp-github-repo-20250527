"""
Advanced Python code file for testing Bifrost MCP coding analysis features.
This file contains various Python constructs to test language analysis.
"""

import json
import os
import sys
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class AnalysisResult:
    """Data class for storing analysis results."""
    file_path: str
    lines_of_code: int
    functions: List[str]
    classes: List[str]
    complexity_score: float
    
    def to_dict(self) -> Dict[str, Union[str, int, float, List[str]]]:
        """Convert to dictionary representation."""
        return {
            'file_path': self.file_path,
            'lines_of_code': self.lines_of_code,
            'functions': self.functions,
            'classes': self.classes,
            'complexity_score': self.complexity_score
        }


class CodeAnalyzer(ABC):
    """Abstract base class for code analyzers."""
    
    @abstractmethod
    def analyze_file(self, file_path: str) -> AnalysisResult:
        """Analyze a single file and return results."""
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """Return list of supported file extensions."""
        pass


class PythonAnalyzer(CodeAnalyzer):
    """Concrete analyzer for Python files."""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.supported_extensions = ['.py', '.pyx', '.pyw']
    
    def analyze_file(self, file_path: str) -> AnalysisResult:
        """Analyze a Python file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        functions = self._extract_functions(content)
        classes = self._extract_classes(content)
        complexity = self._calculate_complexity(content)
        
        return AnalysisResult(
            file_path=file_path,
            lines_of_code=len([line for line in lines if line.strip()]),
            functions=functions,
            classes=classes,
            complexity_score=complexity
        )
    
    def get_supported_extensions(self) -> List[str]:
        """Return supported file extensions."""
        return self.supported_extensions
    
    def _extract_functions(self, content: str) -> List[str]:
        """Extract function names from content."""
        import re
        pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        return re.findall(pattern, content)
    
    def _extract_classes(self, content: str) -> List[str]:
        """Extract class names from content."""
        import re
        pattern = r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[\(:]'
        return re.findall(pattern, content)
    
    def _calculate_complexity(self, content: str) -> float:
        """Calculate a simple complexity score."""
        # Simple complexity based on control structures
        control_keywords = ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally']
        complexity = 1.0  # Base complexity
        
        for keyword in control_keywords:
            complexity += content.count(f' {keyword} ') + content.count(f'\n{keyword} ')
        
        return complexity


class ProjectAnalyzer:
    """Analyzer for entire projects."""
    
    def __init__(self):
        self.analyzers = {
            '.py': PythonAnalyzer()
        }
    
    def analyze_project(self, project_path: str) -> Dict[str, AnalysisResult]:
        """Analyze all supported files in a project."""
        results = {}
        
        for root, dirs, files in os.walk(project_path):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1]
                
                if ext in self.analyzers:
                    try:
                        analyzer = self.analyzers[ext]
                        result = analyzer.analyze_file(file_path)
                        results[file_path] = result
                    except Exception as e:
                        print(f"Error analyzing {file_path}: {e}")
        
        return results
    
    def generate_report(self, results: Dict[str, AnalysisResult]) -> str:
        """Generate a summary report."""
        total_files = len(results)
        total_lines = sum(r.lines_of_code for r in results.values())
        total_functions = sum(len(r.functions) for r in results.values())
        total_classes = sum(len(r.classes) for r in results.values())
        avg_complexity = sum(r.complexity_score for r in results.values()) / total_files if total_files > 0 else 0
        
        report = f"""
Code Analysis Report
===================
Total Files: {total_files}
Total Lines of Code: {total_lines}
Total Functions: {total_functions}
Total Classes: {total_classes}
Average Complexity: {avg_complexity:.2f}

File Details:
"""
        
        for file_path, result in results.items():
            report += f"\n{file_path}:\n"
            report += f"  Lines: {result.lines_of_code}\n"
            report += f"  Functions: {', '.join(result.functions) if result.functions else 'None'}\n"
            report += f"  Classes: {', '.join(result.classes) if result.classes else 'None'}\n"
            report += f"  Complexity: {result.complexity_score:.2f}\n"
        
        return report


def main():
    """Main function to demonstrate the analyzer."""
    if len(sys.argv) < 2:
        print("Usage: python code_analyzer.py <project_path>")
        sys.exit(1)
    
    project_path = sys.argv[1]
    
    if not os.path.exists(project_path):
        print(f"Error: Path '{project_path}' does not exist.")
        sys.exit(1)
    
    analyzer = ProjectAnalyzer()
    results = analyzer.analyze_project(project_path)
    report = analyzer.generate_report(results)
    
    print(report)
    
    # Save results to JSON file
    json_results = {path: result.to_dict() for path, result in results.items()}
    with open('analysis_results.json', 'w') as f:
        json.dump(json_results, f, indent=2)
    
    print("\nResults saved to analysis_results.json")


if __name__ == "__main__":
    main()
