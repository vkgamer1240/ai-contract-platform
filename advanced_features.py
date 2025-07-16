"""
Advanced Features for Enhanced Contract Analysis
===============================================
Additional capabilities for batch processing, contract comparison, and advanced risk metrics
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Tuple
import pandas as pd
from enhanced_analyzer import EnhancedCUADAnalyzer

class AdvancedContractProcessor:
    def __init__(self, analyzer: EnhancedCUADAnalyzer):
        self.analyzer = analyzer
        self.analysis_history = []
        
    def batch_analyze_contracts(self, contracts: List[Dict[str, str]]) -> Dict:
        """
        Analyze multiple contracts in batch
        contracts: List of dicts with 'name' and 'text' keys
        """
        results = {
            "batch_summary": {
                "total_contracts": len(contracts),
                "analysis_date": datetime.now().isoformat(),
                "high_risk_count": 0,
                "medium_risk_count": 0,
                "low_risk_count": 0
            },
            "individual_results": [],
            "comparative_analysis": {}
        }
        
        all_risks = []
        contract_types = {}
        
        for i, contract in enumerate(contracts):
            print(f"Analyzing contract {i+1}/{len(contracts)}: {contract['name']}")
            
            # Comprehensive analysis
            analysis = self.analyzer.analyze_contract_comprehensive(contract['text'])
            
            # Add to results
            contract_result = {
                "name": contract['name'],
                "analysis": analysis,
                "risk_level": self._categorize_risk_level(analysis.get('risk_assessment', {}).get('risk_score', 0))
            }
            
            results["individual_results"].append(contract_result)
            
            # Track for summary
            risk_level = contract_result['risk_level']
            if risk_level == "High":
                results["batch_summary"]["high_risk_count"] += 1
            elif risk_level == "Medium":
                results["batch_summary"]["medium_risk_count"] += 1
            else:
                results["batch_summary"]["low_risk_count"] += 1
            
            # Collect data for comparative analysis
            contract_type = analysis.get('contract_type', 'unknown')
            if contract_type not in contract_types:
                contract_types[contract_type] = []
            contract_types[contract_type].append(contract_result)
            
            all_risks.extend(analysis.get('risk_assessment', {}).get('high_risk', []))
        
        # Comparative analysis
        results["comparative_analysis"] = {
            "contract_types": contract_types,
            "common_risks": self._find_common_risks(all_risks),
            "risk_distribution": {
                "high": results["batch_summary"]["high_risk_count"],
                "medium": results["batch_summary"]["medium_risk_count"],
                "low": results["batch_summary"]["low_risk_count"]
            }
        }
        
        return results
    
    def compare_contracts(self, contract1: str, contract2: str, names: Tuple[str, str] = ("Contract A", "Contract B")) -> Dict:
        """Compare two contracts side by side"""
        print(f"Comparing {names[0]} vs {names[1]}")
        
        # Analyze both contracts
        analysis1 = self.analyzer.analyze_contract_comprehensive(contract1)
        analysis2 = self.analyzer.analyze_contract_comprehensive(contract2)
        
        comparison = {
            "contracts": {
                names[0]: analysis1,
                names[1]: analysis2
            },
            "comparison_summary": {
                "risk_comparison": self._compare_risks(analysis1, analysis2),
                "term_comparison": self._compare_terms(analysis1, analysis2),
                "recommendations": self._generate_comparison_recommendations(analysis1, analysis2, names)
            }
        }
        
        return comparison
    
    def analyze_app_store_compliance(self, contract_text: str, platform: str = "both") -> Dict:
        """
        Analyze app agreement for App Store/Play Store compliance
        platform: "ios", "android", or "both"
        """
        compliance_checks = {
            "ios": {
                "required_clauses": [
                    "App Store Review Guidelines compliance",
                    "Apple Developer Program License Agreement reference",
                    "In-app purchase terms",
                    "Content filtering policies",
                    "Privacy policy link"
                ],
                "prohibited_content": [
                    "External payment links",
                    "Alternative app store references",
                    "Cryptocurrency mining",
                    "Adult content without restrictions"
                ]
            },
            "android": {
                "required_clauses": [
                    "Google Play Developer Policy compliance",
                    "Google Play Billing integration",
                    "Target API level compliance",
                    "Data safety declarations",
                    "Family-friendly content ratings"
                ],
                "prohibited_content": [
                    "Malicious software references",
                    "Unauthorized payment systems",
                    "Misleading content policies",
                    "Inappropriate content for minors"
                ]
            }
        }
        
        results = {
            "platform_analysis": {},
            "compliance_score": 0,
            "recommendations": [],
            "risk_areas": []
        }
        
        platforms_to_check = ["ios", "android"] if platform == "both" else [platform]
        
        for p in platforms_to_check:
            platform_result = self._check_platform_compliance(contract_text, compliance_checks[p])
            results["platform_analysis"][p] = platform_result
        
        # Overall compliance score
        total_score = sum(r["compliance_score"] for r in results["platform_analysis"].values())
        results["compliance_score"] = total_score / len(platforms_to_check)
        
        # Generate recommendations
        results["recommendations"] = self._generate_compliance_recommendations(results["platform_analysis"])
        
        return results
    
    def generate_contract_report(self, analysis_results: Dict, contract_name: str = "Contract") -> str:
        """Generate a comprehensive report in markdown format"""
        report = f"""# Contract Analysis Report: {contract_name}
**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
**Contract Type:** {analysis_results.get('contract_type', 'Unknown')}
**Risk Level:** {self._categorize_risk_level(analysis_results.get('risk_assessment', {}).get('risk_score', 0))}
**Overall Risk Score:** {analysis_results.get('risk_assessment', {}).get('risk_score', 0)}/100

## Key Findings

### High-Risk Issues
"""
        
        high_risks = analysis_results.get('risk_assessment', {}).get('high_risk', [])
        if high_risks:
            for risk in high_risks:
                report += f"- ⚠️ {risk}\n"
        else:
            report += "- ✅ No high-risk issues identified\n"
        
        report += "\n### Medium-Risk Issues\n"
        medium_risks = analysis_results.get('risk_assessment', {}).get('medium_risk', [])
        if medium_risks:
            for risk in medium_risks:
                report += f"- ⚡ {risk}\n"
        else:
            report += "- ✅ No medium-risk issues identified\n"
        
        report += "\n### Red Flags\n"
        red_flags = analysis_results.get('risk_assessment', {}).get('red_flags', [])
        if red_flags:
            for flag in red_flags:
                report += f"- 🚩 {flag}\n"
        else:
            report += "- ✅ No red flags identified\n"
        
        # Add CUAD analysis results
        report += "\n## Detailed Analysis\n"
        cuad_results = analysis_results.get('cuad_analysis', {})
        for category, result in cuad_results.items():
            if result.get('answer') and result.get('answer') != 'No answer found.':
                report += f"\n### {category.replace('_', ' ').title()}\n"
                report += f"**Answer:** {result['answer']}\n"
                report += f"**Confidence:** {result['confidence']:.2f}\n"
        
        # Add Groq analysis if available
        groq_analysis = analysis_results.get('groq_analysis', {})
        if groq_analysis and 'analysis' in groq_analysis:
            report += f"\n## AI Legal Analysis\n{groq_analysis['analysis']}\n"
        
        # Add recommendations
        recommendations = analysis_results.get('recommendations', [])
        if recommendations:
            report += "\n## Recommendations\n"
            for i, rec in enumerate(recommendations, 1):
                report += f"{i}. {rec}\n"
        
        return report
    
    def _categorize_risk_level(self, risk_score: int) -> str:
        """Categorize risk based on score"""
        if risk_score >= 70:
            return "High"
        elif risk_score >= 40:
            return "Medium"
        else:
            return "Low"
    
    def _find_common_risks(self, all_risks: List[str]) -> Dict:
        """Find common risks across multiple contracts"""
        risk_counts = {}
        for risk in all_risks:
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        # Sort by frequency
        return dict(sorted(risk_counts.items(), key=lambda x: x[1], reverse=True))
    
    def _compare_risks(self, analysis1: Dict, analysis2: Dict) -> Dict:
        """Compare risk assessments between two contracts"""
        risk1 = analysis1.get('risk_assessment', {})
        risk2 = analysis2.get('risk_assessment', {})
        
        return {
            "risk_scores": {
                "contract_1": risk1.get('risk_score', 0),
                "contract_2": risk2.get('risk_score', 0),
                "difference": abs(risk1.get('risk_score', 0) - risk2.get('risk_score', 0))
            },
            "unique_risks_contract_1": list(set(risk1.get('high_risk', [])) - set(risk2.get('high_risk', []))),
            "unique_risks_contract_2": list(set(risk2.get('high_risk', [])) - set(risk1.get('high_risk', []))),
            "common_risks": list(set(risk1.get('high_risk', [])) & set(risk2.get('high_risk', [])))
        }
    
    def _compare_terms(self, analysis1: Dict, analysis2: Dict) -> Dict:
        """Compare specific terms between contracts"""
        cuad1 = analysis1.get('cuad_analysis', {})
        cuad2 = analysis2.get('cuad_analysis', {})
        
        term_comparison = {}
        all_categories = set(cuad1.keys()) | set(cuad2.keys())
        
        for category in all_categories:
            term1 = cuad1.get(category, {}).get('answer', 'Not found')
            term2 = cuad2.get(category, {}).get('answer', 'Not found')
            
            term_comparison[category] = {
                "contract_1": term1,
                "contract_2": term2,
                "different": term1 != term2
            }
        
        return term_comparison
    
    def _generate_comparison_recommendations(self, analysis1: Dict, analysis2: Dict, names: Tuple[str, str]) -> List[str]:
        """Generate recommendations based on contract comparison"""
        recommendations = []
        
        risk1 = analysis1.get('risk_assessment', {}).get('risk_score', 0)
        risk2 = analysis2.get('risk_assessment', {}).get('risk_score', 0)
        
        if risk1 < risk2:
            recommendations.append(f"Consider using {names[0]} as it has lower risk (score: {risk1} vs {risk2})")
        elif risk2 < risk1:
            recommendations.append(f"Consider using {names[1]} as it has lower risk (score: {risk2} vs {risk1})")
        
        # Check for specific advantageous terms
        cuad1 = analysis1.get('cuad_analysis', {})
        cuad2 = analysis2.get('cuad_analysis', {})
        
        if cuad1.get('termination', {}).get('confidence', 0) > cuad2.get('termination', {}).get('confidence', 0):
            recommendations.append(f"{names[0]} has clearer termination terms")
        
        if cuad1.get('liability', {}).get('confidence', 0) > cuad2.get('liability', {}).get('confidence', 0):
            recommendations.append(f"{names[0]} has better defined liability terms")
        
        return recommendations
    
    def _check_platform_compliance(self, contract_text: str, compliance_rules: Dict) -> Dict:
        """Check compliance with platform-specific rules"""
        text_lower = contract_text.lower()
        
        required_found = 0
        prohibited_found = 0
        
        # Check required clauses
        for clause in compliance_rules["required_clauses"]:
            if any(word in text_lower for word in clause.lower().split()):
                required_found += 1
        
        # Check for prohibited content
        for content in compliance_rules["prohibited_content"]:
            if any(word in text_lower for word in content.lower().split()):
                prohibited_found += 1
        
        compliance_score = (required_found / len(compliance_rules["required_clauses"])) * 100
        if prohibited_found > 0:
            compliance_score -= (prohibited_found * 10)  # Penalty for prohibited content
        
        return {
            "compliance_score": max(0, compliance_score),
            "required_found": required_found,
            "required_total": len(compliance_rules["required_clauses"]),
            "prohibited_found": prohibited_found,
            "issues": self._identify_compliance_issues(contract_text, compliance_rules)
        }
    
    def _identify_compliance_issues(self, contract_text: str, compliance_rules: Dict) -> List[str]:
        """Identify specific compliance issues with improved accuracy"""
        issues = []
        text_lower = contract_text.lower()
        
        # Check missing required clauses with better matching
        for clause in compliance_rules["required_clauses"]:
            clause_keywords = clause.lower().split()
            # Require at least 2 keywords to match for better accuracy
            keyword_matches = sum(1 for keyword in clause_keywords if keyword in text_lower)
            match_ratio = keyword_matches / len(clause_keywords)
            
            if match_ratio < 0.5:  # Less than 50% of keywords found
                issues.append(f"Missing required clause: {clause}")
        
        # Check for prohibited content with stricter matching
        prohibited_patterns = {
            "External payment links": ["external", "payment", "link"],
            "Alternative app store references": ["alternative", "store", "sideload"],
            "Adult content without restrictions": ["adult", "mature", "18+", "nsfw"],
            "Misleading content policies": ["misleading", "false", "deceptive", "no refund"],
            "Inappropriate content for minors": ["minor", "child", "age restriction"]
        }
        
        for content in compliance_rules["prohibited_content"]:
            if content in prohibited_patterns:
                pattern_words = prohibited_patterns[content]
                matches = sum(1 for word in pattern_words if word in text_lower)
                if matches >= 2:  # Require at least 2 related words
                    issues.append(f"Contains prohibited content: {content}")
            else:
                # Fallback to old method for unlisted patterns
                if any(word in text_lower for word in content.lower().split()):
                    issues.append(f"Contains prohibited content: {content}")
        
        return issues
    
    def _generate_compliance_recommendations(self, platform_analysis: Dict) -> List[str]:
        """Generate platform compliance recommendations"""
        recommendations = []
        
        for platform, analysis in platform_analysis.items():
            score = analysis["compliance_score"]
            if score < 70:
                recommendations.append(f"Improve {platform.upper()} compliance (current score: {score:.1f}%)")
            
            for issue in analysis["issues"]:
                recommendations.append(f"{platform.upper()}: {issue}")
        
        return recommendations

def create_sample_app_agreements():
    """Create sample app agreements for testing"""
    return {
        "mobile_game_tos": """
        MOBILE GAME TERMS OF SERVICE
        
        1. ACCEPTANCE OF TERMS
        By downloading, installing, or using GameApp, you agree to these Terms of Service.
        
        2. GAME CONTENT AND VIRTUAL ITEMS
        The game includes virtual currency and items that can be purchased with real money.
        All virtual items are owned by the Company and licensed to you for use.
        
        3. DATA COLLECTION
        We collect device information, gameplay data, and may access your camera and contacts.
        Data is shared with third-party analytics and advertising partners.
        
        4. SUBSCRIPTION SERVICES
        Premium subscriptions auto-renew monthly at $9.99 unless cancelled 24 hours before renewal.
        Refunds are not provided for unused subscription periods.
        
        5. USER CONTENT
        You grant us a perpetual, worldwide license to use any content you create in the game.
        We may monetize, modify, and distribute your content without compensation.
        
        6. LIABILITY
        Company is not liable for any damages, including data loss or device damage.
        Maximum liability is limited to $50 regardless of circumstances.
        
        7. GOVERNING LAW
        This agreement is governed by laws of Delaware, USA.
        Disputes must be resolved through binding arbitration.
        """,
        
        "social_media_privacy": """
        SOCIAL MEDIA APP PRIVACY POLICY
        
        1. INFORMATION WE COLLECT
        We collect personal information, photos, contacts, location data, and device identifiers.
        We track your activity across other apps and websites.
        
        2. HOW WE USE YOUR INFORMATION
        Your data is used for personalized advertising, content recommendations, and analytics.
        We may sell anonymized data to third parties for research purposes.
        
        3. DATA SHARING
        We share your information with advertising partners, analytics providers, and government agencies when required.
        Your posts may be used in our marketing materials without compensation.
        
        4. DATA RETENTION
        We retain your data indefinitely, even after account deletion.
        Some data may be stored on servers outside your country.
        
        5. YOUR RIGHTS
        You may request data deletion, but some information may remain in backups.
        You cannot opt out of essential data collection for app functionality.
        
        6. CHILDREN'S PRIVACY
        We do not knowingly collect data from children under 13, but age verification is limited.
        
        7. UPDATES
        We may update this policy at any time without notice.
        Continued use constitutes acceptance of changes.
        """,
        
        "saas_agreement": """
        SOFTWARE AS A SERVICE AGREEMENT
        
        1. SERVICE DESCRIPTION
        CompanyCloud provides web-based project management software accessible via subscription.
        
        2. SUBSCRIPTION TERMS
        Monthly subscription fee is $49 per user, billed annually in advance.
        Service levels are not guaranteed and may vary based on usage.
        
        3. DATA OWNERSHIP
        Customer retains ownership of their data, but grants us broad license to process and analyze.
        We may use aggregated data for product improvement and benchmarking.
        
        4. TERMINATION
        Either party may terminate with 30 days notice.
        Upon termination, data will be deleted after 30 days with no recovery option.
        
        5. LIABILITY AND WARRANTIES
        Service is provided "as is" without warranties.
        Our liability is limited to one month's subscription fees.
        Customer is responsible for data backup and security.
        
        6. INTELLECTUAL PROPERTY
        Customer grants us license to their data for service provision.
        We retain all rights to the software and any improvements.
        
        7. COMPLIANCE
        Customer is responsible for compliance with applicable laws and regulations.
        We may suspend service if we suspect non-compliance.
        """
    }

if __name__ == "__main__":
    # Example usage
    print("Advanced Contract Processing Features")
    print("====================================")
    
    # Initialize
    from enhanced_analyzer import EnhancedCUADAnalyzer
    analyzer = EnhancedCUADAnalyzer('./')
    processor = AdvancedContractProcessor(analyzer)
    
    # Test with sample agreements
    samples = create_sample_app_agreements()
    
    # Convert to list format for batch processing
    contracts = [
        {"name": "Mobile Game ToS", "text": samples["mobile_game_tos"]},
        {"name": "Social Media Privacy", "text": samples["social_media_privacy"]},
        {"name": "SaaS Agreement", "text": samples["saas_agreement"]}
    ]
    
    print("\n1. Batch Analysis")
    batch_results = processor.batch_analyze_contracts(contracts)
    print(f"Analyzed {batch_results['batch_summary']['total_contracts']} contracts")
    print(f"High risk: {batch_results['batch_summary']['high_risk_count']}")
    print(f"Medium risk: {batch_results['batch_summary']['medium_risk_count']}")
    print(f"Low risk: {batch_results['batch_summary']['low_risk_count']}")
    
    print("\n2. Contract Comparison")
    comparison = processor.compare_contracts(
        samples["mobile_game_tos"],
        samples["social_media_privacy"],
        ("Game ToS", "Social Media Privacy")
    )
    print("Comparison completed - check results for detailed analysis")
    
    print("\n3. App Store Compliance Check")
    compliance = processor.analyze_app_store_compliance(samples["mobile_game_tos"])
    print(f"iOS compliance score: {compliance['platform_analysis'].get('ios', {}).get('compliance_score', 0):.1f}%")
    print(f"Android compliance score: {compliance['platform_analysis'].get('android', {}).get('compliance_score', 0):.1f}%")
