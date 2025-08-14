import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# ✅ Fix for large DataFrame rendering
pd.set_option("styler.render.max_elements", 1000000)

st.set_page_config(page_title="Supermarket Dashboard", layout="wide")

# ✅ Simple, Clean Theme
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .stMetric {
        background-color: #262730;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #4a4a4a;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin: 8px 0;
    }
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        border-color: #00d4ff;
    }
    .metric-label {
        color: #00d4ff;
        font-size: 14px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }
    .metric-value {
        color: white;
        font-size: 26px;
        font-weight: bold;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    .metric-delta {
        color: #51cf66;
        font-size: 12px;
        font-weight: 600;
        background: rgba(81, 207, 102, 0.1);
        padding: 2px 8px;
        border-radius: 12px;
        display: inline-block;
        margin-top: 5px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        padding: 8px 16px;
        box-shadow: 0 2px 8px rgba(0, 212, 255, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.4);
    }
    .stSelectbox > div > div {
        background: #262730;
        border: 1px solid #4a4a4a;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .stSelectbox > div > div:hover {
        border-color: #00d4ff;
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.2);
    }
    .stSlider > div > div > div > div {
        background: #00d4ff;
        box-shadow: 0 2px 4px rgba(0, 212, 255, 0.3);
    }
    .stCheckbox > div > div {
        background: #262730;
        border: 1px solid #4a4a4a;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    .stCheckbox > div > div:hover {
        border-color: #00d4ff;
    }
    .stDataFrame {
        background: #262730;
        border-radius: 12px;
        border: 1px solid #4a4a4a;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        overflow: hidden;
    }
    

    
    .correlation-metric {
        background: linear-gradient(135deg, #262730 0%, #1e1e2e 100%);
        border: 1px solid #4a4a4a;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .correlation-metric:hover {
        border-color: #00d4ff;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }
    }
    .stDataFrame:hover {
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }
    .stAlert {
        background: #262730;
        border: 1px solid #4a4a4a;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        padding: 15px;
        margin: 10px 0;
    }
    .stSuccess {
        background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        border: none;
        color: white;
        box-shadow: 0 4px 12px rgba(81, 207, 102, 0.3);
    }
    .stWarning {
        background: linear-gradient(135deg, #ffd43b 0%, #fcc419 100%);
        border: none;
        color: #333;
        box-shadow: 0 4px 12px rgba(255, 212, 59, 0.3);
    }
    .stInfo {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        border: none;
        color: white;
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
    }
    .stError {
        background: linear-gradient(135deg, #ff6b6b 0%, #fa5252 100%);
        border: none;
        color: white;
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
    }
    .header-glow {
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #00d4ff 50%, transparent 100%);
        margin: 20px 0;
        border-radius: 1px;
    }
    .metric-container {
        background: linear-gradient(135deg, #262730 0%, #1e1e2e 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #4a4a4a;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        margin: 15px 0;
    }
    .chart-container {
        background: linear-gradient(135deg, #262730 0%, #1e1e2e 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #4a4a4a;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    .chart-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        border-color: #00d4ff;
    }
    .sidebar-section {
        background: linear-gradient(135deg, #262730 0%, #1e1e2e 100%);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #4a4a4a;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .sidebar-section:hover {
        border-color: #00d4ff;
        box-shadow: 0 6px 18px rgba(0, 212, 255, 0.2);
    }
    .footer-glow {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #262730 0%, #1e1e2e 100%);
        border-radius: 12px;
        border: 1px solid #4a4a4a;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="header-glow">Supermarket Inventory Dashboard</h1>', unsafe_allow_html=True)

# ✅ Load Data
@st.cache_data
def load_data():
    return pd.read_csv("multi_product_results_all_policies.csv")

df = load_data()

# ✅ Simple Sidebar
with st.sidebar:
    st.header("Filters")
    
    # Policy Filter
    if "Donation Policy" in df.columns:
        policies = ["All Policies"] + sorted(df["Donation Policy"].dropna().unique().tolist())
        selected_policy = st.selectbox("Select Policy", policies)
    
    # Product Filter
    products = df["Product"].unique()
    selected_product = st.selectbox("Select Product", products)
    
    # Theta Set Filter
    if "theta_set_type" in df.columns:
        theta_options = ["All Data", "Regular Customers", "Extreme Customers"]
        selected_theta = st.selectbox("Customer Type", theta_options)
    
    # Markdown Policy Filter
    if "Markdown Policy" in df.columns:
        markdown_policies = ["All Markdown Policies"] + sorted(df["Markdown Policy"].dropna().unique().tolist())
        selected_markdown = st.selectbox("Select Markdown Policy", markdown_policies)
    
    # Scenario Filter
    if "Scenario" in df.columns:
        scenarios = ["All Scenarios"] + sorted(df["Scenario"].dropna().unique().tolist())
        selected_scenario = st.selectbox("Select Scenario", scenarios)
    
    # ✅ Add Day Navigation
    st.header("Day Navigation")
    
    if "current_day" not in st.session_state:
        st.session_state.current_day = 1
    
    # Day slider
    max_day = int(df["Day"].max()) if "Day" in df.columns else 90
    selected_day = st.slider("Select Day", 1, max_day, st.session_state.current_day)
    if selected_day != st.session_state.current_day:
        st.session_state.current_day = selected_day
    
    # Day navigation buttons
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("⬅️ Prev"):
            st.session_state.current_day = max(1, st.session_state.current_day - 1)
    with col_next:
        if st.button("Next ➡️"):
            st.session_state.current_day = min(max_day, st.session_state.current_day + 1)
    
    # ✅ Add Customer Simulation Controls
    st.header("Customer Simulation")
    
    customers_per_day = st.slider("Customers per Day", 1, 100, 25)
    

    
    # Show current day info
    st.markdown(f"""
    <div style="background: rgba(0,212,255,0.05); 
                border: 1px solid #4a4a4a; 
                border-radius: 8px; 
                padding: 15px; 
                margin: 15px 0;">
                        <h4 style="color: #00d4ff; margin-bottom: 10px;">Current Simulation Status</h4>
        <p style="color: white; margin: 5px 0;">
            <strong>Current Day:</strong> {st.session_state.current_day}
        </p>
        <p style="color: white; margin: 5px 0;">
            <strong>Customers:</strong> {customers_per_day} per day
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ✅ Add Simulation Controls
    st.header("Simulation Controls")
    
    show_cumulative = st.checkbox("Show Cumulative Stats", value=False)
    show_animation = st.checkbox("Show Customer Animation", value=True)
    
    # Simulation speed
    animation_speed = st.slider("Animation Speed", 0.01, 0.1, 0.03, 0.01)
    
    # Advanced Analysis Features
    st.header("Advanced Analysis")
    
    show_correlation_analysis = st.checkbox("Show Correlation Analysis", value=False)
    show_policy_ranking = st.checkbox("Show Policy Efficiency Ranking", value=False)
    show_customer_sensitivity = st.checkbox("Show Customer Sensitivity Analysis", value=False)
    show_markdown_analysis = st.checkbox("Show Markdown Policy Analysis", value=False)

# ✅ Filter Data
filtered_df = df[df["Product"] == selected_product]

if selected_policy != "All Policies":
    filtered_df = filtered_df[filtered_df["Donation Policy"] == selected_policy]

if selected_theta == "Regular Customers":
    filtered_df = filtered_df[filtered_df["theta_set_type"] == "Regular"]
elif selected_theta == "Extreme Customers":
    filtered_df = filtered_df[filtered_df["theta_set_type"] == "Extreme"]

# Apply markdown policy filter
if selected_markdown != "All Markdown Policies":
    filtered_df = filtered_df[filtered_df["Markdown Policy"] == selected_markdown]

# Apply scenario filter
if selected_scenario != "All Scenarios":
    if "scenario_id" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["scenario_id"] == int(selected_scenario)]
    elif "Scenario" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Scenario"] == selected_scenario]

# ✅ Main Dashboard
if not filtered_df.empty:

    
    # Calculate totals based on cumulative or daily view
    if show_cumulative:
        # Calculate cumulative totals
        cumulative_df = filtered_df.copy()
        cumulative_df['Sold (Cumulative)'] = cumulative_df['Sold (Today)'].cumsum()
        cumulative_df['Donated (Cumulative)'] = cumulative_df['Donated (Today)'].cumsum()
        cumulative_df['Wasted (Cumulative)'] = cumulative_df['Wasted (Today)'].cumsum()
        cumulative_df['Revenue (Cumulative)'] = cumulative_df['Daily Revenue'].cumsum()
        
        # Use cumulative totals
        total_sold = cumulative_df['Sold (Cumulative)'].iloc[-1]
        total_donated = cumulative_df['Donated (Cumulative)'].iloc[-1]
        total_wasted = cumulative_df['Wasted (Cumulative)'].iloc[-1]
        total_revenue = cumulative_df['Revenue (Cumulative)'].iloc[-1]
        
        # Calculate averages
        avg_daily_sold = total_sold / len(filtered_df)
        avg_daily_donated = total_donated / len(filtered_df)
        avg_daily_wasted = total_wasted / len(filtered_df)
        avg_daily_revenue = total_revenue / len(filtered_df)
        
        metric_suffix = " (Total)"
    else:
        # Use daily totals
        total_sold = filtered_df["Sold (Today)"].sum()
        total_donated = filtered_df["Donated (Today)"].sum()
        total_wasted = filtered_df["Wasted (Today)"].sum()
        total_revenue = filtered_df["Daily Revenue"].sum()
        
        # Calculate averages
        avg_daily_sold = filtered_df["Sold (Today)"].mean()
        avg_daily_donated = filtered_df["Donated (Today)"].mean()
        avg_daily_wasted = filtered_df["Wasted (Today)"].mean()
        avg_daily_revenue = filtered_df["Daily Revenue"].mean()
        
        metric_suffix = " (Total)"
    
    # Calculate percentages
    total_units = total_sold + total_donated + total_wasted
    sold_pct = (total_sold / total_units) * 100 if total_units > 0 else 0
    donated_pct = (total_donated / total_units) * 100 if total_units > 0 else 0
    wasted_pct = (total_wasted / total_units) * 100 if total_units > 0 else 0
    
    # ✅ Key Metrics
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.header(f"Key Performance Metrics{metric_suffix}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Sold",
            value=f"{total_sold:,}",
            delta=f"{sold_pct:.1f}% of total"
        )
    
    with col2:
        st.metric(
            label="Total Donated", 
            value=f"{total_donated:,}",
            delta=f"{donated_pct:.1f}% of total"
        )
    
    with col3:
        st.metric(
            label="Total Wasted",
            value=f"{total_wasted:,}",
            delta=f"{wasted_pct:.1f}% of total"
        )
    
    with col4:
        st.metric(
            label="Total Revenue",
            value=f"€{total_revenue:,.0f}",
            delta=f"€{avg_daily_revenue:.0f} avg/day"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # NEW: Daily Metrics Section
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.header("Daily Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Avg Daily Sold",
            value=f"{avg_daily_sold:.1f}",
            delta=f"per day"
        )
    
    with col2:
        st.metric(
            label="Avg Daily Donated", 
            value=f"{avg_daily_donated:.1f}",
            delta=f"per day"
        )
    
    with col3:
        st.metric(
            label="Avg Daily Wasted",
            value=f"{avg_daily_wasted:.1f}",
            delta=f"per day"
        )
    
    with col4:
        st.metric(
            label="Avg Daily Revenue",
            value=f"€{avg_daily_revenue:.1f}",
            delta=f"per day"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    

    
    # ✅ Product Distribution with View Toggle
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.header("Product Distribution")
    
    # Default to pie chart if no button is pressed
    if 'pie_view' not in st.session_state:
        st.session_state.pie_view = True
        st.session_state.bar_view = False
        st.session_state.line_view = False
    
    # Create different chart types
    if st.session_state.pie_view:
        fig_dist = px.pie(
            values=[total_sold, total_donated, total_wasted],
            names=['Sold', 'Donated', 'Wasted'],
            color_discrete_map={'Sold': '#00d4ff', 'Donated': '#51cf66', 'Wasted': '#ff6b6b'}
        )
        
        # Enhanced tooltips for pie chart
        fig_dist.update_traces(
            hovertemplate="<b>%{label}</b><br>" +
                         "<b>Count:</b> %{value:,.0f}<br>" +
                         "<b>Percentage:</b> %{percent:.2%}<br>" +
                         "<extra></extra>",
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.9)",
                bordercolor="#00d4ff",
                font_size=12,
                font_family="Arial"
            )
        )
    
    elif st.session_state.bar_view:
        fig_dist = px.bar(
            x=['Sold', 'Donated', 'Wasted'],
            y=[total_sold, total_donated, total_wasted],
            color=['Sold', 'Donated', 'Wasted'],
            color_discrete_map={'Sold': '#00d4ff', 'Donated': '#51cf66', 'Wasted': '#ff6b6b'}
        )
        
        # Enhanced tooltips for bar chart
        fig_dist.update_traces(
            hovertemplate="<b>%{x}</b><br>" +
                         "<b>Count:</b> %{y:,.0f}<br>" +
                         "<extra></extra>",
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.9)",
                bordercolor="#00d4ff",
                font_size=12,
                font_family="Arial"
            )
        )
    
    else:  # st.session_state.line_view
        fig_dist = px.line(
            x=['Sold', 'Donated', 'Wasted'],
            y=[total_sold, total_donated, total_wasted],
            markers=True
        )
        
        # Enhanced tooltips for line chart
        fig_dist.update_traces(
            hovertemplate="<b>%{x}</b><br>" +
                         "<b>Count:</b> %{y:,.0f}<br>" +
                         "<extra></extra>",
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.9)",
                bordercolor="#00d4ff",
                font_size=12,
                font_family="Arial"
            ),
            line=dict(width=3),
            mode='lines+markers'
        )
    
    # Common layout for all chart types
    fig_dist.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title="Category"
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title="Count"
        ),
        hovermode='closest'
    )
    
    st.plotly_chart(fig_dist, use_container_width=True)
    
    # View toggle buttons below the chart (centered)
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col2:
        if st.button("Pie Chart", key="pie_btn"):
            st.session_state.pie_view = True
            st.session_state.bar_view = False
            st.session_state.line_view = False
            st.rerun()
    with col3:
        if st.button("Bar Chart", key="bar_btn"):
            st.session_state.pie_view = False
            st.session_state.bar_view = True
            st.session_state.line_view = False
            st.rerun()
    with col4:
        if st.button("Line Chart", key="line_btn"):
            st.session_state.pie_view = False
            st.session_state.bar_view = False
            st.session_state.line_view = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ✅ Daily Trends with View Toggle
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.header("Daily Trends")
    
    # Sample data for trend (last 30 days if available)
    trend_df = filtered_df.tail(30) if len(filtered_df) > 30 else filtered_df
    
    # Default to line chart if no button is pressed
    if 'line_trend_view' not in st.session_state:
        st.session_state.line_trend_view = True
        st.session_state.bar_trend_view = False
        st.session_state.area_trend_view = False
    
    # Create different chart types
    if st.session_state.line_trend_view:
        fig_trend = px.line(
            trend_df,
            x="Day",
            y=["Sold (Today)", "Donated (Today)", "Wasted (Today)"],
            template="plotly_dark"
        )
        
        # Enhanced tooltips for line chart
        fig_trend.update_traces(
            hovertemplate="<b>%{fullData.name}</b><br>" +
                         "<b>Day:</b> %{x}<br>" +
                         "<b>Count:</b> %{y:,.0f}<br>" +
                         "<extra></extra>",
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.9)",
                bordercolor="#00d4ff",
                font_size=12,
                font_family="Arial"
            ),
            line=dict(width=3),
            mode='lines+markers'
        )
    
    elif st.session_state.bar_trend_view:
        fig_trend = px.bar(
            trend_df,
            x="Day",
            y=["Sold (Today)", "Donated (Today)", "Wasted (Today)"],
            barmode='group',
            template="plotly_dark"
        )
        
        # Enhanced tooltips for bar chart
        fig_trend.update_traces(
            hovertemplate="<b>%{fullData.name}</b><br>" +
                         "<b>Day:</b> %{x}<br>" +
                         "<b>Count:</b> %{y:,.0f}<br>" +
                         "<extra></extra>",
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.9)",
                bordercolor="#00d4ff",
                font_size=12,
                font_family="Arial"
            )
        )
    
    else:  # st.session_state.area_trend_view
        fig_trend = px.area(
            trend_df,
            x="Day",
            y=["Sold (Today)", "Donated (Today)", "Wasted (Today)"],
            template="plotly_dark"
        )
        
        # Enhanced tooltips for area chart
        fig_trend.update_traces(
            hovertemplate="<b>%{fullData.name}</b><br>" +
                         "<b>Day:</b> %{x}<br>" +
                         "<b>Count:</b> %{y:,.0f}<br>" +
                         "<extra></extra>",
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.9)",
                bordercolor="#00d4ff",
                font_size=12,
                font_family="Arial"
            )
        )
    
    # Common layout for all chart types
    fig_trend.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title="Day"
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            title="Count"
        ),
        hovermode='closest'
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # View toggle buttons below the chart (centered)
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col2:
        if st.button("Line Chart", key="line_trend_btn"):
            st.session_state.line_trend_view = True
            st.session_state.bar_trend_view = False
            st.session_state.area_trend_view = False
            st.rerun()
    with col3:
        if st.button("Bar Chart", key="bar_trend_btn"):
            st.session_state.line_trend_view = False
            st.session_state.bar_trend_view = True
            st.session_state.area_trend_view = False
            st.rerun()
    with col4:
        if st.button("Area Chart", key="area_trend_btn"):
            st.session_state.line_trend_view = False
            st.session_state.bar_trend_view = False
            st.session_state.area_trend_view = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ✅ Data Table
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.header("Data Table")
    
    # Show a manageable sample of the data
    if len(filtered_df) > 50:
        st.markdown(f"""
        <div style="background: rgba(0,212,255,0.05); 
                    border: 1px solid #4a4a4a; 
                    border-radius: 8px; 
                    padding: 15px; 
                    margin: 15px 0;">
            <h4 style="color: #00d4ff; margin-bottom: 5px;">Dataset Information</h4>
            <p style="color: white; margin: 5px 0;">
                <strong>Dataset Size:</strong> Showing <strong>first 50 rows</strong> of <strong>{len(filtered_df):,} total rows</strong>
            </p>
            <p style="color: white; margin: 5px 0;">
                <strong>Data Management:</strong> Use filters above to narrow down results or download full dataset
            </p>
        </div>
        """, unsafe_allow_html=True)
        display_table = filtered_df.head(50)
    else:
        st.markdown(f"""
        <div style="background: rgba(0,212,255,0.05); 
                    border: 1px solid #4a4a4a; 
                    border-radius: 8px; 
                    padding: 15px; 
                    margin: 15px 0;">
            <h4 style="color: #00d4ff; margin-bottom: 5px;">Dataset Information</h4>
            <p style="color: white; margin: 5px 0;">
                <strong>Dataset Size:</strong> Showing all <strong>{len(filtered_df):,} rows</strong> of filtered data
            </p>
            <p style="color: white; margin: 5px 0;">
                <strong>Data Management:</strong> All data fits in view - no pagination needed
            </p>
        </div>
        """, unsafe_allow_html=True)
        display_table = filtered_df
    
    # Select key columns for display
    key_columns = ["Day", "Donation Policy", "Sold (Today)", "Donated (Today)", "Wasted (Today)", "Daily Revenue"]
    available_columns = [col for col in key_columns if col in display_table.columns]
    
    # Add theta set info if available
    if "theta_set_type" in display_table.columns:
        available_columns.append("theta_set_type")
    
    # Display the table
    st.dataframe(
        display_table[available_columns],
        use_container_width=True,
        height=400
    )
    
    # Show download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"supermarket_data_{selected_product}_{selected_policy}.csv",
        mime="text/csv"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ✅ Policy Comparison with View Toggle (if multiple policies)
    if selected_policy == "All Policies" and "Donation Policy" in df.columns:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.header("Policy Comparison")
        
        policy_summary = df[df["Product"] == selected_product].groupby("Donation Policy").agg({
            "Sold (Today)": "sum",
            "Donated (Today)": "sum",
            "Wasted (Today)": "sum"
        }).reset_index()
        
        # Calculate percentages for each policy
        for idx, row in policy_summary.iterrows():
            total = row["Sold (Today)"] + row["Donated (Today)"] + row["Wasted (Today)"]
            if total > 0:
                policy_summary.loc[idx, "Sold %"] = (row["Sold (Today)"] / total) * 100
                policy_summary.loc[idx, "Donated %"] = (row["Donated (Today)"] / total) * 100
                policy_summary.loc[idx, "Wasted %"] = (row["Wasted (Today)"] / total) * 100
        
        # Default to stacked bar chart if no button is pressed
        if 'policy_bar_view' not in st.session_state:
            st.session_state.policy_bar_view = True
            st.session_state.policy_line_view = False
            st.session_state.policy_pie_view = False
        
        # Create different chart types
        if st.session_state.policy_bar_view:
            fig_policy = px.bar(
                policy_summary,
                x="Donation Policy",
                y=["Sold %", "Donated %", "Wasted %"],
                barmode='stack',
                color_discrete_map={'Sold %': '#00d4ff', 'Donated %': '#51cf66', 'Wasted %': '#ff6b6b'}
            )
            
            # Enhanced tooltips for bar chart
            fig_policy.update_traces(
                hovertemplate="<b>%{fullData.name}</b><br>" +
                             "<b>Policy:</b> %{x}<br>" +
                             "<b>Percentage:</b> %{y:.2f}%<br>" +
                             "<extra></extra>",
                hoverlabel=dict(
                    bgcolor="rgba(0,0,0,0.9)",
                    bordercolor="#00d4ff",
                    font_size=12,
                    font_family="Arial"
                )
            )
        
        elif st.session_state.policy_line_view:
            fig_policy = px.line(
                policy_summary,
                x="Donation Policy",
                y=["Sold %", "Donated %", "Wasted %"],
                markers=True
            )
            
            # Enhanced tooltips for line chart
            fig_policy.update_traces(
                hovertemplate="<b>%{fullData.name}</b><br>" +
                             "<b>Policy:</b> %{x}<br>" +
                             "<b>Percentage:</b> %{y:.2f}%<br>" +
                             "<extra></extra>",
                hoverlabel=dict(
                    bgcolor="rgba(0,0,0,0.9)",
                    bordercolor="#00d4ff",
                    font_size=12,
                    font_family="Arial"
                ),
                line=dict(width=3),
                mode='lines+markers'
            )
        
        else:  # st.session_state.policy_pie_view
            # For pie chart, we need to create separate charts for each policy
            fig_policy = px.pie(
                values=policy_summary.iloc[0][["Sold %", "Donated %", "Wasted %"]].values,
                names=["Sold %", "Donated %", "Wasted %"],
                color_discrete_map={'Sold %': '#00d4ff', 'Donated %': '#51cf66', 'Wasted %': '#ff6b6b'}
            )
            
            # Enhanced tooltips for pie chart
            fig_policy.update_traces(
                hovertemplate="<b>%{label}</b><br>" +
                             "<b>Percentage:</b> %{value:.2f}%<br>" +
                             "<extra></extra>",
                hoverlabel=dict(
                    bgcolor="rgba(0,0,0,0.9)",
                    bordercolor="#00d4ff",
                    font_size=12,
                    font_family="Arial"
                )
            )
        
        # Common layout for all chart types
        fig_policy.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                title="Donation Policy"
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                title="Percentage (%)"
            ),
            hovermode='closest'
        )
        
        st.plotly_chart(fig_policy, use_container_width=True)
        
        # View toggle buttons below the chart (centered)
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col2:
            if st.button("Stacked Bar", key="policy_bar_btn"):
                st.session_state.policy_bar_view = True
                st.session_state.policy_line_view = False
                st.session_state.policy_pie_view = False
                st.rerun()
        with col3:
            if st.button("Line Chart", key="policy_line_btn"):
                st.session_state.policy_bar_view = False
                st.session_state.policy_line_view = True
                st.session_state.policy_pie_view = False
                st.rerun()
        with col4:
            if st.button("Pie Chart", key="policy_pie_btn"):
                st.session_state.policy_bar_view = False
                st.session_state.policy_line_view = False
                st.session_state.policy_pie_view = True
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Advanced Analysis Sections
    if show_correlation_analysis:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.header("Correlation Analysis")
        
        if len(filtered_df) > 0:
            # Calculate correlations
            revenue_waste_corr = filtered_df['Daily Revenue'].corr(filtered_df['Wasted (Today)'])
            revenue_donations_corr = filtered_df['Daily Revenue'].corr(filtered_df['Donated (Today)'])
            waste_donations_corr = filtered_df['Wasted (Today)'].corr(filtered_df['Donated (Today)'])
            
            # Display correlation metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Revenue vs Waste", f"{revenue_waste_corr:.3f}")
            with col2:
                st.metric("Revenue vs Donations", f"{revenue_donations_corr:.3f}")
            with col3:
                st.metric("Waste vs Donations", f"{waste_donations_corr:.3f}")
            
            # Default to heatmap if no button is pressed
            if 'corr_heatmap_view' not in st.session_state:
                st.session_state.corr_heatmap_view = True
                st.session_state.corr_scatter_view = False
                st.session_state.corr_bar_view = False
            
            # Create correlation heatmap
            corr_matrix = filtered_df[['Daily Revenue', 'Wasted (Today)', 'Donated (Today)']].corr()
            
            # Create different chart types
            if st.session_state.corr_heatmap_view:
                fig_corr = px.imshow(
                    corr_matrix,
                    color_continuous_scale='RdBu',
                    aspect='auto'
                )
                
                # Enhanced tooltips for correlation heatmap
                fig_corr.update_traces(
                    hovertemplate="<b>Correlation</b><br>" +
                                 "<b>Variable 1:</b> %{x}<br>" +
                                 "<b>Variable 2:</b> %{y}<br>" +
                                 "<b>Correlation:</b> %{z:.3f}<br>" +
                                 "<extra></extra>",
                    hoverlabel=dict(
                        bgcolor="rgba(0,0,0,0.9)",
                        bordercolor="#00d4ff",
                        font_size=12,
                        font_family="Arial"
                    )
                )
            
            elif st.session_state.corr_scatter_view:
                # Create scatter plot matrix
                fig_corr = px.scatter_matrix(
                    filtered_df[['Daily Revenue', 'Wasted (Today)', 'Donated (Today)']],
                    color_discrete_sequence=['#00d4ff']
                )
                
                # Enhanced tooltips for scatter plot
                fig_corr.update_traces(
                    hovertemplate="<b>%{fullData.name}</b><br>" +
                                 "<b>Value:</b> %{y}<br>" +
                                 "<extra></extra>",
                    hoverlabel=dict(
                        bgcolor="rgba(0,0,0,0.9)",
                        bordercolor="#00d4ff",
                        font_size=12,
                        font_family="Arial"
                    )
                )
            
            else:  # st.session_state.corr_bar_view
                # Create bar chart of correlation values
                corr_values = [revenue_waste_corr, revenue_donations_corr, waste_donations_corr]
                corr_names = ['Revenue vs Waste', 'Revenue vs Donations', 'Waste vs Donations']
                
                fig_corr = px.bar(
                    x=corr_names,
                    y=corr_values,
                    color=corr_values,
                    color_continuous_scale='RdBu'
                )
                
                # Enhanced tooltips for bar chart
                fig_corr.update_traces(
                    hovertemplate="<b>%{x}</b><br>" +
                                 "<b>Correlation:</b> %{y:.3f}<br>" +
                                 "<extra></extra>",
                    hoverlabel=dict(
                        bgcolor="rgba(0,0,0,0.9)",
                        bordercolor="#00d4ff",
                        font_size=12,
                        font_family="Arial"
                    )
                )
            
            # Common layout for all chart types
            fig_corr.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)', 
                font=dict(color='white'),
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    title="Variables"
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    title="Correlation"
                ),
                hovermode='closest'
            )
            
            st.plotly_chart(fig_corr, use_container_width=True, key="correlation_heatmap")
            
            # View toggle buttons below the chart (centered)
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
            with col2:
                if st.button("Heatmap", key="corr_heatmap_btn"):
                    st.session_state.corr_heatmap_view = True
                    st.session_state.corr_scatter_view = False
                    st.session_state.corr_bar_view = False
                    st.rerun()
            with col3:
                if st.button("Scatter Matrix", key="corr_scatter_btn"):
                    st.session_state.corr_heatmap_view = False
                    st.session_state.corr_scatter_view = True
                    st.session_state.corr_bar_view = False
                    st.rerun()
            with col4:
                if st.button("Bar Chart", key="corr_bar_btn"):
                    st.session_state.corr_heatmap_view = False
                    st.session_state.corr_scatter_view = False
                    st.session_state.corr_bar_view = True
                    st.rerun()
            
            # Display correlation insights in single container
            if revenue_donations_corr > 0 or revenue_waste_corr < 0:
                st.markdown(f"""
                <div style="background: rgba(0,212,255,0.05); 
                            border: 1px solid #4a4a4a; 
                            border-radius: 8px; 
                            padding: 15px; 
                            margin: 15px 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <p style="color: white; margin: 5px 0;">
                            <strong>Positive Correlation:</strong> Revenue-Donations correlation detected
                        </p>
                        <p style="color: white; margin: 5px 0;">
                            <strong>Correlation Value:</strong> {revenue_donations_corr:.3f}
                        </p>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <p style="color: white; margin: 5px 0;">
                            <strong>Negative Correlation:</strong> Revenue-Waste correlation detected
                        </p>
                        <p style="color: white; margin: 5px 0;">
                            <strong>Correlation Value:</strong> {revenue_waste_corr:.3f}
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if show_policy_ranking:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.header("Policy Efficiency Ranking")
        
        if len(filtered_df) > 0:
            # Calculate efficiency scores
            policy_efficiency = filtered_df.groupby('Donation Policy').agg({
                'Daily Revenue': 'mean',
                'Donated (Today)': 'mean',
                'Wasted (Today)': 'mean'
            })
            
            # Efficiency score = (Revenue + Donations) / (Revenue + Donations + Waste)
            policy_efficiency['Efficiency Score'] = (
                (policy_efficiency['Daily Revenue'] + policy_efficiency['Donated (Today)']) /
                (policy_efficiency['Daily Revenue'] + policy_efficiency['Donated (Today)'] + policy_efficiency['Wasted (Today)'])
            )
            
            policy_efficiency = policy_efficiency.round(3).sort_values('Efficiency Score', ascending=False)
            
            # Display ranking
            st.dataframe(policy_efficiency)
            
            # Show top policy
            top_policy = policy_efficiency.index[0]
            st.markdown(f"""
            <div style="background: rgba(0,212,255,0.05); 
                        border: 1px solid #4a4a4a; 
                        border-radius: 8px; 
                        padding: 15px; 
                        margin: 15px 0;">
                <div style="display: flex; justify-content: space-between;">
                <p style="color: white; margin: 5px 0;">
                    <strong>Top Policy:</strong> {top_policy}
                </p>
                <p style="color: white; margin: 5px 0;">
                    <strong>Efficiency Score:</strong> {policy_efficiency.iloc[0]['Efficiency Score']:.3f}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if show_customer_sensitivity:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.header("Customer Sensitivity Analysis")
        
        if 'theta_set_type' in filtered_df.columns and len(filtered_df) > 0:
            sensitivity_analysis = filtered_df.groupby('theta_set_type').agg({
                'Daily Revenue': 'mean',
                'Donated (Today)': 'mean',
                'Wasted (Today)': 'mean',
                'Sold (Today)': 'mean'
            }).round(2)
            
            st.dataframe(sensitivity_analysis)
            
            # Default to grouped bar chart if no button is pressed
            if 'sensitivity_bar_view' not in st.session_state:
                st.session_state.sensitivity_bar_view = True
                st.session_state.sensitivity_line_view = False
                st.session_state.sensitivity_pie_view = False
            
            # Create different chart types
            if st.session_state.sensitivity_bar_view:
                fig_sensitivity = px.bar(
                    sensitivity_analysis.reset_index(),
                    x='theta_set_type',
                    y=['Daily Revenue', 'Donated (Today)', 'Wasted (Today)'],
                    barmode='group'
                )
                
                # Enhanced tooltips for sensitivity chart
                fig_sensitivity.update_traces(
                    hovertemplate="<b>%{fullData.name}</b><br>" +
                                 "<b>Customer Type:</b> %{x}<br>" +
                                 "<b>Value:</b> %{y:.2f}<br>" +
                                 "<extra></extra>",
                    hoverlabel=dict(
                        bgcolor="rgba(0,0,0,0.9)",
                        bordercolor="#00d4ff",
                        font_size=12,
                        font_family="Arial"
                    )
                )
            
            elif st.session_state.sensitivity_line_view:
                fig_sensitivity = px.line(
                    sensitivity_analysis.reset_index(),
                    x='theta_set_type',
                    y=['Daily Revenue', 'Donated (Today)', 'Wasted (Today)'],
                    markers=True
                )
                
                # Enhanced tooltips for line chart
                fig_sensitivity.update_traces(
                    hovertemplate="<b>%{fullData.name}</b><br>" +
                                 "<b>Customer Type:</b> %{x}<br>" +
                                 "<b>Value:</b> %{y:.2f}<br>" +
                                 "<extra></extra>",
                    hoverlabel=dict(
                        bgcolor="rgba(0,0,0,0.9)",
                        bordercolor="#00d4ff",
                        font_size=12,
                        font_family="Arial"
                    ),
                    line=dict(width=3),
                    mode='lines+markers'
                )
            
            else:  # st.session_state.sensitivity_pie_view
                # Create pie chart for the first metric (Daily Revenue)
                fig_sensitivity = px.pie(
                    sensitivity_analysis.reset_index(),
                    values='Daily Revenue',
                    names='theta_set_type',
                    color_discrete_map={'Regular': '#00d4ff', 'Extreme': '#ff6b6b'}
                )
                
                # Enhanced tooltips for pie chart
                fig_sensitivity.update_traces(
                    hovertemplate="<b>%{label}</b><br>" +
                                 "<b>Daily Revenue:</b> €%{value:.2f}<br>" +
                                 "<b>Percentage:</b> %{percent:.2%}<br>" +
                                 "<extra></extra>",
                    hoverlabel=dict(
                        bgcolor="rgba(0,0,0,0.9)",
                        bordercolor="#00d4ff",
                        font_size=12,
                        font_family="Arial"
                    )
                )
            
            # Common layout for all chart types
            fig_sensitivity.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)', 
                font=dict(color='white'),
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    title="Customer Type"
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    title="Average Value"
                ),
                hovermode='closest'
            )
            
            st.plotly_chart(fig_sensitivity, use_container_width=True, key="sensitivity_chart")
            
            # View toggle buttons below the chart (centered)
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
            with col2:
                if st.button("Grouped Bar", key="sensitivity_bar_btn"):
                    st.session_state.sensitivity_bar_view = True
                    st.session_state.sensitivity_line_view = False
                    st.session_state.sensitivity_pie_view = False
                    st.rerun()
            with col3:
                if st.button("Line Chart", key="sensitivity_line_btn"):
                    st.session_state.sensitivity_bar_view = False
                    st.session_state.sensitivity_line_view = True
                    st.session_state.sensitivity_pie_view = False
                    st.rerun()
            with col4:
                if st.button("Pie Chart", key="sensitivity_pie_btn"):
                    st.session_state.sensitivity_bar_view = False
                    st.session_state.sensitivity_line_view = False
                    st.session_state.sensitivity_pie_view = True
                    st.rerun()
        else:
            st.markdown(f"""
            <div style="background: rgba(0,212,255,0.05); 
                        border: 1px solid #4a4a4a; 
                        border-radius: 8px; 
                        padding: 15px; 
                        margin: 15px 0;">
                <h4 style="color: #00d4ff; margin-bottom: 10px;">Customer Sensitivity Analysis</h4>
                <p style="color: white; margin: 5px 0;">
                    <strong>Status:</strong> Customer sensitivity data not available for selected filters
                </p>
                <p style="color: white; margin: 5px 0;">
                    <strong>Action:</strong> Try adjusting filters or selecting different customer types
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if show_markdown_analysis:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.header("Markdown Policy Analysis")
        
        if 'Markdown Policy' in filtered_df.columns and len(filtered_df) > 0:
            # Filter for markdown policies
            markdown_df = filtered_df[filtered_df['Markdown Policy'].str.contains('Aggressive|Conservative|Moderate|Ultra|Extreme', na=False)]
            
            if len(markdown_df) > 0:
                # Calculate markdown policy effectiveness
                markdown_analysis = markdown_df.groupby('Markdown Policy').agg({
                    'Daily Revenue': 'mean',
                    'Wasted (Today)': 'mean',
                    'Donated (Today)': 'mean'
                }).round(2)
                
                st.dataframe(markdown_analysis)
                
                # Default to grouped bar chart if no button is pressed
                if 'markdown_bar_view' not in st.session_state:
                    st.session_state.markdown_bar_view = True
                    st.session_state.markdown_line_view = False
                    st.session_state.markdown_pie_view = False
                
                # Create different chart types
                if st.session_state.markdown_bar_view:
                    fig_markdown = px.bar(
                        markdown_analysis.reset_index(),
                        x='Markdown Policy',
                        y=['Daily Revenue', 'Wasted (Today)', 'Donated (Today)'],
                        barmode='group'
                    )
                    
                    # Enhanced tooltips for markdown chart
                    fig_markdown.update_traces(
                        hovertemplate="<b>%{fullData.name}</b><br>" +
                                     "<b>Policy:</b> %{x}<br>" +
                                     "<b>Value:</b> %{y:.2f}<br>" +
                                     "<extra></extra>",
                        hoverlabel=dict(
                            bgcolor="rgba(0,0,0,0.9)",
                            bordercolor="#00d4ff",
                            font_size=12,
                            font_family="Arial"
                        )
                    )
                
                elif st.session_state.markdown_line_view:
                    fig_markdown = px.line(
                        markdown_analysis.reset_index(),
                        x='Markdown Policy',
                        y=['Daily Revenue', 'Wasted (Today)', 'Donated (Today)'],
                        markers=True
                    )
                    
                    # Enhanced tooltips for line chart
                    fig_markdown.update_traces(
                        hovertemplate="<b>%{fullData.name}</b><br>" +
                                     "<b>Policy:</b> %{x}<br>" +
                                     "<b>Value:</b> %{y:.2f}<br>" +
                                     "<extra></extra>",
                        hoverlabel=dict(
                            bgcolor="rgba(0,0,0,0.9)",
                            bordercolor="#00d4ff",
                            font_size=12,
                            font_family="Arial"
                        ),
                        line=dict(width=3),
                        mode='lines+markers'
                    )
                
                else:  # st.session_state.markdown_pie_view
                    # Create pie chart for the first metric (Daily Revenue)
                    fig_markdown = px.pie(
                        markdown_analysis.reset_index(),
                        values='Daily Revenue',
                        names='Markdown Policy',
                        color_discrete_sequence=['#00d4ff', '#51cf66', '#ff6b6b', '#ffd43b', '#ae8fff']
                    )
                    
                    # Enhanced tooltips for pie chart
                    fig_markdown.update_traces(
                        hovertemplate="<b>%{label}</b><br>" +
                                     "<b>Daily Revenue:</b> €%{value:.2f}<br>" +
                                     "<b>Percentage:</b> %{percent:.2%}<br>" +
                                     "<extra></extra>",
                        hoverlabel=dict(
                            bgcolor="rgba(0,0,0,0.9)",
                            bordercolor="#00d4ff",
                            font_size=12,
                            font_family="Arial"
                        )
                    )
                
                # Common layout for all chart types
                fig_markdown.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    font=dict(color='white'),
                    xaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)',
                        title="Markdown Policy"
                    ),
                    yaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)',
                        title="Average Value"
                    ),
                    hovermode='closest'
                )
                
                st.plotly_chart(fig_markdown, use_container_width=True, key="markdown_chart")
                
                # View toggle buttons below the chart (centered)
                col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
                with col2:
                    if st.button("Grouped Bar", key="markdown_bar_btn"):
                        st.session_state.markdown_bar_view = True
                        st.session_state.markdown_line_view = False
                        st.session_state.markdown_pie_view = False
                        st.rerun()
                with col3:
                    if st.button("Line Chart", key="markdown_line_btn"):
                        st.session_state.markdown_bar_view = False
                        st.session_state.markdown_line_view = True
                        st.session_state.markdown_pie_view = False
                        st.rerun()
                with col4:
                    if st.button("Pie Chart", key="markdown_pie_btn"):
                        st.session_state.markdown_bar_view = False
                        st.session_state.markdown_line_view = False
                        st.session_state.markdown_pie_view = True
                        st.rerun()
            else:
                st.markdown(f"""
                <div style="background: rgba(0,212,255,0.05); 
                            border: 1px solid #4a4a4a; 
                            border-radius: 8px; 
                            padding: 15px; 
                            margin: 15px 0;">
                    <h4 style="color: #00d4ff; margin-bottom: 10px;">Markdown Policy Analysis</h4>
                    <p style="color: white; margin: 5px 0;">
                        <strong>Status:</strong> No markdown policy data available for selected filters
                    </p>
                    <p style="color: white; margin: 5px 0;">
                        <strong>Action:</strong> Try adjusting filters or selecting different policies
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: rgba(0,212,255,0.05); 
                        border: 1px solid #4a4a4a; 
                        border-radius: 8px; 
                        padding: 15px; 
                        margin: 15px 0;">
                <h4 style="color: #00d4ff; margin-bottom: 10px;">Markdown Policy Analysis</h4>
                <p style="color: white; margin: 5px 0;">
                    <strong>Status:</strong> Markdown policy data not available
                </p>
                <p style="color: white; margin: 5px 0;">
                    <strong>Action:</strong> Check if markdown policy column exists in dataset
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ✅ Analysis Summary
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.header("Analysis Summary")
    
    if selected_policy == "All Policies":
        policy_text = "all policies"
    else:
        policy_text = f"the {selected_policy} policy"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Data Scope",
            value=f"{len(filtered_df):,} days",
            delta=f"{selected_product} | {policy_text}"
        )
        
        st.metric(
            label="Customer Type",
            value=selected_theta,
            delta=f"Markdown: {selected_markdown if 'selected_markdown' in locals() else 'All'}"
        )
    
    with col2:
        st.metric(
            label="Best Performance",
            value="Donations" if donated_pct > wasted_pct else "Sales" if sold_pct > 80 else "Needs Improvement",
            delta=f"Scenario: {selected_scenario if 'selected_scenario' in locals() else 'All'}"
        )
        
        st.metric(
            label="Data Coverage",
            value=f"{sold_pct:.1f}% sold",
            delta=f"{donated_pct:.1f}% donated | {wasted_pct:.1f}% wasted"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
else:
    st.markdown(f"""
    <div style="background: rgba(0,212,255,0.05); 
                border: 1px solid #4a4a4a; 
                border-radius: 8px; 
                padding: 15px; 
                margin: 15px 0;">
        <h4 style="color: #00d4ff; margin-bottom: 10px;">Data Availability</h4>
        <p style="color: white; margin: 5px 0;">
            <strong>Status:</strong> No data available for the selected filters
        </p>
        <p style="color: white; margin: 5px 0;">
            <strong>Action:</strong> Try different filter options or check data source
        </p>
    </div>
    """, unsafe_allow_html=True)

# ✅ Enhanced Footer
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('''
<div style="background: linear-gradient(135deg, #262730 0%, #1e1e2e 100%); 
            border: 1px solid #4a4a4a; 
            border-radius: 15px; 
            padding: 15px; 
            margin: 30px 0 20px 0; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.3); 
            text-align: center;">
    <div style="margin-bottom: 3px;">
        <p style="color: #888; margin: 3px 0 0 0; font-size: 14px;">Advanced Analytics & Performance Monitoring System</p>
    </div>
    <div style="border-top: 1px solid #4a4a4a; padding-top: 8px; margin-top: 3px;">
        <p style="color: #666; margin: 0; font-size: 12px;">© 2024 Supermarket Analytics Platform | Built with Streamlit & Python</p>
    </div>
</div>
''', unsafe_allow_html=True)

