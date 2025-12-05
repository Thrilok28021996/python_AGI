"""
Security Scanner
Automatic security vulnerability scanning for AI-generated projects
Supports Python (bandit) and general code analysis
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional
import colorama
import re

colorama.init(autoreset=True)


class SecurityScanner:
    """
    Scans projects for security vulnerabilities
    Integrates with bandit for Python, and provides general security checks
    """

    def __init__(self, project_path: str):
        """
        Initialize security scanner

        Args:
            project_path: Path to the project directory
        """
        self.project_path = Path(project_path)
        self.vulnerabilities = []

    def scan_project(self) -> Dict:
        """
        Run comprehensive security scan

        Returns:
            Dict with vulnerability results
        """
        print(colorama.Fore.CYAN + "\n🔒 Running Security Scan..." + colorama.Style.RESET_ALL)

        results = {
            "timestamp": None,
            "vulnerabilities": [],
            "severity_counts": {"high": 0, "medium": 0, "low": 0},
            "scans_run": []
        }

        # Detect project type and run appropriate scans
        if self._is_python_project():
            print(colorama.Fore.CYAN + "  📝 Detected Python project" + colorama.Style.RESET_ALL)
            python_vulns = self._scan_python()
            results["vulnerabilities"].extend(python_vulns)
            results["scans_run"].append("bandit (Python)")

        # Run general security checks
        general_vulns = self._scan_general_issues()
        results["vulnerabilities"].extend(general_vulns)
        results["scans_run"].append("General security checks")

        # Count severities
        for vuln in results["vulnerabilities"]:
            severity = vuln.get("severity", "low").lower()
            if severity in results["severity_counts"]:
                results["severity_counts"][severity] += 1

        self.vulnerabilities = results["vulnerabilities"]
        return results

    def _is_python_project(self) -> bool:
        """Check if project contains Python files (excludes system files)"""
        from utils import should_ignore_file
        py_files = [f for f in self.project_path.glob("**/*.py") if not should_ignore_file(f)]
        return len(py_files) > 0

    def _scan_python(self) -> List[Dict]:
        """Scan Python code with bandit"""
        vulnerabilities = []

        try:
            # Check if bandit is installed
            check_result = subprocess.run(
                ['bandit', '--version'],
                capture_output=True,
                timeout=5
            )

            if check_result.returncode != 0:
                print(colorama.Fore.YELLOW + "  ⚠️  Bandit not installed. Install with: pip install bandit" + colorama.Style.RESET_ALL)
                return vulnerabilities

            # Run bandit
            result = subprocess.run(
                ['bandit', '-r', '.', '-f', 'json', '-ll'],  # -ll = low severity and above
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            # Bandit returns non-zero if issues found, but that's not an error
            if result.stdout:
                try:
                    data = json.loads(result.stdout)
                    vulnerabilities = self._parse_bandit_results(data)
                    print(colorama.Fore.GREEN + f"  ✓ Bandit scan complete: {len(vulnerabilities)} issues found" + colorama.Style.RESET_ALL)
                except json.JSONDecodeError:
                    print(colorama.Fore.YELLOW + "  ⚠️  Could not parse bandit output" + colorama.Style.RESET_ALL)

        except subprocess.TimeoutExpired:
            print(colorama.Fore.RED + "  ✗ Bandit scan timed out" + colorama.Style.RESET_ALL)
        except FileNotFoundError:
            print(colorama.Fore.YELLOW + "  ⚠️  Bandit not found. Install with: pip install bandit" + colorama.Style.RESET_ALL)
        except Exception as e:
            print(colorama.Fore.RED + f"  ✗ Bandit scan error: {e}" + colorama.Style.RESET_ALL)

        return vulnerabilities

    def _parse_bandit_results(self, data: Dict) -> List[Dict]:
        """Parse bandit JSON output"""
        vulnerabilities = []

        for result in data.get("results", []):
            vulnerabilities.append({
                "tool": "bandit",
                "severity": result.get("issue_severity", "UNKNOWN").lower(),
                "confidence": result.get("issue_confidence", "UNKNOWN"),
                "issue_id": result.get("test_id", ""),
                "description": result.get("issue_text", "No description"),
                "file": result.get("filename", "unknown"),
                "line": result.get("line_number", 0),
                "code": result.get("code", ""),
                "more_info": result.get("more_info", "")
            })

        return vulnerabilities

    def _scan_general_issues(self) -> List[Dict]:
        """
        Scan for common security issues across all file types
        Checks for hardcoded secrets, weak patterns, etc.
        """
        vulnerabilities = []

        # Patterns to detect
        patterns = {
            "hardcoded_password": {
                "pattern": r'password\s*=\s*["\']([^"\']+)["\']',
                "severity": "high",
                "description": "Hardcoded password detected"
            },
            "hardcoded_api_key": {
                "pattern": r'api[_-]?key\s*=\s*["\']([^"\']+)["\']',
                "severity": "high",
                "description": "Hardcoded API key detected"
            },
            "hardcoded_secret": {
                "pattern": r'secret\s*=\s*["\']([^"\']+)["\']',
                "severity": "high",
                "description": "Hardcoded secret detected"
            },
            "sql_injection_risk": {
                "pattern": r'execute\s*\(\s*["\'].*%s.*["\']',
                "severity": "medium",
                "description": "Potential SQL injection vulnerability (string formatting in query)"
            },
            "weak_random": {
                "pattern": r'import\s+random[^_]',
                "severity": "medium",
                "description": "Using weak random number generator (use secrets module for security)"
            },
            "eval_usage": {
                "pattern": r'\beval\s*\(',
                "severity": "high",
                "description": "Use of eval() detected - potential code injection risk"
            },
            "exec_usage": {
                "pattern": r'\bexec\s*\(',
                "severity": "high",
                "description": "Use of exec() detected - potential code injection risk"
            }
        }

        # Scan all Python files (excludes system files)
        from utils import should_ignore_file
        for py_file in self.project_path.glob("**/*.py"):
            if should_ignore_file(py_file):
                continue
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                for issue_type, config in patterns.items():
                    matches = re.finditer(config["pattern"], content, re.IGNORECASE)

                    for match in matches:
                        # Find line number
                        line_num = content[:match.start()].count('\n') + 1

                        vulnerabilities.append({
                            "tool": "security_scanner",
                            "severity": config["severity"],
                            "confidence": "medium",
                            "issue_id": issue_type,
                            "description": config["description"],
                            "file": str(py_file.relative_to(self.project_path)),
                            "line": line_num,
                            "code": lines[line_num - 1].strip() if line_num <= len(lines) else "",
                            "matched_text": match.group(0)
                        })

            except Exception as e:
                print(colorama.Fore.YELLOW + f"  ⚠️  Could not scan {py_file.name}: {e}" + colorama.Style.RESET_ALL)

        if vulnerabilities:
            print(colorama.Fore.GREEN + f"  ✓ General security scan complete: {len(vulnerabilities)} issues found" + colorama.Style.RESET_ALL)

        return vulnerabilities

    def generate_report(self, results: Dict) -> str:
        """
        Generate human-readable security report

        Args:
            results: Results from scan_project()

        Returns:
            Formatted report string
        """
        total_vulns = len(results['vulnerabilities'])
        high_count = results['severity_counts']['high']
        medium_count = results['severity_counts']['medium']
        low_count = results['severity_counts']['low']

        # Determine overall severity
        if high_count > 0:
            overall_status = "🔴 CRITICAL"
            status_color = colorama.Fore.RED
        elif medium_count > 0:
            overall_status = "🟡 WARNING"
            status_color = colorama.Fore.YELLOW
        elif low_count > 0:
            overall_status = "🟢 INFO"
            status_color = colorama.Fore.GREEN
        else:
            overall_status = "✅ SECURE"
            status_color = colorama.Fore.GREEN

        report = f"""
{status_color}{'='*80}
🔒 SECURITY SCAN REPORT
{'='*80}{colorama.Style.RESET_ALL}

Status: {overall_status}
Scans Run: {', '.join(results['scans_run'])}

Vulnerabilities Found: {total_vulns}
  🔴 High Severity: {high_count}
  🟡 Medium Severity: {medium_count}
  🟢 Low Severity: {low_count}

"""

        if results['vulnerabilities']:
            report += f"{colorama.Fore.YELLOW}{'='*80}\nDETAILED FINDINGS\n{'='*80}{colorama.Style.RESET_ALL}\n\n"

            # Group by severity
            by_severity = {"high": [], "medium": [], "low": []}
            for vuln in results['vulnerabilities']:
                severity = vuln.get("severity", "low").lower()
                if severity in by_severity:
                    by_severity[severity].append(vuln)

            # Show high severity first
            for severity in ["high", "medium", "low"]:
                vulns = by_severity[severity]
                if not vulns:
                    continue

                severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}[severity]
                report += f"{severity_emoji} {severity.upper()} SEVERITY ({len(vulns)} issues)\n"
                report += "-" * 80 + "\n\n"

                for i, vuln in enumerate(vulns, 1):
                    report += f"{i}. {vuln['description']}\n"
                    report += f"   File: {vuln['file']}:{vuln.get('line', '?')}\n"
                    report += f"   Tool: {vuln['tool']}\n"

                    if vuln.get('code'):
                        report += f"   Code: {vuln['code'][:100]}\n"

                    if vuln.get('more_info'):
                        report += f"   More Info: {vuln['more_info']}\n"

                    report += "\n"

            # Recommendations
            report += f"{colorama.Fore.CYAN}{'='*80}\nRECOMMENDATIONS\n{'='*80}{colorama.Style.RESET_ALL}\n\n"

            if high_count > 0:
                report += "⚠️  URGENT: Fix high severity issues immediately before deployment.\n"
            if medium_count > 0:
                report += "⚠️  Address medium severity issues in next iteration.\n"
            if low_count > 0:
                report += "ℹ️  Review low severity issues when time permits.\n"

            report += "\n"

        else:
            report += f"{colorama.Fore.GREEN}{'='*80}\n"
            report += "✅ No security vulnerabilities detected!\n"
            report += "Your code passed all security checks.\n"
            report += f"{'='*80}{colorama.Style.RESET_ALL}\n\n"

        return report

    def get_fix_suggestions(self) -> List[str]:
        """
        Generate automated fix suggestions for security agent

        Returns:
            List of fix suggestions
        """
        suggestions = []

        for vuln in self.vulnerabilities:
            suggestion = f"Fix {vuln['severity']} severity issue in {vuln['file']}:{vuln['line']}: {vuln['description']}"

            # Add specific fix guidance
            issue_id = vuln.get('issue_id', '')

            if 'hardcoded_password' in issue_id or 'hardcoded' in issue_id:
                suggestion += "\n  → Move to environment variables or secure vault"
            elif 'sql_injection' in issue_id:
                suggestion += "\n  → Use parameterized queries instead of string formatting"
            elif 'eval' in issue_id or 'exec' in issue_id:
                suggestion += "\n  → Use safer alternatives like ast.literal_eval() or remove dynamic code execution"
            elif 'random' in issue_id:
                suggestion += "\n  → Use secrets module for cryptographic operations"

            suggestions.append(suggestion)

        return suggestions


# Example usage and testing
if __name__ == "__main__":
    import tempfile
    import shutil

    # Create a test project with vulnerabilities
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"\n🧪 Testing Security Scanner in: {tmpdir}\n")

        # Create vulnerable Python file
        vuln_code = '''
import random  # Weak random

def login(username, password):
    # Hardcoded password (BAD!)
    admin_password = "admin123"

    if password == admin_password:
        return True

    # SQL injection risk
    query = "SELECT * FROM users WHERE username='%s'" % username
    execute(query)

    return False

# Eval usage (DANGEROUS!)
user_input = "print('hello')"
eval(user_input)
'''

        test_file = Path(tmpdir) / "vulnerable.py"
        test_file.write_text(vuln_code)

        # Run scanner
        scanner = SecurityScanner(tmpdir)
        results = scanner.scan_project()

        # Generate report
        report = scanner.generate_report(results)
        print(report)

        # Get fix suggestions
        suggestions = scanner.get_fix_suggestions()
        if suggestions:
            print(colorama.Fore.CYAN + "FIX SUGGESTIONS:" + colorama.Style.RESET_ALL)
            for suggestion in suggestions[:5]:
                print(f"  • {suggestion}\n")

        print(f"\n✅ Test complete! Found {len(results['vulnerabilities'])} vulnerabilities")
