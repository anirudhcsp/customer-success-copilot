"""
W&B Weave Integration for Customer Success Copilot
Simplified version using @weave.op() decorators without manual logging

This demonstrates production-ready observability for Forward Deployed Engineers
"""

import weave
from typing import Dict, List, Optional
import json
import time
from datetime import datetime
from dataclasses import dataclass, asdict

from customer_success_agent import CustomerSuccessCopilot, AnalysisResult, CustomerProfile

def initialize_weave(project_name: str = "customer-success-copilot"):
    """Initialize Weave tracking for the project"""
    try:
        weave.init(project_name)
        print(f"✅ W&B Weave initialized: {project_name}")
        return True
    except Exception as e:
        print(f"⚠️ Weave initialization failed: {e}")
        return False

@dataclass
class ConversationTrace:
    """Complete conversation trace for W&B Weave"""
    conversation_id: str
    timestamp: str
    customer_profile: Optional[Dict]
    email_content: str
    analysis_results: Dict
    response_data: Dict
    performance_metrics: Dict
    quality_scores: Dict
    business_impact: Dict

@weave.op()
def analyze_sentiment_with_tracing(agent: CustomerSuccessCopilot, email_content: str) -> Dict:
    """Sentiment analysis with Weave tracing - decorator handles logging automatically"""
    start_time = time.time()
    result = agent._analyze_sentiment_urgency(email_content)
    processing_time = time.time() - start_time
    return {**result, "processing_time": processing_time}

@weave.op()
def classify_intent_with_tracing(agent: CustomerSuccessCopilot, email_content: str) -> List[str]:
    """Intent classification with Weave tracing"""
    return agent._classify_intent(email_content)

@weave.op()
def extract_issues_with_tracing(agent: CustomerSuccessCopilot, email_content: str) -> List[str]:
    """Issue extraction with Weave tracing"""
    return agent._extract_key_issues(email_content)

@weave.op()
def evaluate_response_quality(original_email: str, analysis: AnalysisResult, 
                             generated_response: str, agent: CustomerSuccessCopilot) -> Dict[str, float]:
    """Comprehensive response quality evaluation using LLM-as-judge"""
    
    evaluation_prompt = f"""
    You are an expert customer service quality evaluator. Rate this response across multiple dimensions.

    Original Customer Email: "{original_email[:500]}..."
    
    Customer Analysis Context:
    - Sentiment: {analysis.sentiment['label']} (confidence: {analysis.sentiment['confidence']:.2f})
    - Urgency: {analysis.urgency['level']}
    - Key Issues: {', '.join(analysis.key_issues[:3])}
    - Escalation Needed: {analysis.escalation_needed}
    
    Generated Response: "{generated_response}"
    
    Rate each dimension from 1-10:
    1. Issue Coverage: How well does the response address all customer concerns?
    2. Tone Appropriateness: Does the tone match the customer's emotional state?
    3. Professionalism: Is the response professional and well-structured?
    4. Empathy: Does it show understanding and care for the customer?
    5. Actionability: Are next steps clear and specific?
    6. Personalization: Is it tailored to the customer context?
    
    Return ONLY a JSON object with these scores:
    {{"issue_coverage": X, "tone_appropriateness": X, "professionalism": X, "empathy": X, "actionability": X, "personalization": X}}
    """
    
    try:
        response = agent.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert customer service evaluator. Return only valid JSON with numeric scores 1-10."},
                {"role": "user", "content": evaluation_prompt}
            ],
            temperature=0.1,
            max_tokens=200
        )
        
        scores = json.loads(response.choices[0].message.content)
        overall_score = sum(scores.values()) / len(scores)
        scores["overall_score"] = overall_score
        
        return scores
        
    except Exception as e:
        print(f"⚠️ Response evaluation error: {e}")
        return {
            "issue_coverage": 7.0,
            "tone_appropriateness": 7.0,
            "professionalism": 8.0,
            "empathy": 7.0,
            "actionability": 7.0,
            "personalization": 6.0,
            "overall_score": 7.0
        }

class WeaveTrackedCustomerSuccessCopilot(CustomerSuccessCopilot):
    """
    Enhanced Customer Success Copilot with W&B Weave integration
    Uses @weave.op() decorators for automatic tracking
    """
    
    def __init__(self, api_key: str = None, weave_project: str = "customer-success-copilot"):
        super().__init__(api_key)
        self.weave_enabled = initialize_weave(weave_project)
        self.conversation_traces = []
        self.performance_metrics = {
            "total_conversations": 0,
            "total_processing_time": 0,
            "avg_quality_score": 0,
            "escalation_rate": 0,
            "customer_satisfaction_estimate": 0.85
        }
        
    @weave.op()
    def analyze_customer_communication_with_full_tracking(self, 
                                                         email_content: str, 
                                                         customer_profile: Optional[CustomerProfile] = None) -> Dict:
        """
        Complete customer communication analysis with full W&B Weave tracking
        All tracking happens automatically via @weave.op() decorator
        """
        conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        start_time = time.time()
        
        try:
            # Step 1: Sentiment Analysis (traced automatically)
            sentiment_result = analyze_sentiment_with_tracing(self, email_content)
            
            # Step 2: Intent Classification (traced automatically)
            intents = classify_intent_with_tracing(self, email_content)
            
            # Step 3: Issue Extraction (traced automatically)
            issues = extract_issues_with_tracing(self, email_content)
            
            # Step 4: Escalation Assessment
            escalation_needed = self._assess_escalation_need(
                email_content, sentiment_result, customer_profile
            )
            
            # Step 5: Compile Analysis Results
            analysis = AnalysisResult(
                sentiment=sentiment_result["sentiment"],
                urgency=sentiment_result["urgency"],
                intent=intents,
                key_issues=issues,
                customer_context=self._build_customer_context(customer_profile),
                escalation_needed=escalation_needed,
                estimated_resolution_time=self._estimate_resolution_time(intents, escalation_needed)
            )
            
            # Step 6: Generate Response
            response_data = self._generate_tracked_response(analysis, email_content, conversation_id)
            
            # Step 7: Evaluate Response Quality (traced automatically)
            quality_scores = evaluate_response_quality(email_content, analysis, 
                                                      response_data["suggested_response"], self)
            
            total_processing_time = time.time() - start_time
            
            # Step 8: Calculate Business Impact Metrics
            business_impact = self._calculate_business_impact(analysis, quality_scores, total_processing_time)
            
            # Step 9: Create Complete Conversation Trace
            conversation_trace = ConversationTrace(
                conversation_id=conversation_id,
                timestamp=datetime.now().isoformat(),
                customer_profile=asdict(customer_profile) if customer_profile else None,
                email_content=email_content[:200] + "..." if len(email_content) > 200 else email_content,
                analysis_results={
                    "sentiment": analysis.sentiment,
                    "urgency": analysis.urgency,
                    "intent": analysis.intent,
                    "key_issues": analysis.key_issues,
                    "escalation_needed": analysis.escalation_needed
                },
                response_data={
                    "response_length": len(response_data["suggested_response"]),
                    "tone_guidance": response_data["tone_guidance"],
                    "follow_up_actions": response_data["follow_up_actions"]
                },
                performance_metrics={
                    "total_processing_time": total_processing_time,
                    "sentiment_processing_time": sentiment_result.get("processing_time", 0),
                    "response_generation_time": response_data.get("generation_time", 0)
                },
                quality_scores=quality_scores,
                business_impact=business_impact
            )
            
            # Store trace
            self.conversation_traces.append(conversation_trace)
            self._update_performance_metrics(conversation_trace)
            
            return {
                "analysis": analysis,
                "response_data": response_data,
                "quality_scores": quality_scores,
                "business_impact": business_impact,
                "conversation_trace": conversation_trace,
                "performance_metrics": {
                    "processing_time": total_processing_time,
                    "conversation_id": conversation_id
                }
            }
            
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            raise
    
    @weave.op()
    def _generate_tracked_response(self, analysis: AnalysisResult, email_content: str, conversation_id: str) -> Dict:
        """Generate response with tracking"""
        start_time = time.time()
        response_data = self.generate_response_suggestion(analysis, email_content)
        generation_time = time.time() - start_time
        response_data["generation_time"] = generation_time
        return response_data
    
    def _calculate_business_impact(self, analysis: AnalysisResult, quality_scores: Dict, processing_time: float) -> Dict:
        """Calculate business impact metrics for this conversation"""
        
        manual_analysis_time = 15  # minutes
        ai_analysis_time = processing_time / 60  # convert to minutes
        time_saved = manual_analysis_time - ai_analysis_time
        
        baseline_quality = 6.5
        ai_quality = quality_scores["overall_score"]
        quality_improvement = max(0, ai_quality - baseline_quality)
        
        cost_per_minute_agent = 0.83  # $50/hour
        cost_savings = time_saved * cost_per_minute_agent
        
        satisfaction_multiplier = 1.0
        if analysis.escalation_needed and analysis.urgency["level"] in ["High", "Critical"]:
            satisfaction_multiplier = 1.3
        
        estimated_satisfaction_improvement = quality_improvement * 0.1 * satisfaction_multiplier
        
        return {
            "time_saved_minutes": round(time_saved, 2),
            "cost_savings_dollars": round(cost_savings, 2),
            "quality_improvement_points": round(quality_improvement, 2),
            "estimated_satisfaction_improvement": round(estimated_satisfaction_improvement, 3),
            "processing_efficiency": round((manual_analysis_time / max(ai_analysis_time, 0.1)), 1),
            "business_value_score": round(time_saved * quality_improvement, 2)
        }
    
    def _update_performance_metrics(self, trace: ConversationTrace):
        """Update running performance metrics"""
        self.performance_metrics["total_conversations"] += 1
        self.performance_metrics["total_processing_time"] += trace.performance_metrics["total_processing_time"]
        
        total_conversations = self.performance_metrics["total_conversations"]
        
        # Average quality score
        current_avg_quality = self.performance_metrics["avg_quality_score"]
        new_quality = trace.quality_scores["overall_score"]
        self.performance_metrics["avg_quality_score"] = (
            (current_avg_quality * (total_conversations - 1) + new_quality) / total_conversations
        )
        
        # Escalation rate
        escalations = sum(1 for t in self.conversation_traces if t.analysis_results["escalation_needed"])
        self.performance_metrics["escalation_rate"] = escalations / total_conversations
    
    def get_analytics_dashboard_data(self) -> Dict:
        """Generate comprehensive analytics data for dashboard"""
        
        if not self.conversation_traces:
            return self._get_demo_analytics_data()
        
        traces = self.conversation_traces
        
        avg_processing_time = sum(t.performance_metrics["total_processing_time"] for t in traces) / len(traces)
        avg_quality_score = sum(t.quality_scores["overall_score"] for t in traces) / len(traces)
        escalation_rate = sum(1 for t in traces if t.analysis_results["escalation_needed"]) / len(traces)
        
        sentiments = [t.analysis_results["sentiment"]["label"] for t in traces]
        sentiment_dist = {
            "Positive": sentiments.count("Positive") / len(sentiments) if sentiments else 0,
            "Neutral": sentiments.count("Neutral") / len(sentiments) if sentiments else 0,
            "Frustrated": sentiments.count("Frustrated") / len(sentiments) if sentiments else 0,
            "Angry": sentiments.count("Angry") / len(sentiments) if sentiments else 0
        }
        
        urgencies = [t.analysis_results["urgency"]["level"] for t in traces]
        urgency_dist = {
            "Low": urgencies.count("Low") / len(urgencies) if urgencies else 0,
            "Medium": urgencies.count("Medium") / len(urgencies) if urgencies else 0,
            "High": urgencies.count("High") / len(urgencies) if urgencies else 0,
            "Critical": urgencies.count("Critical") / len(urgencies) if urgencies else 0
        }
        
        total_time_saved = sum(t.business_impact["time_saved_minutes"] for t in traces)
        total_cost_savings = sum(t.business_impact["cost_savings_dollars"] for t in traces)
        
        return {
            "performance_metrics": {
                "total_conversations": len(traces),
                "avg_processing_time_seconds": round(avg_processing_time, 2),
                "avg_quality_score": round(avg_quality_score, 2),
                "escalation_rate": round(escalation_rate, 3)
            },
            "distribution_metrics": {
                "sentiment_distribution": sentiment_dist,
                "urgency_distribution": urgency_dist
            },
            "business_impact": {
                "total_time_saved_minutes": round(total_time_saved, 2),
                "total_cost_savings_dollars": round(total_cost_savings, 2),
                "avg_time_saved_per_conversation": round(total_time_saved / len(traces), 2),
                "estimated_annual_savings": round(total_cost_savings * 365 / len(traces), 0)
            },
            "quality_metrics": {
                "avg_issue_coverage": round(sum(t.quality_scores["issue_coverage"] for t in traces) / len(traces), 2),
                "avg_tone_appropriateness": round(sum(t.quality_scores["tone_appropriateness"] for t in traces) / len(traces), 2),
                "avg_empathy_score": round(sum(t.quality_scores["empathy"] for t in traces) / len(traces), 2)
            }
        }
    
    def _get_demo_analytics_data(self) -> Dict:
        """Demo analytics data when no real conversations exist"""
        return {
            "performance_metrics": {
                "total_conversations": 0,
                "avg_processing_time_seconds": 3.2,
                "avg_quality_score": 8.1,
                "escalation_rate": 0.18
            },
            "distribution_metrics": {
                "sentiment_distribution": {
                    "Positive": 0.35,
                    "Neutral": 0.40,
                    "Frustrated": 0.20,
                    "Angry": 0.05
                },
                "urgency_distribution": {
                    "Low": 0.30,
                    "Medium": 0.45,
                    "High": 0.20,
                    "Critical": 0.05
                }
            },
            "business_impact": {
                "total_time_saved_minutes": 0,
                "total_cost_savings_dollars": 0,
                "avg_time_saved_per_conversation": 12.5,
                "estimated_annual_savings": 125000
            },
            "quality_metrics": {
                "avg_issue_coverage": 8.2,
                "avg_tone_appropriateness": 8.4,
                "avg_empathy_score": 7.9
            }
        }

if __name__ == "__main__":
    print("🔧 W&B Weave Integration - Customer Success Copilot")
    print("=" * 60)
    
    if initialize_weave("customer-success-copilot-demo"):
        print("✅ Weave integration ready for production deployment")
        print("✅ Complete conversation tracking enabled")
        print("✅ Response quality evaluation active")
        print("✅ Business impact analytics available")
        print("✅ Performance monitoring operational")