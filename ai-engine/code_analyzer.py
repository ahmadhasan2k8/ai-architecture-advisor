"""
AST-based Code Analyzer for Design Pattern Opportunities

This module analyzes Python code to identify opportunities for implementing
design patterns and detect anti-patterns in existing code.
"""

import ast
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple, Union
from pathlib import Path
from enum import Enum

from .pattern_knowledge import (
    PatternKnowledge, 
    PATTERN_KNOWLEDGE, 
    PatternConfidence,
    ComplexityLevel
)


class OpportunityType(Enum):
    """Types of pattern opportunities"""
    REFACTOR_TO_PATTERN = "refactor_to_pattern"
    ANTI_PATTERN_DETECTED = "anti_pattern_detected"
    OPTIMIZATION_OPPORTUNITY = "optimization_opportunity"
    COMPLEXITY_REDUCTION = "complexity_reduction"


@dataclass
class PatternOpportunity:
    """Represents a pattern implementation opportunity in code"""
    pattern_name: str
    opportunity_type: OpportunityType
    confidence: PatternConfidence
    file_path: str
    line_number: int
    line_end: Optional[int]
    description: str
    current_code_snippet: str
    suggested_improvement: str
    reasoning: str
    effort_estimate: str  # "Low", "Medium", "High"
    impact_estimate: str  # "Low", "Medium", "High"
    
    @property
    def priority_score(self) -> float:
        """Calculate priority score based on confidence, effort, and impact"""
        confidence_weight = {
            PatternConfidence.LOW: 0.2,
            PatternConfidence.MEDIUM: 0.5,
            PatternConfidence.HIGH: 0.8,
            PatternConfidence.CRITICAL: 1.0
        }
        
        effort_weight = {"Low": 1.0, "Medium": 0.7, "High": 0.4}
        impact_weight = {"Low": 0.3, "Medium": 0.6, "High": 1.0}
        
        return (
            confidence_weight[self.confidence] * 0.4 +
            effort_weight[self.effort_estimate] * 0.3 +
            impact_weight[self.impact_estimate] * 0.3
        )


class CodeAnalyzer(ast.NodeVisitor):
    """AST visitor for analyzing code patterns"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.opportunities: List[PatternOpportunity] = []
        self.current_class: Optional[str] = None
        self.current_function: Optional[str] = None
        self.imports: Set[str] = set()
        
        # Track various code patterns
        self.if_elif_chains: List[Tuple[int, int, List[str]]] = []  # (start_line, length, conditions)
        self.class_constructors: Dict[str, List[str]] = {}  # class_name -> parameter_list
        self.notification_patterns: List[Tuple[int, str]] = []  # (line, pattern_type)
        self.singleton_patterns: List[Tuple[int, str]] = []  # (line, class_name)
        self.factory_patterns: List[Tuple[int, str]] = []  # (line, pattern_description)
        
    def analyze_file(self, source_code: str) -> List[PatternOpportunity]:
        """Analyze source code and return pattern opportunities"""
        try:
            tree = ast.parse(source_code)
            self.visit(tree)
            self._detect_patterns()
            return sorted(self.opportunities, key=lambda x: x.priority_score, reverse=True)
        except SyntaxError as e:
            # Return empty list for files with syntax errors
            return []
    
    def visit_Import(self, node: ast.Import) -> None:
        """Track imports for context"""
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Track from imports for context"""
        if node.module:
            for alias in node.names:
                self.imports.add(f"{node.module}.{alias.name}")
        self.generic_visit(node)
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Analyze class definitions for patterns"""
        old_class = self.current_class
        self.current_class = node.name
        
        # Check for singleton patterns
        self._check_singleton_pattern(node)
        
        # Analyze constructor for builder pattern opportunities
        self._analyze_constructor(node)
        
        # Check for adapter pattern opportunities
        self._check_adapter_pattern(node)
        
        self.generic_visit(node)
        self.current_class = old_class
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Analyze function definitions"""
        old_function = self.current_function
        self.current_function = node.name
        
        # Check for factory method patterns
        if "create" in node.name.lower() or "factory" in node.name.lower():
            self._check_factory_pattern(node)
        
        # Analyze function body for patterns
        self._analyze_function_body(node)
        
        self.generic_visit(node)
        self.current_function = old_function
    
    def visit_If(self, node: ast.If) -> None:
        """Analyze if/elif chains for strategy pattern opportunities"""
        self._analyze_if_elif_chain(node)
        self.generic_visit(node)
    
    def visit_For(self, node: ast.For) -> None:
        """Analyze for loops for observer pattern opportunities"""
        self._check_observer_pattern_in_loop(node)
        self.generic_visit(node)
    
    def _check_singleton_pattern(self, node: ast.ClassDef) -> None:
        """Check for singleton pattern usage and anti-patterns"""
        has_new_method = False
        has_instance_variable = False
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == "__new__":
                has_new_method = True
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and target.id == "_instance":
                        has_instance_variable = True
        
        # Check for singleton implementation
        if has_new_method and has_instance_variable:
            # Check if it's appropriate for singleton
            if self._is_data_model_class(node.name):
                self.opportunities.append(PatternOpportunity(
                    pattern_name="singleton",
                    opportunity_type=OpportunityType.ANTI_PATTERN_DETECTED,
                    confidence=PatternConfidence.CRITICAL,
                    file_path=self.file_path,
                    line_number=node.lineno,
                    line_end=getattr(node, 'end_lineno', None),
                    description=f"Anti-pattern: {node.name} should not be a singleton",
                    current_code_snippet=f"class {node.name} with singleton implementation",
                    suggested_improvement="Convert to regular class - data models should have multiple instances",
                    reasoning="Data models (User, Product, Order, etc.) should not be singletons as you need multiple instances",
                    effort_estimate="Low",
                    impact_estimate="High"
                ))
        
        # Check for singleton opportunities
        elif self._could_benefit_from_singleton(node.name):
            self.opportunities.append(PatternOpportunity(
                pattern_name="singleton",
                opportunity_type=OpportunityType.REFACTOR_TO_PATTERN,
                confidence=PatternConfidence.MEDIUM,
                file_path=self.file_path,
                line_number=node.lineno,
                line_end=getattr(node, 'end_lineno', None),
                description=f"{node.name} could benefit from singleton pattern",
                current_code_snippet=f"class {node.name}",
                suggested_improvement="Implement singleton pattern with thread-safe instance control",
                reasoning="Classes like DatabaseConnection, ConfigManager, Logger often benefit from singleton",
                effort_estimate="Medium",
                impact_estimate="Medium"
            ))
    
    def _analyze_constructor(self, node: ast.ClassDef) -> None:
        """Analyze __init__ method for builder pattern opportunities"""
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                param_count = len(item.args.args) - 1  # Exclude 'self'
                
                # Check for builder pattern opportunity
                if param_count >= 5:
                    optional_params = len([arg for arg in item.args.defaults])
                    
                    confidence = PatternConfidence.HIGH if param_count >= 7 else PatternConfidence.MEDIUM
                    
                    self.opportunities.append(PatternOpportunity(
                        pattern_name="builder",
                        opportunity_type=OpportunityType.REFACTOR_TO_PATTERN,
                        confidence=confidence,
                        file_path=self.file_path,
                        line_number=item.lineno,
                        line_end=getattr(item, 'end_lineno', None),
                        description=f"Constructor with {param_count} parameters could benefit from Builder pattern",
                        current_code_snippet=f"def __init__(self, {param_count} parameters)",
                        suggested_improvement="Implement Builder pattern for more readable object construction",
                        reasoning=f"Constructor has {param_count} parameters ({optional_params} optional). Builder pattern threshold: 5+ parameters",
                        effort_estimate="Medium" if param_count < 8 else "High",
                        impact_estimate="Medium"
                    ))
                break
    
    def _analyze_if_elif_chain(self, node: ast.If) -> None:
        """Analyze if/elif chains for strategy or factory pattern opportunities"""
        chain_length = 1
        conditions = []
        current = node
        
        # Count the chain length
        while current:
            if isinstance(current.test, ast.Compare):
                # Extract comparison for analysis
                if hasattr(current.test.left, 'id'):
                    conditions.append(current.test.left.id)
            elif isinstance(current.test, ast.Call):
                # isinstance() calls might indicate factory pattern
                if hasattr(current.test.func, 'id') and current.test.func.id == 'isinstance':
                    conditions.append('isinstance')
            
            if current.orelse and len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
                current = current.orelse[0]
                chain_length += 1
            else:
                break
        
        # Strategy pattern opportunity
        if chain_length >= 3:
            # Check if it's algorithm selection
            if self._looks_like_algorithm_selection(node):
                self.opportunities.append(PatternOpportunity(
                    pattern_name="strategy",
                    opportunity_type=OpportunityType.REFACTOR_TO_PATTERN,
                    confidence=PatternConfidence.HIGH if chain_length >= 4 else PatternConfidence.MEDIUM,
                    file_path=self.file_path,
                    line_number=node.lineno,
                    line_end=getattr(node, 'end_lineno', None),
                    description=f"Long if/elif chain ({chain_length} conditions) suggests Strategy pattern",
                    current_code_snippet=f"if/elif chain with {chain_length} conditions",
                    suggested_improvement="Replace with Strategy pattern for better maintainability",
                    reasoning=f"Chain length {chain_length} exceeds threshold of 3. Strategy pattern helps eliminate conditionals",
                    effort_estimate="Medium",
                    impact_estimate="Medium"
                ))
        
        # Factory pattern opportunity
        if 'isinstance' in conditions and chain_length >= 2:
            self.opportunities.append(PatternOpportunity(
                pattern_name="factory",
                opportunity_type=OpportunityType.REFACTOR_TO_PATTERN,
                confidence=PatternConfidence.MEDIUM,
                file_path=self.file_path,
                line_number=node.lineno,
                line_end=getattr(node, 'end_lineno', None),
                description="Type-based conditionals suggest Factory pattern",
                current_code_snippet="if/elif with isinstance() checks",
                suggested_improvement="Use Factory pattern to encapsulate object creation logic",
                reasoning="Multiple isinstance() checks indicate object creation based on type",
                effort_estimate="Medium",
                impact_estimate="Medium"
            ))
    
    def _check_observer_pattern_in_loop(self, node: ast.For) -> None:
        """Check for manual observer pattern implementation in loops"""
        # Look for notification loops
        if isinstance(node.iter, ast.Name):
            iter_name = node.iter.id.lower()
            if any(keyword in iter_name for keyword in ['observer', 'listener', 'subscriber', 'notification']):
                # Check if loop contains method calls that look like notifications
                for item in ast.walk(node):
                    if isinstance(item, ast.Call) and isinstance(item.func, ast.Attribute):
                        method_name = item.func.attr.lower()
                        if any(keyword in method_name for keyword in ['update', 'notify', 'on_', 'handle']):
                            self.opportunities.append(PatternOpportunity(
                                pattern_name="observer",
                                opportunity_type=OpportunityType.REFACTOR_TO_PATTERN,
                                confidence=PatternConfidence.MEDIUM,
                                file_path=self.file_path,
                                line_number=node.lineno,
                                line_end=getattr(node, 'end_lineno', None),
                                description="Manual observer notification loop detected",
                                current_code_snippet=f"for loop over {iter_name} with notification calls",
                                suggested_improvement="Implement formal Observer pattern with subscription management",
                                reasoning="Manual loops for notifications suggest need for Observer pattern",
                                effort_estimate="Low",
                                impact_estimate="Medium"
                            ))
                            break
    
    def _check_factory_pattern(self, node: ast.FunctionDef) -> None:
        """Check for factory pattern opportunities in functions"""
        # Look for functions that return different types based on parameters
        return_statements = []
        for item in ast.walk(node):
            if isinstance(item, ast.Return) and item.value:
                if isinstance(item.value, ast.Call):
                    return_statements.append(item.value)
        
        if len(return_statements) >= 2:
            # Multiple return types might indicate factory pattern
            self.opportunities.append(PatternOpportunity(
                pattern_name="factory",
                opportunity_type=OpportunityType.OPTIMIZATION_OPPORTUNITY,
                confidence=PatternConfidence.MEDIUM,
                file_path=self.file_path,
                line_number=node.lineno,
                line_end=getattr(node, 'end_lineno', None),
                description=f"Function {node.name} returns multiple types - consider Factory pattern",
                current_code_snippet=f"def {node.name}() with {len(return_statements)} different return types",
                suggested_improvement="Formalize as Factory pattern with clear interface",
                reasoning=f"Function returns {len(return_statements)} different types, suggesting factory behavior",
                effort_estimate="Low",
                impact_estimate="Low"
            ))
    
    def _check_adapter_pattern(self, node: ast.ClassDef) -> None:
        """Check for adapter pattern opportunities"""
        # Look for classes that wrap other objects
        has_adaptee = False
        has_delegation = False
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                # Check if constructor takes another object
                if len(item.args.args) >= 2:  # self + at least one param
                    has_adaptee = True
            elif isinstance(item, ast.FunctionDef):
                # Check for delegation patterns
                for subitem in ast.walk(item):
                    if isinstance(subitem, ast.Attribute) and isinstance(subitem.value, ast.Name):
                        if subitem.value.id != 'self':
                            has_delegation = True
                            break
        
        if has_adaptee and has_delegation:
            self.opportunities.append(PatternOpportunity(
                pattern_name="adapter",
                opportunity_type=OpportunityType.OPTIMIZATION_OPPORTUNITY,
                confidence=PatternConfidence.LOW,
                file_path=self.file_path,
                line_number=node.lineno,
                line_end=getattr(node, 'end_lineno', None),
                description=f"Class {node.name} shows adapter-like behavior",
                current_code_snippet=f"class {node.name} with delegation pattern",
                suggested_improvement="Consider formalizing as Adapter pattern if interfacing incompatible classes",
                reasoning="Class takes object in constructor and delegates calls - possible adapter",
                effort_estimate="Low",
                impact_estimate="Low"
            ))
    
    def _analyze_function_body(self, node: ast.FunctionDef) -> None:
        """Analyze function body for various patterns"""
        # Check for command pattern opportunities
        if any(keyword in node.name.lower() for keyword in ['execute', 'run', 'perform', 'do']):
            # Look for state storage that might indicate command pattern
            has_state_storage = False
            for item in ast.walk(node):
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                            if target.value.id == 'self':
                                has_state_storage = True
                                break
            
            if has_state_storage:
                self.opportunities.append(PatternOpportunity(
                    pattern_name="command",
                    opportunity_type=OpportunityType.OPTIMIZATION_OPPORTUNITY,
                    confidence=PatternConfidence.LOW,
                    file_path=self.file_path,
                    line_number=node.lineno,
                    line_end=getattr(node, 'end_lineno', None),
                    description=f"Function {node.name} stores state - consider Command pattern",
                    current_code_snippet=f"def {node.name}() with state storage",
                    suggested_improvement="Consider Command pattern if undo/redo or queuing needed",
                    reasoning="Function stores state and has execution-like name - possible command",
                    effort_estimate="Medium",
                    impact_estimate="Low"
                ))
    
    def _detect_patterns(self) -> None:
        """Detect higher-level patterns from collected data"""
        # Additional pattern detection logic can be added here
        pass
    
    def _is_data_model_class(self, class_name: str) -> bool:
        """Check if class name suggests it's a data model"""
        data_model_patterns = [
            'user', 'product', 'order', 'customer', 'item', 'model',
            'entity', 'record', 'data', 'person', 'account', 'invoice'
        ]
        return any(pattern in class_name.lower() for pattern in data_model_patterns)
    
    def _could_benefit_from_singleton(self, class_name: str) -> bool:
        """Check if class could benefit from singleton pattern"""
        singleton_candidates = [
            'database', 'connection', 'config', 'settings', 'logger',
            'cache', 'registry', 'manager', 'service', 'client'
        ]
        return any(candidate in class_name.lower() for candidate in singleton_candidates)
    
    def _looks_like_algorithm_selection(self, node: ast.If) -> bool:
        """Check if if/elif chain looks like algorithm selection"""
        # Heuristic: look for different method calls or operations in each branch
        branches = []
        current = node
        
        while current:
            branch_calls = set()
            for item in ast.walk(current):
                if isinstance(item, ast.Call) and isinstance(item.func, ast.Name):
                    branch_calls.add(item.func.id)
                elif isinstance(item, ast.Call) and isinstance(item.func, ast.Attribute):
                    branch_calls.add(item.func.attr)
            branches.append(branch_calls)
            
            if current.orelse and len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
                current = current.orelse[0]
            else:
                break
        
        # If branches have different method calls, likely algorithm selection
        if len(branches) >= 2:
            all_calls = set().union(*branches)
            return len(all_calls) >= len(branches)  # Different algorithms likely use different methods
        
        return False


def analyze_file(file_path: Union[str, Path]) -> List[PatternOpportunity]:
    """Analyze a single Python file for pattern opportunities"""
    file_path = Path(file_path)
    
    if not file_path.exists() or file_path.suffix != '.py':
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        analyzer = CodeAnalyzer(str(file_path))
        return analyzer.analyze_file(source_code)
    
    except (IOError, UnicodeDecodeError):
        return []


def analyze_directory(directory_path: Union[str, Path], 
                     exclude_patterns: Optional[List[str]] = None) -> Dict[str, List[PatternOpportunity]]:
    """Analyze all Python files in a directory for pattern opportunities"""
    directory_path = Path(directory_path)
    exclude_patterns = exclude_patterns or ['__pycache__', '.git', '.venv', 'venv', 'env']
    
    results = {}
    
    for py_file in directory_path.rglob('*.py'):
        # Skip excluded directories
        if any(pattern in str(py_file) for pattern in exclude_patterns):
            continue
        
        opportunities = analyze_file(py_file)
        if opportunities:  # Only include files with opportunities
            results[str(py_file)] = opportunities
    
    return results


def generate_analysis_report(opportunities_by_file: Dict[str, List[PatternOpportunity]]) -> str:
    """Generate a human-readable analysis report"""
    total_opportunities = sum(len(ops) for ops in opportunities_by_file.values())
    
    if total_opportunities == 0:
        return "🎉 No pattern opportunities detected! Your code looks well-structured."
    
    report = f"# Pattern Analysis Report\n\n"
    report += f"**Total Opportunities Found**: {total_opportunities} across {len(opportunities_by_file)} files\n\n"
    
    # Group by pattern type
    by_pattern = {}
    for opportunities in opportunities_by_file.values():
        for opp in opportunities:
            if opp.pattern_name not in by_pattern:
                by_pattern[opp.pattern_name] = []
            by_pattern[opp.pattern_name].append(opp)
    
    report += "## Summary by Pattern\n\n"
    for pattern, opportunities in sorted(by_pattern.items()):
        count = len(opportunities)
        high_priority = len([o for o in opportunities if o.priority_score > 0.7])
        report += f"- **{pattern.title()}**: {count} opportunities ({high_priority} high priority)\n"
    
    report += "\n## High Priority Opportunities\n\n"
    all_opportunities = []
    for opportunities in opportunities_by_file.values():
        all_opportunities.extend(opportunities)
    
    high_priority = sorted([o for o in all_opportunities if o.priority_score > 0.7], 
                          key=lambda x: x.priority_score, reverse=True)
    
    for i, opp in enumerate(high_priority[:10], 1):  # Top 10
        report += f"### {i}. {opp.pattern_name.title()} Pattern\n"
        report += f"**File**: {opp.file_path}:{opp.line_number}\n"
        report += f"**Confidence**: {opp.confidence.value.title()}\n"
        report += f"**Description**: {opp.description}\n"
        report += f"**Reasoning**: {opp.reasoning}\n"
        report += f"**Effort**: {opp.effort_estimate} | **Impact**: {opp.impact_estimate}\n\n"
    
    if len(high_priority) > 10:
        report += f"... and {len(high_priority) - 10} more high priority opportunities.\n\n"
    
    return report