import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(layout="wide", page_title="Election Strategy Dashboard")

# Sample data
correlation_data = pd.DataFrame([
    {"asset": "XLF", "trumpCorr": 0.72, "harrisCorr": -0.45},
    {"asset": "XLE", "trumpCorr": 0.65, "harrisCorr": -0.38},
    {"asset": "IWM", "trumpCorr": 0.58, "harrisCorr": -0.42},
    {"asset": "XLI", "trumpCorr": 0.52, "harrisCorr": -0.35},
    {"asset": "XLB", "trumpCorr": 0.48, "harrisCorr": -0.31},
    {"asset": "QQQ", "trumpCorr": -0.45, "harrisCorr": 0.62},
    {"asset": "XLK", "trumpCorr": -0.42, "harrisCorr": 0.58},
    {"asset": "XLV", "trumpCorr": -0.38, "harrisCorr": 0.45},
])

portfolio_allocation = pd.DataFrame([
    {"asset": "XLF", "long": 0.65, "short": 0.35, "net": 0.30},
    {"asset": "XLE", "long": 0.60, "short": 0.40, "net": 0.20},
    {"asset": "IWM", "long": 0.55, "short": 0.45, "net": 0.10},
    {"asset": "QQQ", "long": 0.35, "short": 0.65, "net": -0.30},
    {"asset": "XLK", "long": 0.40, "short": 0.60, "net": -0.20},
])

beta_deviation_data = pd.DataFrame([
    {"asset": "XLF", "theoreticalBeta": 1.2, "eventBeta": 1.4, "deviation": 0.2},
    {"asset": "XLE", "theoreticalBeta": 1.1, "eventBeta": 1.25, "deviation": 0.15},
    {"asset": "IWM", "theoreticalBeta": 1.15, "eventBeta": 1.35, "deviation": 0.20},
    {"asset": "QQQ", "theoreticalBeta": 1.05, "eventBeta": 0.85, "deviation": -0.20},
    {"asset": "XLK", "theoreticalBeta": 1.1, "eventBeta": 0.95, "deviation": -0.15},
])

# Dashboard title
st.title("Election Strategy Analysis Dashboard")

# Create two columns for the first row
col1, col2 = st.columns(2)

# Asset Correlations
with col1:
    st.subheader("Asset Correlations with Candidate Odds")
    fig_corr = go.Figure()
    fig_corr.add_trace(go.Bar(
        x=correlation_data['asset'],
        y=correlation_data['trumpCorr'],
        name='Trump Correlation',
        marker_color='red'
    ))
    fig_corr.add_trace(go.Bar(
        x=correlation_data['asset'],
        y=correlation_data['harrisCorr'],
        name='Harris-Biden Correlation',
        marker_color='blue'
    ))
    fig_corr.update_layout(barmode='group', height=400)
    st.plotly_chart(fig_corr, use_container_width=True)

# Portfolio Allocations
with col2:
    st.subheader("Portfolio Allocations")
    fig_portfolio = go.Figure()
    fig_portfolio.add_trace(go.Bar(
        x=portfolio_allocation['asset'],
        y=portfolio_allocation['long'],
        name='Long Allocation',
        marker_color='green'
    ))
    fig_portfolio.add_trace(go.Bar(
        x=portfolio_allocation['asset'],
        y=portfolio_allocation['short'],
        name='Short Allocation',
        marker_color='red'
    ))
    fig_portfolio.add_trace(go.Scatter(
        x=portfolio_allocation['asset'],
        y=portfolio_allocation['net'],
        name='Net Exposure',
        mode='lines+markers',
        line=dict(color='purple', width=2)
    ))
    fig_portfolio.update_layout(barmode='stack', height=400)
    st.plotly_chart(fig_portfolio, use_container_width=True)

# Create two columns for the second row
col3, col4 = st.columns(2)

# Beta Deviations
with col3:
    st.subheader("Beta Deviations During Events")
    fig_beta = go.Figure()
    fig_beta.add_trace(go.Scatter(
        x=beta_deviation_data['theoreticalBeta'],
        y=beta_deviation_data['eventBeta'],
        mode='markers+text',
        text=beta_deviation_data['asset'],
        textposition='top center',
        name='Beta Comparison',
        marker=dict(size=10, color='purple')
    ))
    # Add diagonal line
    fig_beta.add_trace(go.Scatter(
        x=[0.8, 1.4],
        y=[0.8, 1.4],
        mode='lines',
        name='No Deviation Line',
        line=dict(color='gray', dash='dash')
    ))
    fig_beta.update_layout(
        height=400,
        xaxis_title="Theoretical Beta",
        yaxis_title="Event Beta"
    )
    st.plotly_chart(fig_beta, use_container_width=True)

# Expected Alpha
with col4:
    st.subheader("Expected Alpha by Asset (%)")
    fig_alpha = go.Figure()
    colors = ['green' if x > 0 else 'red' for x in beta_deviation_data['deviation']]
    fig_alpha.add_trace(go.Bar(
        x=beta_deviation_data['asset'],
        y=beta_deviation_data['deviation'] * 100,  # Convert to percentage
        marker_color=colors,
        name='Expected Alpha'
    ))
    fig_alpha.update_layout(height=400)
    st.plotly_chart(fig_alpha, use_container_width=True)

# Add metrics summary
st.subheader("Key Metrics Summary")
metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

with metrics_col1:
    st.metric(
        "Highest Trump Correlation",
        f"{correlation_data['trumpCorr'].max():.2f}",
        f"{correlation_data.loc[correlation_data['trumpCorr'].idxmax(), 'asset']}"
    )

with metrics_col2:
    st.metric(
        "Highest Harris Correlation",
        f"{correlation_data['harrisCorr'].max():.2f}",
        f"{correlation_data.loc[correlation_data['harrisCorr'].idxmax(), 'asset']}"
    )

with metrics_col3:
    st.metric(
        "Largest Beta Deviation",
        f"{beta_deviation_data['deviation'].abs().max():.2f}",
        f"{beta_deviation_data.loc[beta_deviation_data['deviation'].abs().idxmax(), 'asset']}"
    )

with metrics_col4:
    st.metric(
        "Largest Net Exposure",
        f"{portfolio_allocation['net'].abs().max():.2f}",
        f"{portfolio_allocation.loc[portfolio_allocation['net'].abs().idxmax(), 'asset']}"
    )