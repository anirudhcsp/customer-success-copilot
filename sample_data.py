"""
Sample Customer Data for Demo
Realistic customer scenarios for interview demonstration
"""

from customer_success_agent import CustomerProfile

# Sample Customer Profiles
CUSTOMER_PROFILES = {
    "sarah_johnson": CustomerProfile(
        name="Sarah Johnson",
        tier="Premium",
        tenure_months=36,
        previous_sentiment="Positive",
        support_tickets_count=2,
        last_interaction_date="2024-08-15"
    ),
    
    "mike_chen": CustomerProfile(
        name="Mike Chen", 
        tier="Standard",
        tenure_months=8,
        previous_sentiment="Neutral",
        support_tickets_count=5,
        last_interaction_date="2024-09-20"
    ),
    
    "alex_rodriguez": CustomerProfile(
        name="Alex Rodriguez",
        tier="Basic",
        tenure_months=3,
        previous_sentiment="Positive", 
        support_tickets_count=1,
        last_interaction_date="2024-09-25"
    )
}

# Sample Customer Emails for Demo
SAMPLE_EMAILS = {
    "frustrated_premium": {
        "email": """
        Subject: URGENT - Premium Features Not Working - Need Immediate Resolution

        Hi Support Team,

        I am extremely frustrated with the current state of your platform. As a Premium 
        customer for over 3 years, I expect better service than what I'm receiving.

        The advanced analytics dashboard that I pay extra for has been completely 
        non-functional for the past week. When I try to generate reports, I get error 
        messages, and the data export feature is completely broken.

        This is affecting our quarterly business review with stakeholders, and frankly, 
        if this isn't resolved by tomorrow, I'll have to seriously consider canceling 
        our subscription and moving to a competitor.

        I need someone senior to call me TODAY to discuss this. My direct number is 
        555-0123.

        This is unacceptable for a Premium service.

        Sarah Johnson
        CFO, TechCorp Solutions
        """,
        "customer_profile": CUSTOMER_PROFILES["sarah_johnson"]
    },
    
    "billing_question": {
        "email": """
        Subject: Question about Recent Billing Changes

        Hello,

        I noticed my bill increased by $200 last month, but I don't recall upgrading 
        any services. Could someone help me understand what changed?

        I've been comparing your service with competitors lately, and I want to make 
        sure I'm getting good value. The extra cost is significant for our small business.

        Also, I'd like to know if there are any discounts available for longer-term 
        commitments. We're planning our budget for next year.

        Please let me know what options I have.

        Thanks,
        Mike Chen
        Operations Manager
        """,
        "customer_profile": CUSTOMER_PROFILES["mike_chen"]
    },
    
    "positive_feedback": {
        "email": """
        Subject: Great Experience with New Features!

        Hi there!

        I just wanted to reach out and say how impressed I am with the new automation 
        features you rolled out last month. The workflow builder has saved our team 
        hours of manual work each week.

        The user interface is intuitive, and the tutorial videos were really helpful 
        for getting our team up to speed quickly.

        I do have one small suggestion - it would be great if we could set custom 
        notifications for when automated workflows complete. Right now we have to 
        check manually.

        Also, are there any advanced training sessions available? We'd love to learn 
        more about maximizing the platform's potential.

        Keep up the excellent work!

        Best regards,
        Alex Rodriguez
        Project Coordinator
        """,
        "customer_profile": CUSTOMER_PROFILES["alex_rodriguez"]
    },
    
    "technical_integration": {
        "email": """
        Subject: API Integration Issues - Production Environment

        Support Team,

        We're experiencing critical issues with the API integration in our production 
        environment. The webhook endpoints are returning 500 errors intermittently, 
        causing data sync failures between our systems.

        This started happening after the maintenance window on Sunday night. Our 
        development team has tried the standard troubleshooting steps, but we need 
        help from your engineering team.

        Error details:
        - Endpoint: /api/v2/webhooks/data-sync
        - Error: HTTP 500 - Internal Server Error
        - Frequency: ~30% of requests
        - Impact: Customer data not syncing to our CRM

        This is affecting our sales team's ability to follow up with leads. Can someone 
        from engineering review the logs and provide an update?

        We need this resolved ASAP as it's impacting business operations.

        Thanks,
        Jennifer Kim
        Lead Developer
        """,
        "customer_profile": None  # New customer, no profile yet
    },
    
    "cancellation_threat": {
        "email": """
        Subject: Considering Cancellation - Multiple Ongoing Issues

        To Whom It May Concern,

        I'm writing to express my disappointment with the service quality over the 
        past few months. We've experienced multiple issues that haven't been 
        adequately resolved:

        1. Slow response times from support (3+ days for simple questions)
        2. Platform downtime during our peak business hours
        3. Missing features that were promised during the sales process
        4. Billing errors that took weeks to correct

        We've invested significant time and resources into your platform, but the 
        return on investment is no longer justified. Our contract is up for renewal 
        next month, and unless we see immediate improvements, we'll be moving to 
        [Competitor Name].

        I'd like to speak with a manager about our options. If you can't provide 
        the level of service we require, we need to know now so we can plan our 
        transition accordingly.

        Please have someone in leadership contact me within 48 hours.

        David Miller
        VP of Operations
        """,
        "customer_profile": CustomerProfile(
            name="David Miller",
            tier="Premium", 
            tenure_months=18,
            previous_sentiment="Negative",
            support_tickets_count=12,
            last_interaction_date="2024-09-22"
        )
    }
}

# Demo scenarios for different situations
DEMO_SCENARIOS = [
    {
        "name": "High-Priority Premium Customer",
        "description": "Frustrated premium customer with urgent technical issue",
        "email_key": "frustrated_premium",
        "expected_outcome": "High urgency, escalation needed, technical support required"
    },
    {
        "name": "Billing Inquiry with Churn Risk", 
        "description": "Cost-conscious customer questioning value, potential churn risk",
        "email_key": "billing_question",
        "expected_outcome": "Medium urgency, retention opportunity, billing team involvement"
    },
    {
        "name": "Positive Customer with Feature Request",
        "description": "Happy customer providing feedback and requesting enhancements",
        "email_key": "positive_feedback", 
        "expected_outcome": "Low urgency, feature request logging, relationship building"
    },
    {
        "name": "Critical Technical Integration Issue",
        "description": "Production system failure requiring immediate engineering support",
        "email_key": "technical_integration",
        "expected_outcome": "Critical urgency, engineering escalation, business impact"
    },
    {
        "name": "Cancellation Threat - Executive Escalation",
        "description": "Multiple issues leading to cancellation consideration",
        "email_key": "cancellation_threat", 
        "expected_outcome": "Critical urgency, executive escalation, retention strategy"
    }
]

def get_demo_email(scenario_name: str):
    """Get demo email by scenario name"""
    scenario = next((s for s in DEMO_SCENARIOS if s["name"] == scenario_name), None)
    if scenario:
        email_key = scenario["email_key"]
        return SAMPLE_EMAILS[email_key]
    return None

def get_all_scenarios():
    """Get all available demo scenarios"""
    return DEMO_SCENARIOS

if __name__ == "__main__":
    print("📧 Sample Customer Data Loaded!")
    print(f"Available scenarios: {len(DEMO_SCENARIOS)}")
    for scenario in DEMO_SCENARIOS:
        print(f"  - {scenario['name']}")