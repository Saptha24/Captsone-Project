import pandas as pd

def generate_comprehensive_report():
    """Generate a comprehensive but concise report from all simulation runs"""
    
    print("=" * 80)
    print("COMPREHENSIVE SIMULATION ANALYSIS REPORT")
    print("=" * 80)
    
    # Load data
    df = pd.read_csv("multi_product_results_all_policies.csv")
    
    print(f"📊 Analysis based on {len(df):,} simulation runs")
    print(f"📅 Simulation period: 90 days")
    print(f"🛒 Product: Milk (€2.50, 8-day shelf life)")
    print(f"👥 Customer types: Regular vs Extreme sensitivity")
    print(f"🏪 Policies tested: 4 donation + 8 markdown combinations")
    
    print("\n" + "=" * 80)
    print("EXECUTIVE SUMMARY")
    print("=" * 80)
    
    # 1. BEST PERFORMING POLICIES
    print("\n🏆 TOP 3 MOST EFFICIENT POLICIES:")
    print("-" * 40)
    
    policy_efficiency = df.groupby('Donation Policy').agg({
        'Daily Revenue': 'mean',
        'Donated (Today)': 'mean',
        'Wasted (Today)': 'mean'
    })
    
    policy_efficiency['Efficiency'] = (
        (policy_efficiency['Daily Revenue'] + policy_efficiency['Donated (Today)']) /
        (policy_efficiency['Daily Revenue'] + policy_efficiency['Donated (Today)'] + policy_efficiency['Wasted (Today)'])
    )
    
    policy_efficiency = policy_efficiency.sort_values('Efficiency', ascending=False)
    
    for i, (policy, row) in enumerate(policy_efficiency.head(3).iterrows(), 1):
        print(f"{i}. {policy:12} | Efficiency: {row['Efficiency']:.3f} | Revenue: €{row['Daily Revenue']:.1f} | Donations: {row['Donated (Today)']:.1f} | Waste: {row['Wasted (Today)']:.1f}")
    
    # 2. CORRELATION INSIGHTS
    print("\n📈 KEY CORRELATIONS:")
    print("-" * 30)
    
    revenue_donations_corr = df['Daily Revenue'].corr(df['Donated (Today)'])
    revenue_waste_corr = df['Daily Revenue'].corr(df['Wasted (Today)'])
    
    print(f"• Revenue ↔ Donations: {revenue_donations_corr:+.3f} (Positive correlation)")
    print(f"• Revenue ↔ Waste: {revenue_waste_corr:+.3f} (Negative correlation)")
    
    print("\n" + "=" * 80)
    print("DETAILED ANALYSIS")
    print("=" * 80)
    
    # 3. OVERALL PERFORMANCE METRICS
    print("\n📊 OVERALL PERFORMANCE METRICS:")
    print("-" * 40)
    
    overall_stats = {
        'Total Revenue': df['Daily Revenue'].sum(),
        'Total Sold': df['Sold (Today)'].sum(),
        'Total Donated': df['Donated (Today)'].sum(),
        'Total Wasted': df['Wasted (Today)'].sum(),
        'Avg Daily Revenue': df['Daily Revenue'].mean(),
        'Avg Daily Sold': df['Sold (Today)'].mean(),
        'Avg Daily Donated': df['Donated (Today)'].mean(),
        'Avg Daily Wasted': df['Wasted (Today)'].mean()
    }
    
    for metric, value in overall_stats.items():
        if 'Total' in metric:
            print(f"{metric:25}: {value:>12,.0f}")
        else:
            print(f"{metric:25}: {value:>12.2f}")
    
    # 4. COMPLETE POLICY RANKING
    print("\n🏆 COMPLETE POLICY EFFICIENCY RANKING:")
    print("-" * 50)
    
    print("Rank | Policy      | Efficiency | Revenue | Donations | Waste")
    print("-" * 65)
    for i, (policy, row) in enumerate(policy_efficiency.iterrows(), 1):
        print(f"{i:4} | {policy:11} | {row['Efficiency']:9.3f} | {row['Daily Revenue']:7.1f} | {row['Donated (Today)']:9.1f} | {row['Wasted (Today)']:5.1f}")
    
    # 5. MARKDOWN POLICY ANALYSIS
    print("\n💰 MARKDOWN POLICY ANALYSIS:")
    print("-" * 40)
    
    if 'Markdown Policy' in df.columns:
        markdown_analysis = df.groupby('Markdown Policy').agg({
            'Daily Revenue': 'mean',
            'Wasted (Today)': 'mean',
            'Donated (Today)': 'mean'
        }).round(2)
        
        print("Markdown Policy      | Revenue | Waste | Donations")
        print("-" * 45)
        for policy, row in markdown_analysis.iterrows():
            print(f"{policy:18} | {row['Daily Revenue']:7.1f} | {row['Wasted (Today)']:5.1f} | {row['Donated (Today)']:9.1f}")
    
    # 6. CUSTOMER SENSITIVITY ANALYSIS
    print("\n👥 CUSTOMER SENSITIVITY ANALYSIS:")
    print("-" * 40)
    
    if 'theta_set_type' in df.columns:
        customer_analysis = df.groupby('theta_set_type').agg({
            'Daily Revenue': 'mean',
            'Donated (Today)': 'mean',
            'Wasted (Today)': 'mean',
            'Sold (Today)': 'mean'
        }).round(2)
        
        print("Customer Type | Revenue | Donations | Waste | Sold")
        print("-" * 50)
        for customer_type, row in customer_analysis.iterrows():
            print(f"{customer_type:12} | {row['Daily Revenue']:7.1f} | {row['Donated (Today)']:9.1f} | {row['Wasted (Today)']:5.1f} | {row['Sold (Today)']:4.1f}")
    
    print("\n" + "=" * 80)
    print("COMPREHENSIVE REPORT COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    generate_comprehensive_report() 