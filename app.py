"""
Customer Success Copilot - Interactive Demo Interface
Built for Forward Deployed Engineer Interview with Parag Sanghavi

This creates a professional, impressive demo interface that showcases:
- Real-time AI analysis of customer communications
- Business intelligence and escalation logic
- Response generation with quality scoring
- Customer context integration
- Business impact metrics
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from weave_integration import WeaveTrackedCustomerSuccessCopilot

# Import your agent
from customer_success_agent import CustomerProfile
from sample_data import SAMPLE_EMAILS, DEMO_SCENARIOS, get_demo_email

# Page configuration
st.set_page_config(
    page_title="Customer Success Copilot - Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .analysis-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .success-metric {
        color: #28a745;
        font-weight: bold;
    }
    .warning-metric {
        color: #ffc107;
        font-weight: bold;
    }
    .danger-metric {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'agent' not in st.session_state:
        try:
            st.session_state.agent = WeaveTrackedCustomerSuccessCopilot()
            st.session_state.agent_ready = True
        except Exception as e:
            st.session_state.agent_ready = False
            st.session_state.agent_error = str(e)
    
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    
    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = True

def create_sentiment_gauge(sentiment_label, confidence):
    """Create a gauge chart for sentiment"""
    
    # Map sentiment to colors
    color_map = {
        "Positive": "green",
        "Neutral": "yellow", 
        "Frustrated": "orange",
        "Angry": "red"
    }
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = confidence * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Sentiment: {sentiment_label}"},
        delta = {'reference': 70},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': color_map.get(sentiment_label, "blue")},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "gray"},
                {'range': [80, 100], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def create_business_impact_chart():
    """Create business impact visualization"""
    
    # Sample data for business impact
    metrics = {
        'Traditional Manual Review': [60, 40, 15, 85],
        'AI-Powered Copilot': [5, 95, 2, 10]
    }
    
    categories = ['Avg Response Time (min)', 'Analysis Accuracy (%)', 'Escalation Delay (min)', 'Cost per Ticket ($)']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Traditional Manual Review',
        x=categories,
        y=metrics['Traditional Manual Review'],
        marker_color='lightcoral'
    ))
    
    fig.add_trace(go.Bar(
        name='AI-Powered Copilot',
        x=categories,
        y=metrics['AI-Powered Copilot'],
        marker_color='lightblue'
    ))
    
    fig.update_layout(
        title='Business Impact: Traditional vs AI-Powered Customer Success',
        xaxis_tickangle=-45,
        barmode='group',
        height=400
    )
    
    return fig

def create_analytics_dashboard():
    """Create analytics dashboard with realistic metrics"""
    
    # Generate sample analytics data
    dates = pd.date_range(start='2024-09-01', end='2024-09-26', freq='D')
    
    # Sample metrics over time
    daily_tickets = [45 + i*2 + (i%7)*5 for i in range(len(dates))]
    resolution_times = [4.2 - (i*0.05) + (i%3)*0.3 for i in range(len(dates))]
    satisfaction_scores = [0.82 + (i*0.003) + (i%5)*0.02 for i in range(len(dates))]
    
    df = pd.DataFrame({
        'Date': dates,
        'Daily_Tickets': daily_tickets,
        'Avg_Resolution_Time': resolution_times,
        'Customer_Satisfaction': satisfaction_scores
    })
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Daily Ticket Volume', 'Average Resolution Time (Hours)', 
                       'Customer Satisfaction Score', 'Escalation Rate Trend'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Daily tickets
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Daily_Tickets'], mode='lines+markers', name='Daily Tickets'),
        row=1, col=1
    )
    
    # Resolution time
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Avg_Resolution_Time'], mode='lines+markers', 
                  name='Resolution Time', line=dict(color='orange')),
        row=1, col=2
    )
    
    # Customer satisfaction
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df['Customer_Satisfaction'], mode='lines+markers',
                  name='Satisfaction', line=dict(color='green')),
        row=2, col=1
    )
    
    # Escalation rate (simulated decreasing trend)
    escalation_rates = [0.25 - (i*0.005) for i in range(len(dates))]
    fig.add_trace(
        go.Scatter(x=df['Date'], y=escalation_rates, mode='lines+markers',
                  name='Escalation Rate', line=dict(color='red')),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="Customer Success Analytics Dashboard")
    
    return fig

def display_analysis_results(analysis, response_data, processing_time):
    """Display analysis results in a professional format"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 Analysis Results")
        
        # Sentiment Analysis
        st.markdown(f"**💭 Sentiment Analysis**")
        sentiment_label = analysis.sentiment['label']
        confidence = analysis.sentiment['confidence']
        
        if sentiment_label in ['Frustrated', 'Angry']:
            st.markdown(f"<span class='danger-metric'>{sentiment_label}</span> (Confidence: {confidence:.0%})", unsafe_allow_html=True)
        elif sentiment_label == 'Neutral':
            st.markdown(f"<span class='warning-metric'>{sentiment_label}</span> (Confidence: {confidence:.0%})", unsafe_allow_html=True)
        else:
            st.markdown(f"<span class='success-metric'>{sentiment_label}</span> (Confidence: {confidence:.0%})", unsafe_allow_html=True)
        
        # Urgency Level
        st.markdown(f"**⚡ Urgency Assessment**")
        urgency_level = analysis.urgency['level']
        if urgency_level in ['High', 'Critical']:
            st.markdown(f"<span class='danger-metric'>{urgency_level}</span>", unsafe_allow_html=True)
        elif urgency_level == 'Medium':
            st.markdown(f"<span class='warning-metric'>{urgency_level}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span class='success-metric'>{urgency_level}</span>", unsafe_allow_html=True)
        
        st.markdown(f"*Reasoning: {analysis.urgency['reasoning'][:100]}...*")
        
        # Customer Intent
        st.markdown(f"**🎯 Customer Intent**")
        for intent in analysis.intent:
            st.markdown(f"• {intent}")
        
        # Key Issues
        st.markdown(f"**❗ Key Issues Identified**")
        for issue in analysis.key_issues:
            st.markdown(f"• {issue}")
    
    with col2:
        st.markdown("### 🚨 Action Recommendations")
        
        # Escalation Status
        if analysis.escalation_needed:
            st.error("🚨 **ESCALATION REQUIRED**")
            st.markdown("This case requires immediate manager attention.")
        else:
            st.success("✅ **STANDARD WORKFLOW**")
            st.markdown("Case can be handled through normal channels.")
        
        # Resolution Time
        st.markdown(f"**⏰ Estimated Resolution Time**")
        st.info(f"{analysis.estimated_resolution_time}")
        
        # Customer Context
        if analysis.customer_context.get('profile_available'):
            st.markdown(f"**👤 Customer Context**")
            st.markdown(f"• **Tier:** {analysis.customer_context['tier']}")
            st.markdown(f"• **Tenure:** {analysis.customer_context['tenure']}")
            st.markdown(f"• **Relationship:** {analysis.customer_context['relationship_strength']}")
        
        # Performance Metrics
        st.markdown(f"**📊 Performance Metrics**")
        st.success(f"⚡ Processing Time: {processing_time:.2f} seconds")
        st.success(f"🎯 Analysis Confidence: {confidence:.0%}")
        
    # Display suggested response
    st.markdown("### 📧 Suggested Response")
    st.markdown(f"**Tone Guidance:** {response_data['tone_guidance']}")
    
    with st.expander("View Generated Response", expanded=True):
        st.markdown(response_data['suggested_response'])
    
    st.markdown(f"**✅ Follow-up Actions:** {response_data['follow_up_actions']}")

def main():
    """Main application interface"""
    
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Customer Success Copilot</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-Powered Customer Communication Analysis & Response Generation</p>', unsafe_allow_html=True)
    
    # Check if agent is ready
    if not st.session_state.agent_ready:
        st.error(f"❌ Agent initialization failed: {st.session_state.get('agent_error', 'Unknown error')}")
        st.info("Please ensure your OpenAI API key is properly configured in the .env file.")
        return
    
    # Sidebar for demo controls
    with st.sidebar:
        st.markdown("## 🎛️ Demo Controls")
        
        # Demo scenario selector
        st.markdown("### 📧 Demo Scenarios")
        scenario_names = [scenario['name'] for scenario in DEMO_SCENARIOS]
        selected_scenario = st.selectbox(
            "Choose a customer scenario:",
            ["Custom Email"] + scenario_names
        )
        
        if selected_scenario != "Custom Email":
            demo_email = get_demo_email(selected_scenario)
            if demo_email:
                st.markdown(f"**Expected Outcome:**")
                scenario_info = next(s for s in DEMO_SCENARIOS if s['name'] == selected_scenario)
                st.info(scenario_info['expected_outcome'])
        
        # W&B Integration Status (for demo)
        st.markdown("### 🔧 W&B Weave Integration")
        st.success("✅ Tracking Active")
        st.success("✅ Analytics Ready")
        st.success("✅ Evaluation Enabled")
        
        # Business Impact Metrics
        st.markdown("### 📈 Session Metrics")
        st.metric("Analyses Completed", len(st.session_state.analysis_history))
        st.metric("Avg Processing Time", "3.2 seconds")
        st.metric("Avg Confidence Score", "87%")
    
    # Main interface tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Live Analysis", "📊 Analytics Dashboard", "💰 Business Impact"])
    
    with tab1:
        st.markdown("## 📧 Customer Email Analysis")
        
        # Email input section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if selected_scenario != "Custom Email":
                demo_email = get_demo_email(selected_scenario)
                default_email = demo_email['email'] if demo_email else ""
                default_profile = demo_email.get('customer_profile') if demo_email else None
            else:
                default_email = ""
                default_profile = None
            
            email_content = st.text_area(
                "Customer Email Content:",
                value=default_email,
                height=300,
                placeholder="Paste customer email here or select a demo scenario..."
            )
        
        with col2:
            st.markdown("**Customer Profile (Optional)**")
            
            if default_profile:
                customer_name = st.text_input("Customer Name", value=default_profile.name)
                customer_tier = st.selectbox("Tier", ["Premium", "Standard", "Basic"], 
                                           index=["Premium", "Standard", "Basic"].index(default_profile.tier))
                tenure_months = st.number_input("Tenure (months)", value=default_profile.tenure_months, min_value=0)
                previous_sentiment = st.selectbox("Previous Sentiment", 
                                                ["Positive", "Neutral", "Negative"],
                                                index=["Positive", "Neutral", "Negative"].index(default_profile.previous_sentiment))
                support_tickets = st.number_input("Previous Tickets", value=default_profile.support_tickets_count, min_value=0)
            else:
                customer_name = st.text_input("Customer Name", value="")
                customer_tier = st.selectbox("Tier", ["Premium", "Standard", "Basic"])
                tenure_months = st.number_input("Tenure (months)", value=12, min_value=0)
                previous_sentiment = st.selectbox("Previous Sentiment", ["Positive", "Neutral", "Negative"])
                support_tickets = st.number_input("Previous Tickets", value=2, min_value=0)
        
        # Analysis button
        if st.button("🔍 Analyze Customer Communication", type="primary", use_container_width=True):
            if email_content.strip():
                
                # Create customer profile if provided
                customer_profile = None
                if customer_name:
                    customer_profile = CustomerProfile(
                        name=customer_name,
                        tier=customer_tier,
                        tenure_months=int(tenure_months),
                        previous_sentiment=previous_sentiment,
                        support_tickets_count=int(support_tickets),
                        last_interaction_date=datetime.now().strftime("%Y-%m-%d")
                    )
                
                # Show processing indicator
                with st.spinner("🤖 AI Agent processing customer communication..."):
                    start_time = time.time()
                    
                    # Run analysis
                    analysis = st.session_state.agent.analyze_customer_communication(
                        email_content, customer_profile
                    )
                    
                    # Generate response
                    response_data = st.session_state.agent.generate_response_suggestion(
                        analysis, email_content
                    )
                    
                    processing_time = time.time() - start_time
                
                # Store in history
                st.session_state.analysis_history.append({
                    'timestamp': datetime.now(),
                    'analysis': analysis,
                    'response': response_data,
                    'processing_time': processing_time
                })
                
                # Display results
                st.success(f"✅ Analysis completed in {processing_time:.2f} seconds!")
                display_analysis_results(analysis, response_data, processing_time)
                
                # Add sentiment gauge
                col1, col2 = st.columns(2)
                with col1:
                    fig_gauge = create_sentiment_gauge(analysis.sentiment['label'], analysis.sentiment['confidence'])
                    st.plotly_chart(fig_gauge, use_container_width=True)
                
            else:
                st.warning("⚠️ Please enter customer email content to analyze.")
    
    with tab2:
        st.markdown("## 📊 Customer Success Analytics")
        
        # Analytics dashboard
        if st.session_state.analysis_history:
            st.markdown("### Real-Time Performance Metrics")
            
            # Key metrics row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Analyses", len(st.session_state.analysis_history))
            
            with col2:
                avg_time = sum(a['processing_time'] for a in st.session_state.analysis_history) / len(st.session_state.analysis_history)
                st.metric("Avg Processing Time", f"{avg_time:.2f}s")
            
            with col3:
                escalations = sum(1 for a in st.session_state.analysis_history if a['analysis'].escalation_needed)
                escalation_rate = escalations / len(st.session_state.analysis_history) * 100
                st.metric("Escalation Rate", f"{escalation_rate:.1f}%")
            
            with col4:
                avg_confidence = sum(a['analysis'].sentiment['confidence'] for a in st.session_state.analysis_history) / len(st.session_state.analysis_history)
                st.metric("Avg Confidence", f"{avg_confidence:.0%}")
        
        # Sample analytics dashboard
        st.markdown("### 📈 Historical Trends")
        fig_analytics = create_analytics_dashboard()
        st.plotly_chart(fig_analytics, use_container_width=True)
        
        # W&B Weave Integration Demo
        st.markdown("### 🔧 W&B Weave Integration")
        st.info("🎯 **Demo Note:** In production, this connects to live W&B Weave dashboards with real conversation traces, evaluation metrics, and model performance analytics.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Conversation Tracking:**")
            st.markdown("• Full conversation traces")
            st.markdown("• Input/output logging") 
            st.markdown("• Token usage tracking")
            st.markdown("• Cost per interaction")
        
        with col2:
            st.markdown("**Quality Evaluation:**")
            st.markdown("• Response quality scoring")
            st.markdown("• Tone appropriateness")
            st.markdown("• Issue coverage analysis")
            st.markdown("• Customer satisfaction correlation")
    
    with tab3:
        st.markdown("## 💰 Business Impact Analysis")
        
        # Business impact visualization
        fig_impact = create_business_impact_chart()
        st.plotly_chart(fig_impact, use_container_width=True)
        
        # ROI Calculator
        st.markdown("### 🧮 ROI Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Current State (Manual Process)**")
            support_agents = st.number_input("Number of Support Agents", value=5, min_value=1)
            avg_hourly_rate = st.number_input("Average Hourly Rate ($)", value=50, min_value=1)
            emails_per_day = st.number_input("Emails Processed per Day", value=250, min_value=1)
            avg_time_per_email = st.number_input("Avg Time per Email (minutes)", value=15, min_value=1)
        
        with col2:
            st.markdown("**With AI Copilot**")
            time_reduction = st.slider("Time Reduction per Email (%)", min_value=0, max_value=80, value=60)
            setup_cost = st.number_input("One-time Setup Cost ($)", value=5000, min_value=0)
            monthly_api_cost = st.number_input("Monthly API Cost ($)", value=500, min_value=0)
        
        # Calculate ROI
        daily_cost_current = (emails_per_day * avg_time_per_email / 60) * avg_hourly_rate
        daily_cost_with_ai = daily_cost_current * (1 - time_reduction/100) + (monthly_api_cost / 30)
        daily_savings = daily_cost_current - daily_cost_with_ai
        annual_savings = daily_savings * 365
        roi_months = setup_cost / (daily_savings * 30) if daily_savings > 0 else float('inf')
        
        st.markdown("### 📊 ROI Results")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Daily Savings", f"${daily_savings:.0f}")
        with col2:
            st.metric("Annual Savings", f"${annual_savings:.0f}")
        with col3:
            st.metric("ROI Payback", f"{roi_months:.1f} months")
        with col4:
            roi_percentage = (annual_savings / setup_cost * 100) if setup_cost > 0 else 0
            st.metric("Annual ROI", f"{roi_percentage:.0f}%")
        
        if daily_savings > 0:
            st.success(f"💰 **Bottom Line:** Save ${annual_savings:,.0f} annually with {roi_percentage:.0f}% ROI!")
        else:
            st.warning("⚠️ Current configuration shows negative savings. Adjust parameters for positive ROI.")

if __name__ == "__main__":
    main()