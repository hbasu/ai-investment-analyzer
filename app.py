import os

os.environ["PYTHONUTF8"] = "1"

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io

from stock_data import StockDataFetcher
from ai_analysis import AIAnalyzer

# Configure page
st.set_page_config(page_title="AI Investment Analyzer",
                   page_icon="🤖",
                   layout="wide")

# Initialize session state
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = None
if '401k_analysis_data' not in st.session_state:
    st.session_state['401k_analysis_data'] = None


def main():
    st.title("🤖 AI Investment Analyzer")
    st.markdown(
        "*Analyze stocks and 401K benefits using advanced AI-powered insights*"
    )

    # Sidebar for input
    with st.sidebar:
        # Tab selector
        analysis_type = st.radio("Select Analysis Type",
                                 ["Stock Analysis", "401K Analysis"],
                                 index=0)

        st.divider()

        if analysis_type == "Stock Analysis":
            stock_symbol, selected_period, period_options, analyze_button = stock_analysis_sidebar(
            )
        else:
            company_name, analyze_401k_button = fourk_analysis_sidebar()

    # Main content area (outside sidebar)
    if analysis_type == "Stock Analysis":
        handle_stock_analysis(stock_symbol, selected_period, period_options,
                              analyze_button)
    else:
        handle_401k_analysis(company_name, analyze_401k_button)


def stock_analysis_sidebar():
    """Sidebar content for stock analysis"""
    st.header("Stock Analysis")

    # Stock symbol input
    stock_symbol = st.text_input(
        "Enter Stock Symbol",
        placeholder="e.g., AAPL, MSFT, GOOGL",
        help="Enter a valid stock ticker symbol").upper()

    # Time period selection
    period_options = {
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
        "2 Years": "2y"
    }

    selected_period = st.selectbox(
        "Analysis Period",
        options=list(period_options.keys()),
        index=3  # Default to 1 year
    )

    analyze_button = st.button("🔍 Analyze Stock", type="primary")

    return stock_symbol, selected_period, period_options, analyze_button


def fourk_analysis_sidebar():
    """Sidebar content for 401K analysis"""
    st.header("401K Analysis")

    # Company name input
    company_name = st.text_input(
        "Enter Company Name",
        placeholder="e.g., Microsoft, Google, Apple",
        help="Enter the company name to analyze 401K benefits")

    analyze_401k_button = st.button("💰 Analyze 401K", type="primary")

    return company_name, analyze_401k_button


def handle_stock_analysis(stock_symbol, selected_period, period_options,
                          analyze_button):
    """Handle stock analysis logic"""
    if analyze_button and stock_symbol:
        with st.spinner("Fetching stock data and performing AI analysis..."):
            try:
                # Initialize data fetcher and AI analyzer
                stock_fetcher = StockDataFetcher()
                ai_analyzer = AIAnalyzer()

                # Fetch stock data
                stock_data = stock_fetcher.get_stock_data(
                    stock_symbol, period_options[selected_period])

                if stock_data is None:
                    st.error(
                        "❌ Invalid stock symbol or no data available. Please check the symbol and try again."
                    )
                    return

                # Perform AI analysis
                ai_analysis = ai_analyzer.analyze_ai_potential(
                    stock_symbol, stock_data['info'])

                # Store in session state
                st.session_state.stock_data = stock_data
                st.session_state.analysis_data = ai_analysis

                # Display results
                display_analysis_results(stock_data, ai_analysis)

            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")

    elif st.session_state.analysis_data and st.session_state.stock_data:
        # Display previously analyzed data
        display_analysis_results(st.session_state.stock_data,
                                 st.session_state.analysis_data)

    else:
        # Welcome screen for stock analysis
        st.markdown("""
        ## Welcome to AI Investment Analyzer - Stock Analysis
        
        This application helps you evaluate stocks based on their AI investment potential using:
        
        - 📊 **Real-time financial data** from Yahoo Finance
        - 🤖 **AI-powered analysis** of company AI strategies
        - 📈 **Investment recommendations** based on AI potential
        - 🎯 **Key AI metrics** and partnership analysis
        - 📋 **Downloadable reports** in CSV format
        
        **Get Started:** Enter a stock symbol in the sidebar to begin your AI investment analysis.
        """)


def handle_401k_analysis(company_name, analyze_401k_button):
    """Handle 401K analysis logic"""
    if analyze_401k_button and company_name:
        with st.spinner(f"Analyzing 401K benefits for {company_name}..."):
            try:
                # Initialize AI analyzer
                ai_analyzer = AIAnalyzer()

                # Perform 401K analysis
                fourk_analysis = ai_analyzer.analyze_company_401k(company_name)

                # Store in session state
                st.session_state['401k_analysis_data'] = {
                    'company_name': company_name,
                    'analysis': fourk_analysis
                }

                # Display results
                display_401k_results(company_name, fourk_analysis)

            except Exception as e:
                st.error(f"❌ Error during 401K analysis: {str(e)}")

    elif st.session_state['401k_analysis_data']:
        # Display previously analyzed data
        data = st.session_state['401k_analysis_data']
        display_401k_results(data['company_name'], data['analysis'])

    else:
        # Welcome screen for 401K analysis
        st.markdown("""
        ## Welcome to AI Investment Analyzer - 401K Analysis
        
        This tool helps you understand and optimize your company's 401K benefits using AI analysis:
        
        - 💰 **Company match analysis** - Understand your employer's matching policy
        - 📅 **Vesting schedules** - Know when you're fully vested
        - 🏦 **Investment options** - Review available funds and their performance
        - 🔄 **Roth vs Traditional** - Get personalized recommendations
        - 📊 **Contribution strategies** - Optimize your retirement savings
        - 📋 **Downloadable analysis** - Save your 401K optimization plan
        
        **Get Started:** Enter your company name in the sidebar to analyze your 401K benefits.
        """)


def display_analysis_results(stock_data, ai_analysis):
    """Display comprehensive analysis results"""

    company_info = stock_data['info']
    price_data = stock_data['price_data']

    # Company header
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.header(
            f"{company_info.get('longName', 'Unknown Company')} ({company_info.get('symbol', 'N/A')})"
        )
        st.write(
            f"**Sector:** {company_info.get('sector', 'N/A')} | **Industry:** {company_info.get('industry', 'N/A')}"
        )

    with col2:
        current_price = company_info.get('currentPrice', 0)
        st.metric("Current Price", f"${current_price:.2f}")

    with col3:
        market_cap = company_info.get('marketCap', 0)
        if market_cap > 0:
            market_cap_formatted = f"${market_cap/1e9:.1f}B" if market_cap > 1e9 else f"${market_cap/1e6:.1f}M"
            st.metric("Market Cap", market_cap_formatted)

    # AI Investment Recommendation
    st.markdown("---")
    recommendation = ai_analysis.get('investment_recommendation', {})

    # Color code the recommendation
    rec_action = recommendation.get('action', 'HOLD')
    color_map = {'BUY': 'green', 'HOLD': 'orange', 'SELL': 'red'}
    color = color_map.get(rec_action, 'gray')

    st.markdown(f"""
    ### 🎯 AI Investment Recommendation
    <div style="padding: 1rem; border-left: 5px solid {color}; background-color: rgba(128,128,128,0.1);">
    <h4 style="color: {color}; margin: 0;">{rec_action}</h4>
    <p style="margin: 0.5rem 0;"><strong>AI Potential Score:</strong> {recommendation.get('ai_score', 0)}/10</p>
    <p style="margin: 0;"><strong>Reasoning:</strong> {recommendation.get('reasoning', 'No reasoning provided')}</p>
    </div>
    """,
                unsafe_allow_html=True)

    # Key AI Metrics
    st.markdown("### 🤖 Key AI Metrics")

    col1, col2, col3, col4 = st.columns(4)
    ai_metrics = ai_analysis.get('ai_metrics', {})

    with col1:
        st.metric("AI Revenue Exposure",
                  f"{ai_metrics.get('ai_revenue_exposure', 0)}%")

    with col2:
        st.metric("AI Partnerships", ai_metrics.get('ai_partnerships', 0))

    with col3:
        st.metric("AI Patents", ai_metrics.get('ai_patents', 0))

    with col4:
        st.metric("AI Investment Score",
                  f"{ai_metrics.get('ai_investment_score', 0)}/10")

    # AI Strategy Analysis
    st.markdown("### 📈 AI Strategy & Opportunities")
    ai_story = ai_analysis.get('ai_story', {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**AI Strategy Summary:**")
        st.write(
            ai_story.get('strategy_summary',
                         'No AI strategy information available.'))

        st.markdown("**Key AI Use Cases:**")
        use_cases = ai_story.get('use_cases', [])
        if use_cases:
            for use_case in use_cases:
                st.write(f"• {use_case}")
        else:
            st.write("No specific AI use cases identified.")

    with col2:
        st.markdown("**AI Opportunities:**")
        opportunities = ai_story.get('opportunities', [])
        if opportunities:
            for opp in opportunities:
                st.write(f"• {opp}")
        else:
            st.write("No specific AI opportunities identified.")

        st.markdown("**Competitive AI Advantages:**")
        advantages = ai_story.get('competitive_advantages', [])
        if advantages:
            for adv in advantages:
                st.write(f"• {adv}")
        else:
            st.write("No specific competitive AI advantages identified.")

    # Stock Price Chart
    st.markdown("### 📊 Stock Price Performance")

    if not price_data.empty:
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(x=price_data.index,
                       y=price_data['Close'],
                       mode='lines',
                       name='Close Price',
                       line=dict(color='#1f77b4', width=2)))

        fig.update_layout(
            title=f"{company_info.get('symbol', 'Stock')} Price Chart",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            hovermode='x unified',
            showlegend=True)

        st.plotly_chart(fig, use_container_width=True)

    # Financial Data Table
    st.markdown("### 📋 Key Financial Data")

    # Prepare financial data for table
    financial_data = {
        'Metric': [
            'Current Price', 'Previous Close', 'Day High', 'Day Low', 'Volume',
            'Market Cap', 'P/E Ratio', 'EPS', 'Dividend Yield', 'Beta'
        ],
        'Value': [
            f"${company_info.get('currentPrice', 0):.2f}",
            f"${company_info.get('previousClose', 0):.2f}",
            f"${company_info.get('dayHigh', 0):.2f}",
            f"${company_info.get('dayLow', 0):.2f}",
            f"{company_info.get('volume', 0):,}",
            f"${company_info.get('marketCap', 0)/1e9:.2f}B"
            if company_info.get('marketCap', 0) > 0 else "N/A",
            f"{company_info.get('trailingPE', 0):.2f}"
            if company_info.get('trailingPE') else "N/A",
            f"${company_info.get('trailingEps', 0):.2f}"
            if company_info.get('trailingEps') else "N/A",
            f"{company_info.get('dividendYield', 0)*100:.2f}%"
            if company_info.get('dividendYield') else "N/A",
            f"{company_info.get('beta', 0):.2f}"
            if company_info.get('beta') else "N/A"
        ]
    }

    financial_df = pd.DataFrame(financial_data)
    st.dataframe(financial_df, use_container_width=True, hide_index=True)

    # Download Section
    st.markdown("### 💾 Download Data")

    col1, col2 = st.columns(2)

    with col1:
        # Download financial data
        csv_financial = financial_df.to_csv(index=False)
        st.download_button(
            label="📊 Download Financial Data (CSV)",
            data=csv_financial,
            file_name=
            f"{company_info.get('symbol', 'stock')}_financial_data.csv",
            mime="text/csv")

    with col2:
        # Download AI analysis
        ai_analysis_df = pd.DataFrame([{
            'Company':
            company_info.get('longName', 'Unknown'),
            'Symbol':
            company_info.get('symbol', 'N/A'),
            'AI Investment Recommendation':
            rec_action,
            'AI Score':
            recommendation.get('ai_score', 0),
            'AI Revenue Exposure %':
            ai_metrics.get('ai_revenue_exposure', 0),
            'AI Partnerships':
            ai_metrics.get('ai_partnerships', 0),
            'AI Patents':
            ai_metrics.get('ai_patents', 0),
            'AI Investment Score':
            ai_metrics.get('ai_investment_score', 0),
            'Analysis Date':
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }])

        csv_ai = ai_analysis_df.to_csv(index=False)
        st.download_button(
            label="🤖 Download AI Analysis (CSV)",
            data=csv_ai,
            file_name=f"{company_info.get('symbol', 'stock')}_ai_analysis.csv",
            mime="text/csv")


def display_401k_results(company_name, analysis):
    """Display comprehensive 401K analysis results"""

    # Company header
    st.header(f"💰 401K Analysis for {company_name}")

    # 401K Overview
    st.markdown("---")
    overview = analysis.get('overview', {})

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        match_rate = overview.get('match_percentage', 0)
        st.metric("Company Match", f"{match_rate}%")

    with col2:
        vesting_period = overview.get('vesting_period', 'Unknown')
        st.metric("Vesting Period", vesting_period)

    with col3:
        roth_available = overview.get('roth_available', False)
        roth_status = "✅ Available" if roth_available else "❌ Not Available"
        st.metric("Roth 401K", roth_status)

    with col4:
        max_match = overview.get('max_match_salary_percent', 0)
        st.metric("Max Match %", f"{max_match}%")

    # Investment Recommendation
    recommendation = analysis.get('recommendation', {})

    st.markdown("### 🎯 401K Optimization Recommendation")

    # Color code based on recommendation strength
    rec_score = recommendation.get('optimization_score', 5)
    if rec_score >= 8:
        color = 'green'
        status = 'Excellent'
    elif rec_score >= 6:
        color = 'orange'
        status = 'Good'
    else:
        color = 'red'
        status = 'Needs Improvement'

    st.markdown(f"""
    <div style="padding: 1rem; border-left: 5px solid {color}; background-color: rgba(128,128,128,0.1);">
    <h4 style="color: {color}; margin: 0;">401K Status: {status}</h4>
    <p style="margin: 0.5rem 0;"><strong>Optimization Score:</strong> {rec_score}/10</p>
    <p style="margin: 0;"><strong>Key Recommendation:</strong> {recommendation.get('primary_advice', 'No recommendation available')}</p>
    </div>
    """,
                unsafe_allow_html=True)

    # Detailed Analysis
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 💡 Contribution Strategy")
        strategy = analysis.get('contribution_strategy', {})

        st.markdown("**Recommended Actions:**")
        actions = strategy.get('recommended_actions', [])
        if actions:
            for action in actions:
                st.write(f"• {action}")
        else:
            st.write("No specific actions identified.")

        st.markdown("**Annual Savings Potential:**")
        savings_potential = strategy.get('annual_savings_potential',
                                         'Not calculated')
        st.write(f"💰 {savings_potential}")

    with col2:
        st.markdown("### 🔄 Roth vs Traditional Analysis")
        roth_analysis = analysis.get('roth_analysis', {})

        st.markdown("**Recommendation:**")
        roth_rec = roth_analysis.get('recommendation', 'Traditional')
        st.write(f"📊 **{roth_rec}** is recommended for you")

        st.markdown("**Reasoning:**")
        reasoning = roth_analysis.get('reasoning', 'No analysis available')
        st.write(reasoning)

    # Fund Options
    st.markdown("### 🏦 Available Investment Options")
    fund_options = analysis.get('fund_options', {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Recommended Funds:**")
        recommended = fund_options.get('recommended_funds', [])
        if recommended:
            for fund in recommended:
                st.write(f"• {fund}")
        else:
            st.write("No specific fund recommendations available.")

    with col2:
        st.markdown("**Fund Categories Available:**")
        categories = fund_options.get('fund_categories', [])
        if categories:
            for category in categories:
                st.write(f"• {category}")
        else:
            st.write("Fund information not available.")

    # Additional Benefits
    st.markdown("### ➕ Additional Benefits")
    additional = analysis.get('additional_benefits', {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Other Retirement Benefits:**")
        other_benefits = additional.get('other_benefits', [])
        if other_benefits:
            for benefit in other_benefits:
                st.write(f"• {benefit}")
        else:
            st.write("No additional benefits identified.")

    with col2:
        st.markdown("**Company Perks:**")
        perks = additional.get('financial_wellness_perks', [])
        if perks:
            for perk in perks:
                st.write(f"• {perk}")
        else:
            st.write("No financial wellness perks identified.")

    # Download Section
    st.markdown("### 💾 Download 401K Analysis")

    # Create downloadable report
    report_data = {
        'Company': [company_name],
        'Match Percentage': [overview.get('match_percentage', 0)],
        'Vesting Period': [overview.get('vesting_period', 'Unknown')],
        'Roth Available': [overview.get('roth_available', False)],
        'Max Match Salary %': [overview.get('max_match_salary_percent', 0)],
        'Optimization Score': [rec_score],
        'Primary Recommendation':
        [recommendation.get('primary_advice', 'No recommendation')],
        'Roth vs Traditional':
        [roth_analysis.get('recommendation', 'Traditional')],
        'Annual Savings Potential':
        [strategy.get('annual_savings_potential', 'Not calculated')],
        'Analysis Date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    }

    report_df = pd.DataFrame(report_data)
    csv_report = report_df.to_csv(index=False)

    st.download_button(
        label="📊 Download 401K Analysis Report (CSV)",
        data=csv_report,
        file_name=f"{company_name.replace(' ', '_')}_401k_analysis.csv",
        mime="text/csv")


if __name__ == "__main__":
    main()
