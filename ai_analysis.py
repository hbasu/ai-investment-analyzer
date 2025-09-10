import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
except Exception:
    pass

import json
import os
import logging
import unicodedata
from openai import OpenAI

# Configure Unicode-safe logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def sanitize_text(s):
    """Convert Unicode text to ASCII-safe text"""
    if not s:
        return ""
    
    # Normalize Unicode
    s = unicodedata.normalize('NFKC', str(s))
    
    # Replace common Unicode punctuation with ASCII equivalents
    replacements = {
        '\u2014': '-',  # em dash
        '\u2013': '-',  # en dash
        '\u2018': "'",  # left single quote
        '\u2019': "'",  # right single quote
        '\u201C': '"',  # left double quote
        '\u201D': '"',  # right double quote
        '\u2026': '...',  # ellipsis
        '\u00A0': ' ',  # non-breaking space
    }
    
    for unicode_char, ascii_char in replacements.items():
        s = s.replace(unicode_char, ascii_char)
    
    # Final guard: encode as ASCII with backslash replacement
    return s.encode('ascii', 'backslashreplace').decode('ascii')

def safe_log(msg):
    """Log messages safely without Unicode errors"""
    try:
        sanitized_msg = sanitize_text(msg)
        logger.info(sanitized_msg)
    except UnicodeEncodeError:
        logger.info(str(msg).encode('ascii', 'backslashreplace').decode('ascii'))

class AIAnalyzer:
    """Class to perform AI-powered analysis of companies for AI investment potential"""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
        # do not change this unless explicitly requested by the user
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        
        # Validate API key for Unicode characters that break HTTP headers
        try:
            api_key.encode('ascii')
        except UnicodeEncodeError as e:
            safe_log(f"OPENAI_API_KEY contains non-ASCII characters at position {e.start}")
            if '\u2014' in api_key or '\u2013' in api_key:
                raise RuntimeError(
                    "OPENAI_API_KEY contains em-dash or en-dash characters that break HTTP headers. "
                    "Please reset your OPENAI_API_KEY with a clean ASCII key (avoid copying from "
                    "documents with smart punctuation)."
                )
            else:
                raise RuntimeError(
                    f"OPENAI_API_KEY contains non-ASCII characters that break HTTP headers. "
                    f"Please reset your OPENAI_API_KEY with a clean ASCII key."
                )
        
        self.openai_client = OpenAI(api_key=api_key)
        self.model = "gpt-5"
    
    def analyze_ai_potential(self, symbol, company_info):
        """
        Analyze a company's AI investment potential using OpenAI
        
        Args:
            symbol (str): Stock ticker symbol
            company_info (dict): Company information from yfinance
            
        Returns:
            dict: Comprehensive AI analysis results
        """
        try:
            safe_log(f"=== DEBUG: Starting AI analysis for {symbol} ===")
            
            # Prepare company context
            company_context = self._prepare_company_context(symbol, company_info)
            safe_log(f"DEBUG: Company context prepared for {company_context.get('name', 'Unknown')}")
            
            # Get AI strategy analysis
            safe_log("DEBUG: About to call _analyze_ai_strategy...")
            ai_strategy_analysis = self._analyze_ai_strategy(company_context)
            safe_log(f"DEBUG: AI strategy analysis returned: {ai_strategy_analysis}")
            
            # Get investment recommendation
            investment_recommendation = self._get_investment_recommendation(company_context, ai_strategy_analysis)
            
            # Calculate AI metrics
            ai_metrics = self._calculate_ai_metrics(company_context, ai_strategy_analysis)
            
            # Generate AI story
            ai_story = self._generate_ai_story(company_context, ai_strategy_analysis)
            
            return {
                'investment_recommendation': investment_recommendation,
                'ai_metrics': ai_metrics,
                'ai_story': ai_story,
                'analysis_timestamp': self._get_timestamp()
            }
            
        except Exception as e:
            safe_log(f"=== CRITICAL ERROR in analyze_ai_potential: {str(e)} ===")
            import traceback
            safe_log(f"Full traceback: {traceback.format_exc()}")
            return self._get_default_analysis()
    
    def analyze_company_401k(self, company_name):
        """
        Analyze a company's 401K benefits and provide optimization recommendations using OpenAI
        
        Args:
            company_name (str): Name of the company to analyze
            
        Returns:
            dict: Comprehensive 401K analysis results
        """
        try:
            safe_log(f"Starting 401K analysis for {company_name}")
            
            # Get comprehensive 401K analysis
            analysis_result = self._analyze_401k_benefits(company_name)
            
            return {
                'overview': analysis_result.get('overview', {}),
                'recommendation': analysis_result.get('recommendation', {}),
                'contribution_strategy': analysis_result.get('contribution_strategy', {}),
                'roth_analysis': analysis_result.get('roth_analysis', {}),
                'fund_options': analysis_result.get('fund_options', {}),
                'additional_benefits': analysis_result.get('additional_benefits', {}),
                'analysis_timestamp': self._get_timestamp()
            }
            
        except Exception as e:
            safe_log(f"Error in 401K analysis: {str(e)}")
            return self._get_default_401k_analysis()
    
    def _analyze_401k_benefits(self, company_name):
        """Analyze company's 401K benefits using OpenAI"""
        try:
            safe_log(f"Analyzing 401K benefits for {company_name}")
            
            prompt = f"""
            Analyze the 401K benefits and retirement plan for {company_name}.
            
            Please provide a comprehensive analysis including:
            1. Company 401K match details (percentage and limits)
            2. Vesting schedule and requirements
            3. Available investment options and fund categories
            4. Roth 401K availability and recommendations
            5. Contribution strategies and optimization tips
            6. Additional retirement benefits and perks
            7. Comparison to industry standards
            8. Personalized recommendations for maximizing benefits
            
            Respond in JSON format with the following structure:
            {{
                "overview": {{
                    "match_percentage": 0-100,
                    "max_match_salary_percent": 0-15,
                    "vesting_period": "immediate/1 year/2 years/etc",
                    "roth_available": true/false,
                    "company_size": "startup/mid-size/large enterprise",
                    "industry_rating": "below average/average/above average/excellent"
                }},
                "recommendation": {{
                    "optimization_score": 0-10,
                    "primary_advice": "main recommendation",
                    "key_actions": ["action1", "action2", "action3"],
                    "urgency_level": "low/medium/high"
                }},
                "contribution_strategy": {{
                    "recommended_contribution_percent": 0-30,
                    "annual_savings_potential": "$X,XXX - $XX,XXX",
                    "tax_optimization": "details about tax benefits",
                    "recommended_actions": ["specific action 1", "specific action 2"]
                }},
                "roth_analysis": {{
                    "recommendation": "Roth/Traditional/Mix",
                    "reasoning": "detailed explanation",
                    "age_considerations": "advice based on career stage",
                    "tax_bracket_impact": "current vs future tax considerations"
                }},
                "fund_options": {{
                    "fund_categories": ["Large Cap", "International", "Bonds", "Target Date"],
                    "recommended_funds": ["specific fund recommendation 1", "fund recommendation 2"],
                    "expense_ratio_analysis": "low/medium/high cost funds available",
                    "diversification_advice": "portfolio allocation recommendations"
                }},
                "additional_benefits": {{
                    "other_benefits": ["pension", "stock options", "HSA", "etc"],
                    "financial_wellness_perks": ["financial advisor access", "planning tools"],
                    "catch_up_contributions": "available for 50+ employees",
                    "loan_provisions": "details about 401k loans if available"
                }}
            }}
            
            Base your analysis on typical benefits for companies of this size and industry. 
            For well-known companies, use publicly available information about their actual benefits.
            Provide specific, actionable recommendations.
            """
            
            safe_log("Calling OpenAI API for 401K benefits analysis...")
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert financial advisor and benefits analyst specializing in 401K plans and retirement optimization. Provide detailed, practical advice based on current industry standards and best practices."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            safe_log("OpenAI API response received, processing 401K analysis...")
            
            # Use safe JSON parser to handle encoding issues
            result = self._parse_openai_json(response)
            if result:
                safe_log(f"401K analysis completed successfully with {len(result)} sections")
                return result
            else:
                safe_log("Failed to parse OpenAI response for 401K analysis")
                return {}
                
        except Exception as e:
            safe_log(f"Error in 401K benefits analysis: {str(e)}")
            return self._get_default_401k_benefits()
    
    def _get_default_401k_analysis(self):
        """Return default 401K analysis structure when analysis fails"""
        return {
            'overview': {
                'match_percentage': 0,
                'max_match_salary_percent': 0,
                'vesting_period': 'Unknown',
                'roth_available': False,
                'company_size': 'Unknown',
                'industry_rating': 'Unknown'
            },
            'recommendation': {
                'optimization_score': 5,
                'primary_advice': '401K analysis not available at this time.',
                'key_actions': [],
                'urgency_level': 'medium'
            },
            'contribution_strategy': {
                'recommended_contribution_percent': 10,
                'annual_savings_potential': 'Not calculated',
                'tax_optimization': 'Consult with financial advisor',
                'recommended_actions': ['Contribute enough to get company match']
            },
            'roth_analysis': {
                'recommendation': 'Traditional',
                'reasoning': 'Analysis not available',
                'age_considerations': 'Consider your current tax bracket',
                'tax_bracket_impact': 'Consult tax professional'
            },
            'fund_options': {
                'fund_categories': [],
                'recommended_funds': [],
                'expense_ratio_analysis': 'Unknown',
                'diversification_advice': 'Diversify investments across asset classes'
            },
            'additional_benefits': {
                'other_benefits': [],
                'financial_wellness_perks': [],
                'catch_up_contributions': 'Check if available for 50+',
                'loan_provisions': 'Check plan details'
            },
            'analysis_timestamp': self._get_timestamp()
        }
    
    def _get_default_401k_benefits(self):
        """Return default 401K benefits structure when OpenAI analysis fails"""
        return {
            'overview': {
                'match_percentage': 0,
                'max_match_salary_percent': 0,
                'vesting_period': 'Unknown',
                'roth_available': False,
                'company_size': 'Unknown',
                'industry_rating': 'Unknown'
            },
            'recommendation': {
                'optimization_score': 5,
                'primary_advice': '401K analysis temporarily unavailable.',
                'key_actions': ['Contribute at least enough to get company match', 'Review plan documents'],
                'urgency_level': 'medium'
            },
            'contribution_strategy': {
                'recommended_contribution_percent': 10,
                'annual_savings_potential': 'Not calculated',
                'tax_optimization': 'Standard tax-deferred benefits apply',
                'recommended_actions': ['Start with company match', 'Increase contributions annually']
            },
            'roth_analysis': {
                'recommendation': 'Traditional',
                'reasoning': 'Default recommendation for tax-deferred savings',
                'age_considerations': 'Younger employees may benefit from Roth options',
                'tax_bracket_impact': 'Consider current vs expected future tax rates'
            },
            'fund_options': {
                'fund_categories': ['Target Date Funds', 'Index Funds', 'Bond Funds'],
                'recommended_funds': ['Low-cost index funds', 'Target-date funds for simplicity'],
                'expense_ratio_analysis': 'Look for funds with expense ratios under 0.5%',
                'diversification_advice': 'Mix of stocks, bonds, and international exposure'
            },
            'additional_benefits': {
                'other_benefits': ['Standard 401k benefits'],
                'financial_wellness_perks': ['Online planning tools'],
                'catch_up_contributions': 'Available for employees 50 and older',
                'loan_provisions': 'Check with HR for loan availability'
            }
        }
    
    def _parse_openai_json(self, response):
        msg = response.choices[0].message
        parsed = getattr(msg, "parsed", None)
        if parsed is not None:
            return parsed
        content = getattr(msg, "content", None)
        if isinstance(content, str) and content.strip():
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def _prepare_company_context(self, symbol, company_info):
        """Prepare company context for AI analysis"""
        return {
            'symbol': symbol,
            'name': company_info.get('longName', 'Unknown'),
            'sector': company_info.get('sector', 'Unknown'),
            'industry': company_info.get('industry', 'Unknown'),
            'business_summary': company_info.get('longBusinessSummary', ''),
            'market_cap': company_info.get('marketCap', 0),
            'employees': company_info.get('fullTimeEmployees', 0),
            'revenue': company_info.get('totalRevenue', 0),
            'website': company_info.get('website', ''),
            'country': company_info.get('country', 'Unknown')
        }
    
    def _analyze_ai_strategy(self, company_context):
        """Analyze company's AI strategy using OpenAI"""
        try:
            # Sanitize all text fields to prevent Unicode errors
            company_name = sanitize_text(company_context.get('name', 'Unknown'))
            safe_log(f"Starting AI strategy analysis for {company_name}")
            
            sector = sanitize_text(company_context['sector'])
            industry = sanitize_text(company_context['industry'])
            business_summary = sanitize_text(company_context.get('business_summary', ''))[:1000]
            
            prompt = f"""
            Analyze the AI strategy and potential of {company_name} ({company_context['symbol']}).
            
            Company Details:
            - Sector: {sector}
            - Industry: {industry}
            - Business Summary: {business_summary}
            - Market Cap: ${company_context['market_cap']/1e9:.1f}B
            - Employees: {company_context['employees']:,}
            
            Please provide a comprehensive analysis of:
            1. Current AI initiatives and strategies
            2. AI competitive advantages
            3. Potential AI revenue streams
            4. AI partnerships and collaborations
            5. Future AI opportunities
            6. AI-related risks and challenges
            
            Respond in JSON format with the following structure:
            {{
                "ai_initiatives": ["initiative1", "initiative2"],
                "competitive_advantages": ["advantage1", "advantage2"],
                "revenue_streams": ["stream1", "stream2"],
                "partnerships": ["partner1", "partner2"],
                "opportunities": ["opportunity1", "opportunity2"],
                "risks": ["risk1", "risk2"],
                "ai_maturity_score": 0-10,
                "overall_assessment": "detailed assessment"
            }}
            """
            
            # Sanitize the complete prompt
            prompt = sanitize_text(prompt)
            
            safe_log(f"DEBUG: About to call OpenAI API with model: {self.model}")
            safe_log(f"DEBUG: Prompt length: {len(prompt)} characters")
            safe_log("Calling OpenAI API for AI strategy analysis...")
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert AI investment analyst with deep knowledge of technology companies and their AI strategies."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            safe_log("OpenAI API response received, processing content...")
            
            # Use safe JSON parser to handle encoding issues
            result = self._parse_openai_json(response)
            if result:
                safe_log(f"AI strategy analysis completed successfully with {len(result)} keys")
                return result
            else:
                safe_log("Failed to parse OpenAI response")
                return {}
            
        except Exception as e:
            safe_log(f"Error in AI strategy analysis: {str(e)}")
            return {
                "ai_initiatives": [],
                "competitive_advantages": [],
                "revenue_streams": [],
                "partnerships": [],
                "opportunities": [],
                "risks": [],
                "ai_maturity_score": 5,
                "overall_assessment": "Unable to complete AI analysis at this time."
            }
    
    def _get_investment_recommendation(self, company_context, ai_strategy):
        """Get AI-focused investment recommendation"""
        try:
            # Sanitize all text fields to prevent Unicode errors
            company_name = sanitize_text(company_context['name'])
            sector = sanitize_text(company_context['sector'])
            industry = sanitize_text(company_context['industry'])
            
            prompt = f"""
            Based on the AI analysis of {company_name} ({company_context['symbol']}), provide an investment recommendation specifically focused on AI potential.
            
            Company Context:
            - Sector: {sector}
            - Industry: {industry}
            - Market Cap: ${company_context['market_cap']/1e9:.1f}B
            
            AI Analysis Summary:
            - AI Maturity Score: {ai_strategy.get('ai_maturity_score', 5)}/10
            - Key AI Initiatives: {', '.join(str(x) for x in ai_strategy.get('ai_initiatives', [])[:3])}
            - Competitive Advantages: {', '.join(str(x) for x in ai_strategy.get('competitive_advantages', [])[:3])}
            - AI Opportunities: {', '.join(str(x) for x in ai_strategy.get('opportunities', [])[:3])}
            
            Provide a clear investment recommendation (BUY/HOLD/SELL) based on AI potential with:
            1. Clear reasoning focused on AI investment merits
            2. AI potential score (0-10)
            3. Specific AI-related catalysts or concerns
            
            Respond in JSON format:
            {{
                "action": "BUY/HOLD/SELL",
                "ai_score": 0-10,
                "reasoning": "detailed reasoning focusing on AI investment potential",
                "key_catalysts": ["catalyst1", "catalyst2"],
                "risk_factors": ["risk1", "risk2"]
            }}
            """
            
            # Sanitize the complete prompt
            prompt = sanitize_text(prompt)
            
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior investment analyst specializing in AI and technology investments. Provide clear, actionable investment recommendations."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            # Use safe JSON parser to handle encoding issues
            result = self._parse_openai_json(response)
            return result
            
        except Exception as e:
            safe_log(f"Error getting investment recommendation: {str(e)}")
            return {
                "action": "HOLD",
                "ai_score": 5,
                "reasoning": "Unable to complete investment analysis at this time.",
                "key_catalysts": [],
                "risk_factors": []
            }
    
    def _calculate_ai_metrics(self, company_context, ai_strategy):
        """Calculate key AI metrics"""
        try:
            # Base metrics calculation using available data
            ai_score = ai_strategy.get('ai_maturity_score', 5)
            
            # Estimate AI revenue exposure based on sector and AI initiatives
            sector_ai_multipliers = {
                'Technology': 1.5,
                'Communication Services': 1.2,
                'Consumer Cyclical': 1.0,
                'Healthcare': 1.1,
                'Financial Services': 1.1,
                'Industrials': 0.8,
                'Consumer Defensive': 0.7
            }
            
            base_exposure = sector_ai_multipliers.get(company_context['sector'], 0.8)
            ai_initiatives_count = len(ai_strategy.get('ai_initiatives', []))
            estimated_ai_exposure = min(100, (base_exposure * ai_score * 2) + (ai_initiatives_count * 5))
            
            # Estimate partnerships and patents based on analysis
            partnerships = len(ai_strategy.get('partnerships', []))
            estimated_patents = max(0, int(ai_score * 10) + (partnerships * 5))
            
            return {
                'ai_revenue_exposure': round(estimated_ai_exposure, 1),
                'ai_partnerships': partnerships,
                'ai_patents': estimated_patents,
                'ai_investment_score': ai_score
            }
            
        except Exception as e:
            safe_log(f"Error calculating AI metrics: {str(e)}")
            return {
                'ai_revenue_exposure': 0,
                'ai_partnerships': 0,
                'ai_patents': 0,
                'ai_investment_score': 5
            }
    
    def _generate_ai_story(self, company_context, ai_strategy):
        """Generate compelling AI investment story"""
        try:
            # Sanitize all text fields to prevent Unicode errors
            company_name = sanitize_text(company_context['name'])
            
            prompt = f"""
            Create a compelling AI investment story for {company_name} ({company_context['symbol']}).
            
            Based on this AI analysis:
            - AI Initiatives: {[str(x) for x in ai_strategy.get('ai_initiatives', [])]}
            - Competitive Advantages: {[str(x) for x in ai_strategy.get('competitive_advantages', [])]}
            - AI Opportunities: {[str(x) for x in ai_strategy.get('opportunities', [])]}
            - Revenue Streams: {[str(x) for x in ai_strategy.get('revenue_streams', [])]}
            
            Create an investment narrative that includes:
            1. Strategic AI positioning summary
            2. Specific AI use cases and applications
            3. Future AI growth opportunities
            4. Competitive AI advantages
            
            Respond in JSON format:
            {{
                "strategy_summary": "2-3 sentence summary of AI strategy",
                "use_cases": ["specific use case 1", "specific use case 2", "specific use case 3"],
                "opportunities": ["growth opportunity 1", "growth opportunity 2"],
                "competitive_advantages": ["advantage 1", "advantage 2"]
            }}
            """
            
            # Sanitize the complete prompt
            prompt = sanitize_text(prompt)
            
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating compelling investment narratives focused on AI potential. Be specific and factual."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            # Use safe JSON parser to handle encoding issues
            result = self._parse_openai_json(response)
            return result
            
        except Exception as e:
            safe_log(f"Error generating AI story: {str(e)}")
            return {
                "strategy_summary": "AI strategy analysis not available at this time.",
                "use_cases": [],
                "opportunities": [],
                "competitive_advantages": []
            }
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _get_default_analysis(self):
        """Return default analysis structure when AI analysis fails"""
        return {
            'investment_recommendation': {
                'action': 'HOLD',
                'ai_score': 5,
                'reasoning': 'AI analysis not available at this time.',
                'key_catalysts': [],
                'risk_factors': []
            },
            'ai_metrics': {
                'ai_revenue_exposure': 0,
                'ai_partnerships': 0,
                'ai_patents': 0,
                'ai_investment_score': 5
            },
            'ai_story': {
                'strategy_summary': 'AI analysis not available.',
                'use_cases': [],
                'opportunities': [],
                'competitive_advantages': []
            },
            'analysis_timestamp': self._get_timestamp()
        }