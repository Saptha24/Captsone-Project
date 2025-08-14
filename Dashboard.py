import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

#  Fix for large DataFrame rendering
pd.set_option("styler.render.max_elements", 1000000)

st.set_page_config(page_title="Supermarket Dashboard", layout="wide")


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

st.markdown('<h1 class="header-glow">🛒 Supermarket Inventory Dashboard</h1>', unsafe_allow_html=True)

# ✅ Load Data
@st.cache_data
def load_data():
    return pd.read_csv("multi_product_results_all_policies.csv")

df = load_data()

# ✅ Simple Sidebar
with st.sidebar:
    st.header("📊 Filters")
    
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
    st.header("📅 Day Navigation")
    
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
    st.header("🧍 Customer Simulation")
    
    customers_per_day = st.slider("Customers per Day", 1, 100, 10)
    
    # Show current day info
    st.info(f"📅 **Current Day:** {st.session_state.current_day}")
    st.info(f"🧍 **Customers:** {customers_per_day} per day")
    
    # ✅ Add Simulation Controls
    st.header("🎮 Simulation Controls")
    
    show_cumulative = st.checkbox("📦 Show Cumulative Stats", value=False)
    show_animation = st.checkbox("🎬 Show Customer Animation", value=True)
    
    # Simulation speed
    animation_speed = st.slider("Animation Speed", 0.01, 0.1, 0.03, 0.01)
    
    # Advanced Analysis Features
    st.header("📊 Advanced Analysis")
    
    show_correlation_analysis = st.checkbox("🔗 Show Correlation Analysis", value=False)
    show_policy_ranking = st.checkbox("🏆 Show Policy Efficiency Ranking", value=False)
    show_customer_sensitivity = st.checkbox("👥 Show Customer Sensitivity Analysis", value=False)
    show_markdown_analysis = st.checkbox("📈 Show Markdown Policy Analysis", value=False)

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
    # ✅ Customer Simulation Animation
    if show_animation:
        st.header("🧍 Customer Simulation")
        
        # Get data for current day
        current_day_data = filtered_df[filtered_df["Day"] == st.session_state.current_day]
        
        if not current_day_data.empty:
            sold_today = int(current_day_data["Sold (Today)"].iloc[0])
            
            # Create customer animation
            placeholder = st.empty()
            icons = ["🧍‍♂️🥛" if i < sold_today else "🧍‍♂️🚫" for i in range(customers_per_day)]
            
            for step in range(1, customers_per_day + 1):
                with placeholder.container():
                    st.markdown(" ".join(icons[:step]), unsafe_allow_html=True)
                time.sleep(animation_speed)
            
            # Show day summary
            st.success(f"🎉 **Day {st.session_state.current_day} Summary:** {sold_today} customers bought products!")
        else:
            st.info(f"📅 No data available for Day {st.session_state.current_day}")
    
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
    st.header(f"📈 Key Performance Metrics{metric_suffix}")
    
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
    st.header("📊 Daily Performance Metrics")
    
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
    
    # NEW: Current Day Metrics
    if st.session_state.current_day <= len(filtered_df):
        current_day_data = filtered_df[filtered_df["Day"] == st.session_state.current_day]
        if not current_day_data.empty:
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.header(f"📅 Day {st.session_state.current_day} Performance")
            
            day_sold = current_day_data["Sold (Today)"].iloc[0]
            day_donated = current_day_data["Donated (Today)"].iloc[0]
            day_wasted = current_day_data["Wasted (Today)"].iloc[0]
            day_revenue = current_day_data["Daily Revenue"].iloc[0]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label=f"Day {st.session_state.current_day} Sold",
                    value=f"{day_sold:.0f}",
                    delta=f"units"
                )
            
            with col2:
                st.metric(
                    label=f"Day {st.session_state.current_day} Donated", 
                    value=f"{day_donated:.0f}",
                    delta=f"units"
                )
            
            with col3:
                st.metric(
                    label=f"Day {st.session_state.current_day} Wasted",
                    value=f"{day_wasted:.0f}",
                    delta=f"units"
                )
            
            with col4:
                st.metric(
                    label=f"Day {st.session_state.current_day} Revenue",
                    value=f"€{day_revenue:.1f}",
                    delta=f"revenue"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ✅ Simple Pie Chart
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.header("📊 Product Distribution")
    
    fig_pie = px.pie(
        values=[total_sold, total_donated, total_wasted],
        names=['Sold', 'Donated', 'Wasted'],
        title="What happened to all products?",
        color_discrete_map={'Sold': '#00d4ff', 'Donated': '#51cf66', 'Wasted': '#ff6b6b'}
    )
    
    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ✅ Simple Line Chart
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.header("📈 Daily Trends")
    
    # Sample data for trend (last 30 days if available)
    trend_df = filtered_df.tail(30) if len(filtered_df) > 30 else filtered_df
    
    fig_trend = px.line(
        trend_df,
        x="Day",
        y=["Sold (Today)", "Donated (Today)", "Wasted (Today)"],
        title="Last 30 Days Performance",
        template="plotly_dark"
    )
    
    fig_trend.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ✅ Data Table
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.header("📋 Data Table")
    
    # Show a manageable sample of the data
    if len(filtered_df) > 50:
        st.info(f"📊 Showing first 50 rows of {len(filtered_df)} total rows")
        display_table = filtered_df.head(50)
    else:
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
    
    # ✅ Policy Comparison (if multiple policies)
    if selected_policy == "All Policies" and "Donation Policy" in df.columns:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.header("🏆 Policy Comparison")
        
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
        
        # Create simple bar chart
        fig_policy = px.bar(
            policy_summary,
            x="Donation Policy",
            y=["Sold %", "Donated %", "Wasted %"],
            title="Policy Performance Comparison",
            barmode='stack',
            color_discrete_map={'Sold %': '#00d4ff', 'Donated %': '#51cf66', 'Wasted %': '#ff6b6b'}
        )
        
        fig_policy.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        
        st.plotly_chart(fig_policy, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Advanced Analysis Sections
    if show_correlation_analysis:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.header("🔗 Correlation Analysis")
        
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
            
            # Create correlation heatmap
            corr_matrix = filtered_df[['Daily Revenue', 'Wasted (Today)', 'Donated (Today)']].corr()
            fig_corr = px.imshow(
                corr_matrix,
                title="Correlation Heatmap",
                color_continuous_scale='RdBu',
                aspect='auto'
            )
            fig_corr.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
            st.plotly_chart(fig_corr, use_container_width=True, key="correlation_heatmap")
            
            # Display correlation insights
            if revenue_donations_corr > 0:
                st.success("✅ Positive Revenue-Donations correlation detected")
            if revenue_waste_corr < 0:
                st.success("✅ Negative Revenue-Waste correlation detected")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if show_policy_ranking:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.header("🏆 Policy Efficiency Ranking")
        
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
            st.success(f"🏆 **Top Policy:** {top_policy} (Efficiency: {policy_efficiency.iloc[0]['Efficiency Score']:.3f})")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if show_customer_sensitivity:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.header("👥 Customer Sensitivity Analysis")
        
        if 'theta_set_type' in filtered_df.columns and len(filtered_df) > 0:
            sensitivity_analysis = filtered_df.groupby('theta_set_type').agg({
                'Daily Revenue': 'mean',
                'Donated (Today)': 'mean',
                'Wasted (Today)': 'mean',
                'Sold (Today)': 'mean'
            }).round(2)
            
            st.dataframe(sensitivity_analysis)
            
            # Create comparison chart
            fig_sensitivity = px.bar(
                sensitivity_analysis.reset_index(),
                x='theta_set_type',
                y=['Daily Revenue', 'Donated (Today)', 'Wasted (Today)'],
                title="Customer Sensitivity Impact",
                barmode='group'
            )
            fig_sensitivity.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
            st.plotly_chart(fig_sensitivity, use_container_width=True, key="sensitivity_chart")
        else:
            st.warning("Customer sensitivity data not available for selected filters.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if show_markdown_analysis:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.header("📈 Markdown Policy Analysis")
        
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
                
                # Create markdown effectiveness chart
                fig_markdown = px.bar(
                    markdown_analysis.reset_index(),
                    x='Markdown Policy',
                    y=['Daily Revenue', 'Wasted (Today)', 'Donated (Today)'],
                    title="Markdown Policy Effectiveness",
                    barmode='group'
                )
                fig_markdown.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
                st.plotly_chart(fig_markdown, use_container_width=True, key="markdown_chart")
            else:
                st.info("No markdown policy data available for selected filters.")
        else:
            st.warning("Markdown policy data not available.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ✅ Analysis Summary
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.header("📋 Analysis Summary")
    
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
    
    # NEW: Concise Summary Statistics
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.header("📈 Concise Summary Statistics")
    
    # Calculate key metrics for all data
    all_data_summary = df.groupby(['Donation Policy', 'Markdown Policy']).agg({
        'Daily Revenue': ['mean', 'std'],
        'Wasted (Today)': ['mean', 'std'],
        'Donated (Today)': ['mean', 'std'],
        'Sold (Today)': ['mean', 'std']
    }).round(2)
    
    # Flatten column names
    all_data_summary.columns = ['_'.join(col).strip() for col in all_data_summary.columns.values]
    
    # Show top 5 most efficient combinations
    st.subheader("🏆 Top 5 Most Efficient Policy Combinations")
    
    # Calculate efficiency score for each combination
    efficiency_data = []
    for (donation_policy, markdown_policy), group in df.groupby(['Donation Policy', 'Markdown Policy']):
        avg_revenue = group['Daily Revenue'].mean()
        avg_donations = group['Donated (Today)'].mean()
        avg_waste = group['Wasted (Today)'].mean()
        
        efficiency_score = (avg_revenue + avg_donations) / (avg_revenue + avg_donations + avg_waste)
        
        efficiency_data.append({
            'Donation Policy': donation_policy,
            'Markdown Policy': markdown_policy,
            'Efficiency Score': efficiency_score,
            'Avg Revenue': avg_revenue,
            'Avg Donations': avg_donations,
            'Avg Waste': avg_waste
        })
    
    efficiency_df = pd.DataFrame(efficiency_data).sort_values('Efficiency Score', ascending=False)
    st.dataframe(efficiency_df.head(), use_container_width=True)
    
    # Key Metrics Summary
    st.subheader("📊 Key Metrics Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Best performing policy
        best_policy = efficiency_df.iloc[0]
        st.metric(
            label="Best Policy",
            value=f"{best_policy['Donation Policy']} + {best_policy['Markdown Policy']}",
            delta=f"Efficiency: {best_policy['Efficiency Score']:.3f}"
        )
        
        # Revenue vs Donations correlation
        overall_corr = df['Daily Revenue'].corr(df['Donated (Today)'])
        st.metric(
            label="Revenue-Donations Correlation",
            value=f"{overall_corr:.3f}",
            delta="Overall correlation"
        )
    
    with col2:
        # Waste reduction
        avg_waste = df['Wasted (Today)'].mean()
        st.metric(
            label="Average Daily Waste",
            value=f"{avg_waste:.2f}",
            delta="units"
        )
        
        # Donation effectiveness
        avg_donations = df['Donated (Today)'].mean()
        st.metric(
            label="Average Daily Donations",
            value=f"{avg_donations:.2f}",
            delta="units"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
else:
    st.warning("⚠️ No data available for the selected filters. Try different options.")

# ✅ Footer
st.markdown('<div class="footer-glow">', unsafe_allow_html=True)
st.caption("🛒 Supermarket Inventory Management Dashboard")
st.markdown('</div>', unsafe_allow_html=True)
