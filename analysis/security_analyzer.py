#!/usr/bin/env python3
"""
Security Analyzer for Python Code
Scans for common security vulnerabilities and patterns.
"""

import ast
import re
from typing import List, Dict, Set
from dataclasses import dataclass
from enum import Enum


class SecuritySeverity(Enum):
    """Security issue severity levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


@dataclass
class SecurityIssue:
    """Container for security issues."""
    rule_id: str
    severity: SecuritySeverity
    description: str
    line_number: int
    code_snippet: str
    recommendation: str


class SecurityAnalyzer(ast.NodeVisitor):
    """AST visitor for security analysis."""
    
    def __init__(self, source_lines: List[str]):
        self.issues: List[SecurityIssue] = []
        self.source_lines = source_lines
        self.imports: Set[str] = set()
    
    def add_issue(self, rule_id: str, severity: SecuritySeverity, 
                  description: str, line_number: int, recommendation: str):
        """Add a security issue."""
        code_snippet = self.source_lines[line_number - 1] if line_number <= len(self.source_lines) else ""
        issue = SecurityIssue(
            rule_id=rule_id,
            severity=severity,
            description=description,
            line_number=line_number,
            code_snippet=code_snippet.strip(),
            recommendation=recommendation
        )
        self.issues.append(issue)
    
    def visit_Import(self, node: ast.Import) -> None:
        """Check imports for security issues."""
        for alias in node.names:
            self.imports.add(alias.name)
            
            # Check for dangerous imports
            dangerous_imports = {
                'pickle': 'Pickle can execute arbitrary code during deserialization',
                'subprocess': 'Subprocess can lead to command injection vulnerabilities',
                'eval': 'Direct eval usage can execute arbitrary code',
                'exec': 'Direct exec usage can execute arbitrary code'
            }
            
            if alias.name in dangerous_imports:
                self.add_issue(
                    f"dangerous_import_{alias.name}",
                    SecuritySeverity.HIGH,
                    f"Dangerous import: {dangerous_imports[alias.name]}",
                    node.lineno,
                    f"Review usage of {alias.name} and consider safer alternatives"
                )
        
        self.generic_visit(node)
    
    def visit_Call(self, node: ast.Call) -> None:
        """Check function calls for security issues."""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            
            # Check for dangerous functions
            if func_name == 'eval':
                self.add_issue(
                    "eval_usage",
                    SecuritySeverity.CRITICAL,
                    "Use of eval() can execute arbitrary code",
                    node.lineno,
                    "Replace eval() with ast.literal_eval() or safer parsing"
                )
            
            elif func_name == 'exec':
                self.add_issue(
                    "exec_usage",
                    SecuritySeverity.CRITICAL,
                    "Use of exec() can execute arbitrary code",
                    node.lineno,
                    "Avoid exec() or use restricted execution environments"
                )
            
            elif func_name == 'input' and len(node.args) == 0:
                self.add_issue(
                    "input_without_prompt",
                    SecuritySeverity.MEDIUM,
                    "input() without prompt can be confusing",
                    node.lineno,
                    "Always provide a clear prompt for user input"
                )
        
        elif isinstance(node.func, ast.Attribute):
            # Check for SQL injection patterns
            if (isinstance(node.func.value, ast.Name) and 
                node.func.attr in ['execute', 'executemany']):
                
                for arg in node.args:
                    if isinstance(arg, ast.BinOp) and isinstance(arg.op, (ast.Add, ast.Mod)):
                        self.add_issue(
                            "potential_sql_injection",
                            SecuritySeverity.HIGH,
                            "Potential SQL injection via string concatenation",
                            node.lineno,
                            "Use parameterized queries instead of string concatenation"
                        )
        
        self.generic_visit(node)
    
    def visit_Str(self, node: ast.Str) -> None:
        """Check string literals for security issues."""
        value = node.s.lower()
        
        # Check for hardcoded credentials patterns
        credential_patterns = [
            r'password\s*=\s*["\'][^"\'
]{3,}["\']',
            r'api_key\s*=\s*["\'][^"\'
]{10,}["\']',
            r'secret\s*=\s*["\'][^"\'
]{10,}["\']',
            r'token\s*=\s*["\'][^"\'
]{10,}["\']'
        ]
        
        for pattern in credential_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                self.add_issue(
                    "hardcoded_credentials",
                    SecuritySeverity.HIGH,
                    "Potential hardcoded credentials in string literal",
                    node.lineno,
                    "Use environment variables or secure config files for credentials"
                )
                break
        
        # Check for SQL injection keywords
        sql_keywords = ['select ', 'insert ', 'update ', 'delete ', 'drop ', 'create ']
        if any(keyword in value for keyword in sql_keywords):
            if '%s' in value or '.format(' in self.source_lines[node.lineno - 1]:
                self.add_issue(
                    "sql_injection_string",
                    SecuritySeverity.MEDIUM,
                    "SQL string with potential injection vulnerability",
                    node.lineno,
                    "Use parameterized queries for SQL operations"
                )
        
        self.generic_visit(node)


def analyze_file_security(file_path: str) -> List[SecurityIssue]:
    """Analyze security issues in a Python file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return []
    
    source_lines = content.split('\n')
    analyzer = SecurityAnalyzer(source_lines)
    analyzer.visit(tree)
    
    return analyzer.issues


def generate_security_report(issues: List[SecurityIssue]) -> str:
    """Generate a security report from issues."""
    if not issues:
        return "No security issues found."
    
    report = "Security Analysis Report\n"
    report += "=" * 25 + "\n\n"
    
    # Group by severity
    severity_groups = {}
    for issue in issues:
        if issue.severity not in severity_groups:
            severity_groups[issue.severity] = []
        severity_groups[issue.severity].append(issue)
    
    for severity in [SecuritySeverity.CRITICAL, SecuritySeverity.HIGH, 
                    SecuritySeverity.MEDIUM, SecuritySeverity.LOW]:
        if severity in severity_groups:
            report += f"\n{severity.value} Severity Issues:\n"
            report += "-" * (len(severity.value) + 17) + "\n"
            
            for issue in severity_groups[severity]:
                report += f"\nLine {issue.line_number}: {issue.description}\n"
                report += f"  Code: {issue.code_snippet}\n"
                report += f"  Recommendation: {issue.recommendation}\n"
    
    # Summary
    report += f"\n\nSummary:\n"
    report += f"Total Issues: {len(issues)}\n"
    for severity in severity_groups:
        report += f"{severity.value}: {len(severity_groups[severity])}\n"
    
    return report


if __name__ == "__main__":
    import sys
    import os
    
    if len(sys.argv) != 2:
        print("Usage: python security_analyzer.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist")
        sys.exit(1)
    
    if not file_path.endswith('.py'):
        print("Error: Only Python files (.py) are supported")
        sys.exit(1)
    
    issues = analyze_file_security(file_path)
    report = generate_security_report(issues)
    print(report)
