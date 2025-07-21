"""
Repository-level Pattern Analysis

This module provides high-level analysis of entire repositories to identify
architectural pattern opportunities and anti-patterns.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union
from dataclasses import dataclass, asdict
from collections import defaultdict

from .code_analyzer import analyze_directory, PatternOpportunity, OpportunityType
from .pattern_knowledge import PatternConfidence


@dataclass
class ArchitecturalInsight:
    """High-level architectural insight about the repository"""
    insight_type: str  # "architectural_pattern", "anti_pattern", "optimization"
    title: str
    description: str
    affected_files: List[str]
    confidence: PatternConfidence
    impact: str  # "Low", "Medium", "High", "Critical"
    effort: str  # "Low", "Medium", "High"
    recommendations: List[str]
    
    @property
    def priority_score(self) -> float:
        """Calculate priority score for this insight"""
        confidence_weight = {
            PatternConfidence.LOW: 0.2,
            PatternConfidence.MEDIUM: 0.5,
            PatternConfidence.HIGH: 0.8,
            PatternConfidence.CRITICAL: 1.0
        }
        
        effort_weight = {"Low": 1.0, "Medium": 0.7, "High": 0.4}
        impact_weight = {"Low": 0.3, "Medium": 0.6, "High": 0.8, "Critical": 1.0}
        
        return (
            confidence_weight[self.confidence] * 0.4 +
            effort_weight[self.effort] * 0.2 +
            impact_weight[self.impact] * 0.4
        )


@dataclass
class RepositoryAnalysis:
    """Complete analysis of a repository"""
    repository_path: str
    total_files_analyzed: int
    total_opportunities: int
    opportunities_by_file: Dict[str, List[PatternOpportunity]]
    architectural_insights: List[ArchitecturalInsight]
    pattern_usage_summary: Dict[str, int]
    complexity_assessment: str
    recommendations_summary: List[str]


class RepositoryAnalyzer:
    """Analyzes entire repositories for pattern opportunities and architectural insights"""
    
    def __init__(self, repository_path: Union[str, Path]):
        self.repository_path = Path(repository_path)
        self.opportunities_by_file: Dict[str, List[PatternOpportunity]] = {}
        self.architectural_insights: List[ArchitecturalInsight] = []
        
    def analyze(self, exclude_patterns: Optional[List[str]] = None) -> RepositoryAnalysis:
        """Perform comprehensive repository analysis"""
        # Default exclusions for common non-source directories
        default_exclusions = [
            '__pycache__', '.git', '.venv', 'venv', 'env', 'node_modules',
            '.pytest_cache', '.mypy_cache', 'dist', 'build', '.tox'
        ]
        exclude_patterns = (exclude_patterns or []) + default_exclusions
        
        # Analyze individual files
        self.opportunities_by_file = analyze_directory(
            self.repository_path, 
            exclude_patterns=exclude_patterns
        )
        
        # Generate architectural insights
        self._generate_architectural_insights()
        
        # Create summary
        return self._create_analysis_summary()
    
    def _generate_architectural_insights(self) -> None:
        """Generate high-level architectural insights from file-level opportunities"""
        
        # Collect all opportunities
        all_opportunities = []
        for opportunities in self.opportunities_by_file.values():
            all_opportunities.extend(opportunities)
        
        # Group opportunities by pattern
        by_pattern = defaultdict(list)
        for opp in all_opportunities:
            by_pattern[opp.pattern_name].append(opp)
        
        # Analyze patterns
        self._analyze_singleton_usage(by_pattern.get('singleton', []))
        self._analyze_factory_opportunities(by_pattern.get('factory', []))
        self._analyze_observer_opportunities(by_pattern.get('observer', []))
        self._analyze_strategy_opportunities(by_pattern.get('strategy', []))
        self._analyze_builder_opportunities(by_pattern.get('builder', []))
        self._analyze_repository_opportunities(by_pattern.get('repository', []))
        
        # Cross-pattern analysis
        self._analyze_cross_pattern_opportunities(by_pattern)
        
        # Anti-pattern detection
        self._detect_architectural_anti_patterns(all_opportunities)
        
        # Complexity assessment
        self._assess_overall_complexity(all_opportunities)
    
    def _analyze_singleton_usage(self, singleton_opportunities: List[PatternOpportunity]) -> None:
        """Analyze singleton pattern usage across the repository"""
        if not singleton_opportunities:
            return
        
        anti_patterns = [opp for opp in singleton_opportunities 
                        if opp.opportunity_type == OpportunityType.ANTI_PATTERN_DETECTED]
        valid_opportunities = [opp for opp in singleton_opportunities 
                              if opp.opportunity_type != OpportunityType.ANTI_PATTERN_DETECTED]
        
        # Check for singleton overuse
        if len(anti_patterns) >= 2:
            self.architectural_insights.append(ArchitecturalInsight(
                insight_type="anti_pattern",
                title="Singleton Pattern Overuse Detected",
                description=f"Found {len(anti_patterns)} inappropriate singleton implementations. "
                           "Singletons should not be used for data models or entity classes.",
                affected_files=[opp.file_path for opp in anti_patterns],
                confidence=PatternConfidence.HIGH,
                impact="High",
                effort="Medium",
                recommendations=[
                    "Convert data model singletons to regular classes",
                    "Use dependency injection for better testability",
                    "Consider Repository pattern for data access centralization",
                    "Review singleton usage - ensure they're truly needed"
                ]
            ))
        
        # Check for missing singleton opportunities
        if len(valid_opportunities) >= 2:
            config_files = [opp.file_path for opp in valid_opportunities 
                           if 'config' in opp.file_path.lower()]
            db_files = [opp.file_path for opp in valid_opportunities 
                       if any(keyword in opp.file_path.lower() 
                             for keyword in ['database', 'connection', 'db'])]
            
            if config_files or db_files:
                self.architectural_insights.append(ArchitecturalInsight(
                    insight_type="optimization",
                    title="Centralize Shared Resources with Singleton",
                    description="Multiple configuration or database connection classes could benefit from singleton pattern.",
                    affected_files=config_files + db_files,
                    confidence=PatternConfidence.MEDIUM,
                    impact="Medium",
                    effort="Low",
                    recommendations=[
                        "Implement singleton for configuration management",
                        "Centralize database connections with singleton pattern",
                        "Ensure thread-safety for multi-threaded applications",
                        "Consider lazy initialization for performance"
                    ]
                ))
    
    def _analyze_factory_opportunities(self, factory_opportunities: List[PatternOpportunity]) -> None:
        """Analyze factory pattern opportunities"""
        if len(factory_opportunities) >= 3:
            # Multiple factory opportunities suggest need for consistent creation strategy
            self.architectural_insights.append(ArchitecturalInsight(
                insight_type="architectural_pattern",
                title="Standardize Object Creation with Factory Pattern",
                description=f"Found {len(factory_opportunities)} factory pattern opportunities. "
                           "Consider implementing a consistent object creation strategy.",
                affected_files=[opp.file_path for opp in factory_opportunities],
                confidence=PatternConfidence.MEDIUM,
                impact="Medium",
                effort="Medium",
                recommendations=[
                    "Implement factory methods for complex object creation",
                    "Consider Abstract Factory for families of related objects",
                    "Centralize creation logic to improve maintainability",
                    "Use factories to support polymorphism and extensibility"
                ]
            ))
    
    def _analyze_observer_opportunities(self, observer_opportunities: List[PatternOpportunity]) -> None:
        """Analyze observer pattern opportunities"""
        if len(observer_opportunities) >= 2:
            # Multiple observer opportunities suggest event-driven architecture
            self.architectural_insights.append(ArchitecturalInsight(
                insight_type="architectural_pattern",
                title="Implement Event-Driven Architecture",
                description=f"Found {len(observer_opportunities)} observer pattern opportunities. "
                           "Consider implementing a centralized event system.",
                affected_files=[opp.file_path for opp in observer_opportunities],
                confidence=PatternConfidence.MEDIUM,
                impact="High",
                effort="Medium",
                recommendations=[
                    "Implement centralized event bus or observer registry",
                    "Define clear event contracts and interfaces",
                    "Consider async event handling for performance",
                    "Implement proper error handling in event notifications"
                ]
            ))
    
    def _analyze_strategy_opportunities(self, strategy_opportunities: List[PatternOpportunity]) -> None:
        """Analyze strategy pattern opportunities"""
        if len(strategy_opportunities) >= 3:
            # Multiple strategy opportunities suggest algorithmic complexity
            self.architectural_insights.append(ArchitecturalInsight(
                insight_type="complexity_reduction",
                title="Reduce Complexity with Strategy Pattern",
                description=f"Found {len(strategy_opportunities)} strategy pattern opportunities. "
                           "Multiple conditional chains suggest high algorithmic complexity.",
                affected_files=[opp.file_path for opp in strategy_opportunities],
                confidence=PatternConfidence.HIGH,
                impact="Medium",
                effort="Medium",
                recommendations=[
                    "Replace complex conditional logic with strategy patterns",
                    "Create strategy interfaces for algorithm families",
                    "Implement strategy selection mechanisms",
                    "Consider configuration-driven strategy selection"
                ]
            ))
    
    def _analyze_builder_opportunities(self, builder_opportunities: List[PatternOpportunity]) -> None:
        """Analyze builder pattern opportunities"""
        if len(builder_opportunities) >= 2:
            # Multiple builder opportunities suggest complex object construction
            self.architectural_insights.append(ArchitecturalInsight(
                insight_type="optimization",
                title="Simplify Object Construction with Builder Pattern",
                description=f"Found {len(builder_opportunities)} builder pattern opportunities. "
                           "Complex constructors suggest need for builder pattern.",
                affected_files=[opp.file_path for opp in builder_opportunities],
                confidence=PatternConfidence.MEDIUM,
                impact="Medium",
                effort="Low",
                recommendations=[
                    "Implement builder pattern for complex object construction",
                    "Use fluent interfaces for better readability",
                    "Add validation at each construction step",
                    "Consider immutable objects with builders"
                ]
            ))
    
    def _analyze_repository_opportunities(self, repo_opportunities: List[PatternOpportunity]) -> None:
        """Analyze repository pattern opportunities"""
        if repo_opportunities:
            # Repository opportunities suggest data access concerns
            self.architectural_insights.append(ArchitecturalInsight(
                insight_type="architectural_pattern",
                title="Centralize Data Access with Repository Pattern",
                description="Data access logic could benefit from repository pattern implementation.",
                affected_files=[opp.file_path for opp in repo_opportunities],
                confidence=PatternConfidence.MEDIUM,
                impact="High",
                effort="High",
                recommendations=[
                    "Implement repository interfaces for data access",
                    "Separate domain logic from data access logic",
                    "Consider Unit of Work pattern for transaction management",
                    "Implement repository abstractions for testing"
                ]
            ))
    
    def _analyze_cross_pattern_opportunities(self, by_pattern: Dict[str, List[PatternOpportunity]]) -> None:
        """Analyze opportunities for combining multiple patterns"""
        
        # Factory + Strategy combination
        if 'factory' in by_pattern and 'strategy' in by_pattern:
            if len(by_pattern['factory']) >= 1 and len(by_pattern['strategy']) >= 1:
                self.architectural_insights.append(ArchitecturalInsight(
                    insight_type="architectural_pattern",
                    title="Combine Factory and Strategy Patterns",
                    description="Factory and Strategy opportunities detected. Consider creating strategies through factories.",
                    affected_files=list(set([opp.file_path for opp in by_pattern['factory']] + 
                                          [opp.file_path for opp in by_pattern['strategy']])),
                    confidence=PatternConfidence.LOW,
                    impact="Medium",
                    effort="Medium",
                    recommendations=[
                        "Use Factory pattern to create Strategy instances",
                        "Implement strategy registry for dynamic selection",
                        "Consider configuration-driven strategy creation"
                    ]
                ))
        
        # Observer + Command combination
        if 'observer' in by_pattern and 'command' in by_pattern:
            if len(by_pattern['observer']) >= 1 and len(by_pattern['command']) >= 1:
                self.architectural_insights.append(ArchitecturalInsight(
                    insight_type="architectural_pattern",
                    title="Event Sourcing Architecture Opportunity",
                    description="Observer and Command patterns together suggest event sourcing possibilities.",
                    affected_files=list(set([opp.file_path for opp in by_pattern['observer']] + 
                                          [opp.file_path for opp in by_pattern['command']])),
                    confidence=PatternConfidence.LOW,
                    impact="High",
                    effort="High",
                    recommendations=[
                        "Consider implementing event sourcing architecture",
                        "Use Command pattern for event creation",
                        "Use Observer pattern for event handling",
                        "Implement event store for audit and replay capabilities"
                    ]
                ))
    
    def _detect_architectural_anti_patterns(self, all_opportunities: List[PatternOpportunity]) -> None:
        """Detect architectural-level anti-patterns"""
        
        # Check for pattern overuse
        pattern_counts = defaultdict(int)
        for opp in all_opportunities:
            pattern_counts[opp.pattern_name] += 1
        
        high_pattern_usage = {pattern: count for pattern, count in pattern_counts.items() 
                             if count >= 5}
        
        if high_pattern_usage:
            patterns_list = ", ".join(f"{pattern} ({count})" for pattern, count in high_pattern_usage.items())
            self.architectural_insights.append(ArchitecturalInsight(
                insight_type="anti_pattern",
                title="Potential Pattern Overuse",
                description=f"High number of pattern opportunities detected: {patterns_list}. "
                           "Consider if simpler solutions might be more appropriate.",
                affected_files=[],
                confidence=PatternConfidence.LOW,
                impact="Medium",
                effort="Low",
                recommendations=[
                    "Review each pattern opportunity carefully",
                    "Consider simpler alternatives where appropriate",
                    "Ensure patterns solve real problems, not imaginary ones",
                    "Follow YAGNI (You Aren't Gonna Need It) principle"
                ]
            ))
        
        # Check for complexity overload
        total_opportunities = len(all_opportunities)
        if total_opportunities >= 20:
            self.architectural_insights.append(ArchitecturalInsight(
                insight_type="anti_pattern",
                title="High Complexity Warning",
                description=f"Found {total_opportunities} pattern opportunities. "
                           "High pattern density might indicate over-engineering.",
                affected_files=[],
                confidence=PatternConfidence.MEDIUM,
                impact="High",
                effort="Low",
                recommendations=[
                    "Prioritize high-impact, low-effort improvements",
                    "Focus on anti-pattern elimination first",
                    "Consider architectural simplification",
                    "Implement patterns incrementally, not all at once"
                ]
            ))
    
    def _assess_overall_complexity(self, all_opportunities: List[PatternOpportunity]) -> None:
        """Assess overall codebase complexity based on pattern opportunities"""
        
        total_opportunities = len(all_opportunities)
        anti_patterns = len([opp for opp in all_opportunities 
                           if opp.opportunity_type == OpportunityType.ANTI_PATTERN_DETECTED])
        high_confidence = len([opp for opp in all_opportunities 
                             if opp.confidence in [PatternConfidence.HIGH, PatternConfidence.CRITICAL]])
        
        # Generate complexity assessment
        if anti_patterns > 0:
            complexity_level = "High (Anti-patterns detected)"
            primary_recommendation = "Focus on eliminating anti-patterns first"
        elif high_confidence >= 5:
            complexity_level = "Medium-High (Multiple clear improvement opportunities)"
            primary_recommendation = "Implement high-confidence patterns for immediate benefits"
        elif total_opportunities >= 10:
            complexity_level = "Medium (Multiple opportunities available)"
            primary_recommendation = "Prioritize patterns by business value and technical debt reduction"
        elif total_opportunities >= 5:
            complexity_level = "Low-Medium (Some improvement opportunities)"
            primary_recommendation = "Selective pattern implementation based on team capacity"
        else:
            complexity_level = "Low (Well-structured codebase)"
            primary_recommendation = "Maintain current good practices"
        
        # Add complexity insight
        self.architectural_insights.append(ArchitecturalInsight(
            insight_type="assessment",
            title="Codebase Complexity Assessment",
            description=f"Complexity Level: {complexity_level}",
            affected_files=[],
            confidence=PatternConfidence.HIGH,
            impact="Critical",
            effort="N/A",
            recommendations=[primary_recommendation]
        ))
    
    def _create_analysis_summary(self) -> RepositoryAnalysis:
        """Create comprehensive analysis summary"""
        
        all_opportunities = []
        for opportunities in self.opportunities_by_file.values():
            all_opportunities.extend(opportunities)
        
        # Pattern usage summary
        pattern_counts = defaultdict(int)
        for opp in all_opportunities:
            pattern_counts[opp.pattern_name] += 1
        
        # Top recommendations
        top_insights = sorted(self.architectural_insights, 
                            key=lambda x: x.priority_score, reverse=True)[:5]
        
        recommendations_summary = []
        for insight in top_insights:
            recommendations_summary.extend(insight.recommendations[:2])  # Top 2 from each
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations_summary:
            if rec not in seen:
                seen.add(rec)
                unique_recommendations.append(rec)
        
        return RepositoryAnalysis(
            repository_path=str(self.repository_path),
            total_files_analyzed=len(self.opportunities_by_file),
            total_opportunities=len(all_opportunities),
            opportunities_by_file=self.opportunities_by_file,
            architectural_insights=self.architectural_insights,
            pattern_usage_summary=dict(pattern_counts),
            complexity_assessment=next((insight.description for insight in self.architectural_insights 
                                      if insight.title == "Codebase Complexity Assessment"), "Unknown"),
            recommendations_summary=unique_recommendations[:10]  # Top 10 recommendations
        )
    
    def save_analysis(self, analysis: RepositoryAnalysis, output_path: Union[str, Path]) -> None:
        """Save analysis results to JSON file"""
        output_path = Path(output_path)
        
        # Convert to serializable format
        analysis_dict = asdict(analysis)
        
        # Convert PatternOpportunity objects to dictionaries
        for file_path, opportunities in analysis_dict['opportunities_by_file'].items():
            analysis_dict['opportunities_by_file'][file_path] = [
                asdict(opp) for opp in opportunities
            ]
        
        # Convert ArchitecturalInsight confidence enums to strings
        for insight in analysis_dict['architectural_insights']:
            insight['confidence'] = insight['confidence'].value
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_dict, f, indent=2, ensure_ascii=False)
    
    def generate_report(self, analysis: RepositoryAnalysis) -> str:
        """Generate comprehensive human-readable report"""
        
        report = f"# Repository Pattern Analysis Report\n\n"
        report += f"**Repository**: {analysis.repository_path}\n"
        report += f"**Files Analyzed**: {analysis.total_files_analyzed}\n"
        report += f"**Total Opportunities**: {analysis.total_opportunities}\n"
        report += f"**Complexity**: {analysis.complexity_assessment}\n\n"
        
        if not analysis.total_opportunities:
            report += "🎉 **Excellent!** No pattern opportunities detected. Your codebase appears well-structured.\n\n"
            return report
        
        # Pattern summary
        report += "## Pattern Opportunity Summary\n\n"
        for pattern, count in sorted(analysis.pattern_usage_summary.items(), 
                                   key=lambda x: x[1], reverse=True):
            report += f"- **{pattern.title()}**: {count} opportunities\n"
        
        # Top architectural insights
        report += "\n## Key Architectural Insights\n\n"
        top_insights = sorted(analysis.architectural_insights, 
                            key=lambda x: x.priority_score, reverse=True)[:5]
        
        for i, insight in enumerate(top_insights, 1):
            report += f"### {i}. {insight.title}\n"
            report += f"**Type**: {insight.insight_type.replace('_', ' ').title()}\n"
            report += f"**Impact**: {insight.impact} | **Effort**: {insight.effort}\n"
            report += f"**Description**: {insight.description}\n"
            if insight.affected_files:
                report += f"**Affected Files**: {len(insight.affected_files)} files\n"
            report += "**Recommendations**:\n"
            for rec in insight.recommendations[:3]:  # Top 3 recommendations
                report += f"- {rec}\n"
            report += "\n"
        
        # Priority recommendations
        report += "## Priority Action Items\n\n"
        for i, rec in enumerate(analysis.recommendations_summary[:8], 1):
            report += f"{i}. {rec}\n"
        
        # High-priority file-level opportunities
        report += "\n## High-Priority File Opportunities\n\n"
        all_opportunities = []
        for opportunities in analysis.opportunities_by_file.values():
            all_opportunities.extend(opportunities)
        
        high_priority = sorted([opp for opp in all_opportunities if opp.priority_score > 0.7], 
                              key=lambda x: x.priority_score, reverse=True)[:8]
        
        for opp in high_priority:
            report += f"**{opp.pattern_name.title()}** in `{Path(opp.file_path).name}:{opp.line_number}`\n"
            report += f"- {opp.description}\n"
            report += f"- Effort: {opp.effort_estimate} | Impact: {opp.impact_estimate}\n\n"
        
        return report


def analyze_repository(repository_path: Union[str, Path], 
                      exclude_patterns: Optional[List[str]] = None,
                      save_to: Optional[Union[str, Path]] = None) -> RepositoryAnalysis:
    """
    Comprehensive repository analysis with optional save functionality
    
    Args:
        repository_path: Path to the repository to analyze
        exclude_patterns: Additional patterns to exclude from analysis
        save_to: Optional path to save JSON analysis results
        
    Returns:
        RepositoryAnalysis object with complete analysis results
    """
    analyzer = RepositoryAnalyzer(repository_path)
    analysis = analyzer.analyze(exclude_patterns)
    
    if save_to:
        analyzer.save_analysis(analysis, save_to)
    
    return analysis