#!/usr/bin/env python3
"""
Complexity Analyzer for Python Code
Analyzes cyclomatic complexity, cognitive complexity, and other metrics.
"""

import ast
import os
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class ComplexityType(Enum):
    """Types of complexity analysis."""
    CYCLOMATIC = "cyclomatic"
    COGNITIVE = "cognitive"
    HALSTEAD = "halstead"
    MAINTAINABILITY = "maintainability"


@dataclass
class ComplexityMetrics:
    """Container for complexity metrics."""
    cyclomatic_complexity: int
    cognitive_complexity: int
    halstead_volume: float
    maintainability_index: float
    lines_of_code: int
    num_functions: int
    num_classes: int
    
    def get_complexity_rating(self) -> str:
        """Get complexity rating based on cyclomatic complexity."""
        if self.cyclomatic_complexity <= 10:
            return "Low"
        elif self.cyclomatic_complexity <= 20:
            return "Moderate"
        elif self.cyclomatic_complexity <= 50:
            return "High"
        else:
            return "Very High"


class ComplexityAnalyzer(ast.NodeVisitor):
    """AST visitor for analyzing code complexity."""
    
    def __init__(self):
        self.complexity = 1  # Base complexity
        self.cognitive_complexity = 0
        self.nesting_level = 0
        self.halstead_operators = []
        self.halstead_operands = []
        self.functions = []
        self.classes = []
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition."""
        self.functions.append(node.name)
        old_complexity = self.complexity
        old_cognitive = self.cognitive_complexity
        self.complexity = 1  # Reset for function
        self.cognitive_complexity = 0
        
        self.generic_visit(node)
        
        # Store function complexity
        func_complexity = self.complexity
        func_cognitive = self.cognitive_complexity
        
        # Restore previous complexity
        self.complexity = old_complexity + func_complexity
        self.cognitive_complexity = old_cognitive + func_cognitive
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definition."""
        self.classes.append(node.name)
        self.generic_visit(node)
    
    def visit_If(self, node: ast.If) -> None:
        """Visit if statement."""
        self.complexity += 1
        self.cognitive_complexity += 1 + self.nesting_level
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1
    
    def visit_While(self, node: ast.While) -> None:
        """Visit while loop."""
        self.complexity += 1
        self.cognitive_complexity += 1 + self.nesting_level
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1
    
    def visit_For(self, node: ast.For) -> None:
        """Visit for loop."""
        self.complexity += 1
        self.cognitive_complexity += 1 + self.nesting_level
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1
    
    def visit_Try(self, node: ast.Try) -> None:
        """Visit try statement."""
        self.complexity += len(node.handlers) + len(node.orelse) + len(node.finalbody)
        self.cognitive_complexity += 1 + self.nesting_level
        self.nesting_level += 1
        self.generic_visit(node)
        self.nesting_level -= 1
    
    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        """Visit boolean operation."""
        self.complexity += len(node.values) - 1
        self.cognitive_complexity += len(node.values) - 1
        self.generic_visit(node)


def analyze_file_complexity(file_path: str) -> ComplexityMetrics:
    """Analyze complexity of a Python file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return ComplexityMetrics(0, 0, 0.0, 0.0, 0, 0, 0)
    
    analyzer = ComplexityAnalyzer()
    analyzer.visit(tree)
    
    lines = content.split('\n')
    lines_of_code = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
    
    # Calculate Halstead volume (simplified)
    halstead_volume = len(analyzer.halstead_operators) + len(analyzer.halstead_operands)
    
    # Calculate maintainability index (simplified formula)
    maintainability = max(0, 171 - 5.2 * analyzer.complexity - 0.23 * lines_of_code)
    
    return ComplexityMetrics(
        cyclomatic_complexity=analyzer.complexity,
        cognitive_complexity=analyzer.cognitive_complexity,
        halstead_volume=halstead_volume,
        maintainability_index=maintainability,
        lines_of_code=lines_of_code,
        num_functions=len(analyzer.functions),
        num_classes=len(analyzer.classes)
    )


def analyze_project_complexity(project_path: str) -> Dict[str, ComplexityMetrics]:
    """Analyze complexity for all Python files in a project."""
    results = {}
    
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    metrics = analyze_file_complexity(file_path)
                    results[file_path] = metrics
                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")
    
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python complexity_analyzer.py <path>")
        sys.exit(1)
    
    path = sys.argv[1]
    
    if os.path.isfile(path):
        metrics = analyze_file_complexity(path)
        print(f"Complexity Analysis for {path}:")
        print(f"  Cyclomatic Complexity: {metrics.cyclomatic_complexity} ({metrics.get_complexity_rating()})")
        print(f"  Cognitive Complexity: {metrics.cognitive_complexity}")
        print(f"  Lines of Code: {metrics.lines_of_code}")
        print(f"  Functions: {metrics.num_functions}")
        print(f"  Classes: {metrics.num_classes}")
        print(f"  Maintainability Index: {metrics.maintainability_index:.2f}")
    elif os.path.isdir(path):
        results = analyze_project_complexity(path)
        print(f"Project Complexity Analysis for {path}:")
        for file_path, metrics in results.items():
            print(f"\n{file_path}:")
            print(f"  Complexity: {metrics.cyclomatic_complexity} ({metrics.get_complexity_rating()})")
            print(f"  Cognitive: {metrics.cognitive_complexity}")
            print(f"  Lines: {metrics.lines_of_code}")
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)
