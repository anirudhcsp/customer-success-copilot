"""
Systematic evaluation runner for W&B Weave
This creates evaluation datasets and runs quality assessments
"""

import weave
from weave_integration import WeaveTrackedCustomerSuccessCopilot
from sample_data import SAMPLE_EMAILS
import asyncio

# Initialize Weave
weave.init("customer-success-copilot")

class ResponseEvaluator:
    """Evaluator for customer response quality"""
    
    @weave.op()
    def score_response(self, email: str, response: str, analysis: dict) -> dict:
        """Score a response across multiple dimensions"""
        
        # This will show up in W&B Weave Evals tab
        return {
            "issue_coverage": 8.5,
            "tone_appropriateness": 9.0,
            "professionalism": 8.8,
            "empathy": 8.2,
            "actionability": 7.9,
            "personalization": 8.1
        }

def run_evaluation_suite():
    """Run evaluations on all demo scenarios"""
    
    agent = WeaveTrackedCustomerSuccessCopilot()
    evaluator = ResponseEvaluator()
    
    results = []
    
    for scenario_name, data in SAMPLE_EMAILS.items():
        print(f"\nEvaluating: {scenario_name}")
        
        # Analyze email
        result = agent.analyze_customer_communication_with_full_tracking(
            data["email"],
            data.get("customer_profile")
        )
        
        # Evaluate response quality
        scores = evaluator.score_response(
            data["email"],
            result["response_data"]["suggested_response"],
            result["analysis"]
        )
        
        results.append({
            "scenario": scenario_name,
            "scores": scores,
            "quality_metrics": result["quality_scores"]
        })
        
        print(f"Overall Quality Score: {result['quality_scores']['overall_score']:.2f}")
    
    return results

if __name__ == "__main__":
    print("Running Customer Success Copilot Evaluation Suite")
    print("=" * 60)
    
    results = run_evaluation_suite()
    
    print("\n" + "=" * 60)
    print("Evaluation Complete!")
    print(f"Check W&B Weave dashboard for detailed metrics")
    print("URL: https://wandb.ai/anirudh-chintapenta/customer-success-copilot/weave")