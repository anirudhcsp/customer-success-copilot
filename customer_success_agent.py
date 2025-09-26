"""
Customer Success Copilot - Core AI Agent
Built for Forward Deployed Engineer Interview Demo

This demonstrates:
- Advanced prompt engineering for customer support
- Multi-step AI reasoning and analysis
- Business-focused output formatting
- Production-ready error handling
"""

import openai
import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class CustomerProfile:
    """Customer information for context"""
    name: str
    tier: str  # "Premium", "Standard", "Basic"
    tenure_months: int
    previous_sentiment: str  # "Positive", "Neutral", "Negative"
    support_tickets_count: int
    last_interaction_date: str

@dataclass
class AnalysisResult:
    """Structured analysis output"""
    sentiment: Dict[str, float]  # {"label": "Frustrated", "confidence": 0.87}
    urgency: Dict[str, str]      # {"level": "High", "reasoning": "..."}
    intent: List[str]            # ["Billing Dispute", "Feature Request"]
    key_issues: List[str]        # ["Cannot access premium features", "Incorrect billing"]
    customer_context: Dict       # Additional context from customer profile
    escalation_needed: bool
    estimated_resolution_time: str

class CustomerSuccessCopilot:
    """
    AI-powered customer success agent that analyzes customer communications
    and provides intelligent response suggestions with business context
    """
    
    def __init__(self, api_key: str = None):
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in .env file or pass directly.")
            
        self.client = openai.OpenAI(api_key=api_key)
        self.company_knowledge = self._load_company_knowledge()
        self.analysis_history = []
    
    def _load_company_knowledge(self) -> Dict:
        """
        In a real implementation, this would load from a vector database
        For demo purposes, we'll use static knowledge
        """
        return {
            "billing_policies": [
                "Refunds available within 30 days of purchase",
                "Premium features include priority support and advanced analytics",
                "Billing cycles can be changed with 48 hours notice"
            ],
            "escalation_triggers": [
                "Cancellation threats",
                "Premium customer complaints", 
                "Data security concerns",
                "Integration failures affecting business operations"
            ],
            "response_templates": {
                "billing_dispute": "I understand your concern about billing. Let me review your account and ensure everything is accurate.",
                "feature_request": "Thank you for the suggestion! I'll make sure our product team sees this feedback.",
                "technical_issue": "I apologize for the technical difficulties. Let me get our engineering team involved to resolve this quickly."
            }
        }
    
    def analyze_customer_communication(self, 
                                     email_content: str, 
                                     customer_profile: Optional[CustomerProfile] = None) -> AnalysisResult:
        """
        Comprehensive analysis of customer communication
        
        Args:
            email_content: The customer's email/message
            customer_profile: Optional customer context
            
        Returns:
            AnalysisResult with structured analysis
        """
        
        print(f"🔍 Analyzing customer communication...")
        
        # Step 1: Sentiment and Urgency Analysis
        sentiment_urgency = self._analyze_sentiment_urgency(email_content)
        
        # Step 2: Intent Classification
        intent_analysis = self._classify_intent(email_content)
        
        # Step 3: Key Issues Extraction
        key_issues = self._extract_key_issues(email_content)
        
        # Step 4: Escalation Assessment
        escalation_needed = self._assess_escalation_need(
            email_content, sentiment_urgency, customer_profile
        )
        
        # Step 5: Resolution Time Estimation
        resolution_time = self._estimate_resolution_time(intent_analysis, escalation_needed)
        
        result = AnalysisResult(
            sentiment=sentiment_urgency["sentiment"],
            urgency=sentiment_urgency["urgency"],
            intent=intent_analysis,
            key_issues=key_issues,
            customer_context=self._build_customer_context(customer_profile),
            escalation_needed=escalation_needed,
            estimated_resolution_time=resolution_time
        )
        
        # Store in history
        self.analysis_history.append(result)
        
        return result
    
    def _analyze_sentiment_urgency(self, email_content: str) -> Dict:
        """Analyze sentiment and urgency using LLM"""
        
        prompt = f"""
        Analyze this customer email for sentiment and urgency:

        Email: "{email_content}"

        Provide analysis in this exact JSON format:
        {{
            "sentiment": {{
                "label": "Positive/Neutral/Frustrated/Angry",
                "confidence": 0.0-1.0,
                "key_indicators": ["specific phrases that indicate sentiment"]
            }},
            "urgency": {{
                "level": "Low/Medium/High/Critical",
                "reasoning": "Explanation of urgency level",
                "urgency_indicators": ["specific phrases indicating urgency"]
            }}
        }}
        
        Consider factors like:
        - Emotional language and tone
        - Explicit urgency indicators ("urgent", "immediately", "ASAP")
        - Business impact mentions
        - Threat of cancellation or escalation
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert customer success analyst. Provide accurate sentiment and urgency analysis in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=500
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"⚠️ Sentiment analysis error: {e}")
            # Fallback analysis
            return {
                "sentiment": {"label": "Neutral", "confidence": 0.5, "key_indicators": []},
                "urgency": {"level": "Medium", "reasoning": f"Analysis error: {str(e)}", "urgency_indicators": []}
            }
    
    def _classify_intent(self, email_content: str) -> List[str]:
        """Classify customer intent/purpose"""
        
        prompt = f"""
        Classify the intent(s) in this customer email:

        Email: "{email_content}"

        Common intents include:
        - Billing Dispute
        - Feature Request
        - Technical Issue
        - Account Access
        - Cancellation Request
        - Integration Support
        - Training Request
        - General Inquiry
        - Complaint
        - Compliment

        Return ONLY a JSON array of applicable intents:
        ["Intent 1", "Intent 2"]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at classifying customer support intents. Return only valid JSON arrays."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=200
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"⚠️ Intent classification error: {e}")
            return ["General Inquiry"]
    
    def _extract_key_issues(self, email_content: str) -> List[str]:
        """Extract specific issues mentioned"""
        
        prompt = f"""
        Extract the specific issues or problems mentioned in this email:

        Email: "{email_content}"

        Return ONLY a JSON array of specific, actionable issues:
        ["Issue 1", "Issue 2", "Issue 3"]

        Focus on:
        - Concrete problems that need solving
        - Specific features not working
        - Billing discrepancies
        - Access issues
        - Integration failures
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at identifying specific customer issues. Return only valid JSON arrays of concrete, actionable problems."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=300
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"⚠️ Issue extraction error: {e}")
            return ["Unable to extract specific issues"]
    
    def _assess_escalation_need(self, 
                               email_content: str, 
                               sentiment_urgency: Dict, 
                               customer_profile: Optional[CustomerProfile]) -> bool:
        """Determine if escalation is needed"""
        
        escalation_triggers = [
            "cancel", "cancellation", "terminate", "refund",
            "lawyer", "legal", "unacceptable", "terrible",
            "manager", "supervisor", "escalate"
        ]
        
        # Check content for escalation triggers
        content_lower = email_content.lower()
        content_escalation = any(trigger in content_lower for trigger in escalation_triggers)
        
        # Check sentiment/urgency
        high_urgency = sentiment_urgency.get("urgency", {}).get("level") in ["High", "Critical"]
        negative_sentiment = sentiment_urgency.get("sentiment", {}).get("label") in ["Frustrated", "Angry"]
        
        # Check customer profile
        premium_customer = customer_profile and customer_profile.tier == "Premium" if customer_profile else False
        
        return content_escalation or (high_urgency and negative_sentiment) or (premium_customer and negative_sentiment)
    
    def _estimate_resolution_time(self, intents: List[str], escalation_needed: bool) -> str:
        """Estimate resolution time based on issue complexity"""
        
        time_estimates = {
            "General Inquiry": "< 2 hours",
            "Billing Dispute": "24-48 hours",
            "Technical Issue": "4-24 hours",
            "Feature Request": "Logged for future development",
            "Account Access": "< 4 hours",
            "Integration Support": "1-3 business days",
            "Cancellation Request": "< 24 hours"
        }
        
        if escalation_needed:
            return "< 2 hours (escalated)"
        
        # Get the longest estimate from all intents
        max_time = "< 2 hours"
        for intent in intents:
            if intent in time_estimates:
                estimated_time = time_estimates[intent]
                if "business days" in estimated_time or "24-48" in estimated_time:
                    max_time = estimated_time
        
        return max_time
    
    def _build_customer_context(self, customer_profile: Optional[CustomerProfile]) -> Dict:
        """Build customer context for response personalization"""
        
        if not customer_profile:
            return {"profile_available": False}
        
        return {
            "profile_available": True,
            "customer_name": customer_profile.name,
            "tier": customer_profile.tier,
            "tenure": f"{customer_profile.tenure_months} months",
            "previous_sentiment": customer_profile.previous_sentiment,
            "support_history": f"{customer_profile.support_tickets_count} previous tickets",
            "relationship_strength": self._assess_relationship_strength(customer_profile)
        }
    
    def _assess_relationship_strength(self, customer_profile: CustomerProfile) -> str:
        """Assess customer relationship strength"""
        
        score = 0
        
        # Tenure bonus
        if customer_profile.tenure_months > 24:
            score += 2
        elif customer_profile.tenure_months > 12:
            score += 1
        
        # Tier bonus
        if customer_profile.tier == "Premium":
            score += 2
        elif customer_profile.tier == "Standard":
            score += 1
        
        # Sentiment bonus
        if customer_profile.previous_sentiment == "Positive":
            score += 2
        elif customer_profile.previous_sentiment == "Neutral":
            score += 1
        
        # Support history (fewer tickets = better)
        if customer_profile.support_tickets_count < 3:
            score += 1
        
        if score >= 6:
            return "Strong"
        elif score >= 4:
            return "Moderate"
        else:
            return "Weak"

    def generate_response_suggestion(self, 
                                   analysis: AnalysisResult, 
                                   email_content: str) -> Dict[str, str]:
        """Generate suggested response based on analysis"""
        
        print(f"📝 Generating response suggestion...")
        
        # Build context for response generation
        context = f"""
        Customer Analysis:
        - Sentiment: {analysis.sentiment['label']} (confidence: {analysis.sentiment['confidence']:.2f})
        - Urgency: {analysis.urgency['level']}
        - Intents: {', '.join(analysis.intent)}
        - Key Issues: {', '.join(analysis.key_issues)}
        - Escalation Needed: {analysis.escalation_needed}
        - Customer Tier: {analysis.customer_context.get('tier', 'Unknown')}
        
        Original Email: "{email_content}"
        """
        
        prompt = f"""
        Generate a professional, empathetic customer support response based on this analysis:

        {context}

        The response should:
        1. Acknowledge their concerns specifically
        2. Address each key issue mentioned
        3. Match the appropriate tone (more formal for angry customers)
        4. Include next steps and timeline
        5. Be personalized if customer info is available
        6. Be concise but comprehensive

        Generate a response that a customer success professional would send.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert customer success manager who writes empathetic, professional, and effective customer responses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            suggested_response = response.choices[0].message.content
            
            return {
                "suggested_response": suggested_response,
                "tone_guidance": self._get_tone_guidance(analysis),
                "follow_up_actions": self._generate_follow_up_actions(analysis)
            }
            
        except Exception as e:
            print(f"⚠️ Response generation error: {e}")
            return {
                "suggested_response": "I apologize for the delay in my response. I'm looking into your inquiry and will get back to you shortly with a resolution.",
                "tone_guidance": "Professional and apologetic",
                "follow_up_actions": f"Error generating actions: {str(e)}"
            }
    
    def _get_tone_guidance(self, analysis: AnalysisResult) -> str:
        """Provide tone guidance for the response"""
        
        sentiment = analysis.sentiment['label']
        urgency = analysis.urgency['level']
        
        if sentiment in ["Angry", "Frustrated"] and urgency in ["High", "Critical"]:
            return "Extremely empathetic, formal, and solution-focused. Acknowledge frustration explicitly."
        elif sentiment in ["Angry", "Frustrated"]:
            return "Empathetic and professional. Focus on understanding and resolving concerns."
        elif urgency in ["High", "Critical"]:
            return "Professional and urgent. Emphasize quick resolution timeline."
        else:
            return "Friendly and professional. Maintain positive relationship tone."
    
    def _generate_follow_up_actions(self, analysis: AnalysisResult) -> str:
        """Generate internal follow-up actions"""
        
        actions = []
        
        if analysis.escalation_needed:
            actions.append("🚨 Escalate to manager immediately")
        
        if "Billing Dispute" in analysis.intent:
            actions.append("💰 Review billing history and usage")
        
        if "Technical Issue" in analysis.intent:
            actions.append("🔧 Engage engineering team for technical review")
        
        if "Feature Request" in analysis.intent:
            actions.append("💡 Log feature request in product backlog")
        
        if analysis.customer_context.get('tier') == 'Premium':
            actions.append("⭐ Apply premium support SLA (< 4 hour response)")
        
        actions.append(f"⏰ Follow up within {analysis.estimated_resolution_time}")
        
        return " | ".join(actions)


# Demo usage and testing
if __name__ == "__main__":
    print("🚀 Customer Success Copilot - Core Agent Ready!")
    print("This is the foundation for your interview demo.")
    print("\nNext steps:")
    print("1. Test with sample customer emails")
    print("2. Integrate with W&B Weave for tracking")
    print("3. Build Streamlit interface for live demo")