# Code Analysis Tools

This directory contains advanced code analysis tools for Python projects, designed to work with the Bifrost MCP GitHub CLI server.

## Tools

### 1. Complexity Analyzer (`complexity_analyzer.py`)

Analyzes code complexity metrics including:
- **Cyclomatic Complexity**: Measures the number of linearly independent paths through code
- **Cognitive Complexity**: Measures how difficult code is to understand
- **Halstead Volume**: Estimates the mental effort required to understand code
- **Maintainability Index**: Calculated metric for code maintainability

**Usage:**
```bash
# Analyze a single file
python complexity_analyzer.py path/to/file.py

# Analyze entire project
python complexity_analyzer.py path/to/project/
```

**Complexity Ratings:**
- **Low (1-10)**: Easy to test and maintain
- **Moderate (11-20)**: Slightly complex
- **High (21-50)**: Complex, consider refactoring
- **Very High (50+)**: Very complex, refactoring recommended

### 2. Security Analyzer (`security_analyzer.py`)

Scans for common security vulnerabilities:
- **Dangerous Imports**: Identifies risky modules (pickle, eval, exec)
- **Code Injection**: Detects eval() and exec() usage
- **SQL Injection**: Identifies potential SQL injection patterns
- **Hardcoded Credentials**: Finds potential hardcoded passwords/tokens

**Usage:**
```bash
python security_analyzer.py path/to/file.py
```

**Severity Levels:**
- **Critical**: Immediate security risk
- **High**: Significant security concern
- **Medium**: Moderate security issue
- **Low**: Minor security consideration

## Integration with Bifrost MCP

These tools are designed to work seamlessly with the Bifrost MCP GitHub CLI server:

1. **Automated Analysis**: Run analysis on repositories via MCP commands
2. **Issue Creation**: Automatically create GitHub issues for security vulnerabilities
3. **PR Integration**: Include analysis results in pull request reviews
4. **Continuous Monitoring**: Set up workflows to analyze code on commits

## Example Workflow

```python
# Via Bifrost MCP GitHub CLI
# 1. Clone repository
# 2. Run analysis tools
# 3. Generate reports
# 4. Create issues for critical findings
# 5. Update documentation
```

## Advanced Features

### Complexity Analysis
- **AST-based parsing** for accurate analysis
- **Function-level metrics** with nesting awareness
- **Project-wide aggregation** for overview insights
- **Customizable thresholds** for different project types

### Security Analysis
- **Pattern matching** for vulnerability detection
- **Context-aware analysis** considering code structure
- **Extensible rule system** for custom security rules
- **Integration ready** for CI/CD pipelines

## Best Practices

1. **Regular Analysis**: Run tools on every commit
2. **Threshold Monitoring**: Set complexity limits for code review
3. **Security First**: Address critical security issues immediately
4. **Documentation**: Keep analysis results in repository documentation
5. **Team Training**: Ensure team understands metrics and recommendations

## Future Enhancements

- [ ] Support for additional languages (JavaScript, TypeScript, Java)
- [ ] Machine learning-based anomaly detection
- [ ] Integration with popular IDEs
- [ ] Real-time analysis during development
- [ ] Advanced visualization dashboards
- [ ] Custom rule configuration files

## Contributing

Contributions welcome! Please:
1. Add tests for new features
2. Update documentation
3. Follow existing code style
4. Include examples for new analyzers

---

*These tools were created to demonstrate the advanced coding and analysis capabilities of the Bifrost MCP GitHub CLI server.*
