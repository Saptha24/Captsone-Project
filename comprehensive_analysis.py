import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

print("="*80)
print("COMPREHENSIVE ANALYSIS RESULTS")
print("="*80)

# Load the results
try:
    df = pd.read_csv("multi_product_results_all_policies.csv")
    print(f"Loaded {len(df)} simulation runs")
except FileNotFoundError:
    print("Results file not found. Please run test5.py first.")
    exit()

print("\n" + "="*80)
print("1. DONATION ACCEPTANCE PROBABILITIES")
print("="*80)
print("Updated acceptance rates:")
print("   - Fresh products (0-2 days): 95%")
print("   - Near-fresh (3-4 days): 85%")
print("   - Near-expiry (5-6 days): 75%")
print("   - Expired (within shelf life): 65%")
print("   - Very old (beyond shelf life): 45%")

# Analyze donation effectiveness by policy
donation_analysis = df.groupby('Donation Policy').agg({
    'Donated (Today)': 'mean',
    'Wasted (Today)': 'mean',
    'Daily Revenue': 'mean'
}).round(2)

print("\nDONATION POLICY EFFECTIVENESS:")
print(donation_analysis)

print("\n" + "="*80)
print("2. MARKDOWN POLICY CORRELATION ANALYSIS")
print("="*80)

# Filter for markdown policy analysis
markdown_df = df[df['Markdown Policy'].str.contains('Aggressive|Conservative|Moderate|Ultra|Extreme', na=False)]

if len(markdown_df) > 0:
    # Calculate correlations for each markdown policy
    correlation_results = []
    
    for policy in markdown_df['Markdown Policy'].unique():
        policy_data = markdown_df[markdown_df['Markdown Policy'] == policy]
        
        # Revenue vs Waste correlation
        revenue_waste_corr = policy_data['Daily Revenue'].corr(policy_data['Wasted (Today)'])
        
        # Revenue vs Donations correlation  
        revenue_donations_corr = policy_data['Daily Revenue'].corr(policy_data['Donated (Today)'])
        
        # Waste vs Donations correlation
        waste_donations_corr = policy_data['Wasted (Today)'].corr(policy_data['Donated (Today)'])
        
        correlation_results.append({
            'Markdown Policy': policy,
            'Revenue vs Waste': revenue_waste_corr,
            'Revenue vs Donations': revenue_donations_corr,
            'Waste vs Donations': waste_donations_corr,
            'Mean Revenue': policy_data['Daily Revenue'].mean(),
            'Mean Waste': policy_data['Wasted (Today)'].mean(),
            'Mean Donations': policy_data['Donated (Today)'].mean()
        })
    
    correlation_df = pd.DataFrame(correlation_results)
    correlation_df = correlation_df.round(3)
    
    print("CORRELATION ANALYSIS RESULTS:")
    print(correlation_df.to_string(index=False))
    
    # Find the most effective markdown policy
    best_policy = correlation_df.loc[correlation_df['Revenue vs Donations'].idxmax()]
    print(f"\nMOST EFFECTIVE POLICY: {best_policy['Markdown Policy']}")
    print(f"Revenue-Donations Correlation: {best_policy['Revenue vs Donations']:.3f}")
    print(f"Revenue-Waste Correlation: {best_policy['Revenue vs Waste']:.3f}")

print("\n" + "="*80)
print("3. RESTRICTIVE DONATION SETTINGS")
print("="*80)

# Analyze restrictive donation settings
restrictive_df = df[df['Donation Policy'] == 'Restricted']
if len(restrictive_df) > 0:
    print(f"Restricted donation runs: {len(restrictive_df)}")
    
    # Simple analysis without grouping by donation days
    restrictive_summary = restrictive_df.agg({
        'Donated (Today)': 'mean',
        'Wasted (Today)': 'mean',
        'Daily Revenue': 'mean'
    }).round(2)
    
    print("\nRESTRICTIVE POLICY SUMMARY:")
    print(restrictive_summary)
else:
    print("No restricted donation data available")

print("\n" + "="*80)
print("4. CUSTOMER SENSITIVITY ANALYSIS")
print("="*80)

# Compare Regular vs Extreme theta sets
if 'theta_set_type' in df.columns:
    sensitivity_analysis = df.groupby('theta_set_type').agg({
        'Daily Revenue': 'mean',
        'Donated (Today)': 'mean',
        'Wasted (Today)': 'mean',
        'Sold (Today)': 'mean'
    }).round(2)
    
    print("CUSTOMER SENSITIVITY COMPARISON:")
    print(sensitivity_analysis)

print("\n" + "="*80)
print("5. POLICY EFFICIENCY RANKING")
print("="*80)

# Calculate efficiency scores
if len(df) > 0:
    policy_efficiency = df.groupby('Donation Policy').agg({
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
    
    print("POLICY EFFICIENCY RANKING:")
    print(policy_efficiency)
    
    print(f"\nTOP POLICY: {policy_efficiency.index[0]}")
    print(f"Efficiency Score: {policy_efficiency.iloc[0]['Efficiency Score']:.3f}")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80) 