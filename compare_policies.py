import pandas as pd
import matplotlib.pyplot as plt

# Load the single CSV file that contains all policies
df = pd.read_csv("multi_product_results_all_policies.csv")

print("=== POLICY COMPARISON RESULTS ===\n")

# Filter data for each policy
early_data = df[df['Donation Policy'] == 'Early']
end_data = df[df['Donation Policy'] == 'End']
overstock_data = df[df['Donation Policy'] == 'Overstock']
restricted_data = df[df['Donation Policy'] == 'Restricted']

# Filter by theta set type
regular_data = df[df['theta_set_type'] == 'Regular']
extreme_data = df[df['theta_set_type'] == 'Extreme']

# Calculate totals for each policy
policies = {
    'Early': early_data,
    'End of Shelf Life': end_data, 
    'Overstock': overstock_data,
    'Restricted': restricted_data
}

# REGULAR THETA SETS RESULTS
print("RESULTS FOR REGULAR THETA SETS:")
print("-" * 80)
print(f"{'Policy':<20} {'Sold':<12} {'Donated':<12} {'Wasted':<12} {'Discounted':<12} {'Revenue':<12}")
print("-" * 80)

for policy_name, policy_data in policies.items():
    if not policy_data.empty:
        # Filter for regular theta sets only
        regular_policy_data = policy_data[policy_data['theta_set_type'] == 'Regular']
        if not regular_policy_data.empty:
            total_sold = regular_policy_data['Sold (Today)'].sum()
            total_donated = regular_policy_data['Donated (Today)'].sum()
            total_wasted = regular_policy_data['Wasted (Today)'].sum()
            total_discounted = regular_policy_data['Discounted Sales (Today)'].sum()
            total_revenue = regular_policy_data['Daily Revenue'].sum()
            
            print(f"{policy_name:<20} {total_sold:<12} {total_donated:<12} {total_wasted:<12} {total_discounted:<12} {total_revenue:<12.2f}")

print("\n" + "=" * 80)

# EXTREME THETA SETS RESULTS
print("RESULTS FOR EXTREME THETA SETS:")
print("-" * 80)
print(f"{'Policy':<20} {'Sold':<12} {'Donated':<12} {'Wasted':<12} {'Discounted':<12} {'Revenue':<12}")
print("-" * 80)

for policy_name, policy_data in policies.items():
    if not policy_data.empty:
        # Filter for extreme theta sets only
        extreme_policy_data = policy_data[policy_data['theta_set_type'] == 'Extreme']
        if not extreme_policy_data.empty:
            total_sold = extreme_policy_data['Sold (Today)'].sum()
            total_donated = extreme_policy_data['Donated (Today)'].sum()
            total_wasted = extreme_policy_data['Wasted (Today)'].sum()
            total_discounted = extreme_policy_data['Discounted Sales (Today)'].sum()
            total_revenue = extreme_policy_data['Daily Revenue'].sum()
            
            print(f"{policy_name:<20} {total_sold:<12} {total_donated:<12} {total_wasted:<12} {total_discounted:<12} {total_revenue:<12.2f}")

print("\n" + "=" * 80)

# AGGREGATED RESULTS
print("AGGREGATED RESULTS:")
print("-" * 80)
print(f"{'Policy':<20} {'Sold':<12} {'Donated':<12} {'Wasted':<12} {'Discounted':<12} {'Revenue':<12}")
print("-" * 80)

for policy_name, policy_data in policies.items():
    if not policy_data.empty:
        total_sold = policy_data['Sold (Today)'].sum()
        total_donated = policy_data['Donated (Today)'].sum()
        total_wasted = policy_data['Wasted (Today)'].sum()
        total_discounted = policy_data['Discounted Sales (Today)'].sum()
        total_revenue = policy_data['Daily Revenue'].sum()
        
        print(f"{policy_name:<20} {total_sold:<12} {total_donated:<12} {total_wasted:<12} {total_discounted:<12} {total_revenue:<12.2f}")

print("\n" + "=" * 80)

# Calculate percentages
print("\nPERCENTAGES BY POLICY:")
print("-" * 80)
print(f"{'Policy':<20} {'Sold %':<10} {'Donated %':<12} {'Wasted %':<12}")
print("-" * 80)

for policy_name, policy_data in policies.items():
    if not policy_data.empty:
        total_units = (policy_data['Sold (Today)'].sum() + 
                      policy_data['Donated (Today)'].sum() + 
                      policy_data['Wasted (Today)'].sum())
        
        sold_pct = (policy_data['Sold (Today)'].sum() / total_units) * 100
        donated_pct = (policy_data['Donated (Today)'].sum() / total_units) * 100
        wasted_pct = (policy_data['Wasted (Today)'].sum() / total_units) * 100
        
        print(f"{policy_name:<20} {sold_pct:<10.1f} {donated_pct:<12.1f} {wasted_pct:<12.1f}")

print("\n" + "=" * 80)

# Daily averages
print("\nDAILY AVERAGES BY POLICY:")
print("-" * 80)
print(f"{'Policy':<20} {'Avg Sold/Day':<15} {'Avg Donated/Day':<18} {'Avg Wasted/Day':<16}")
print("-" * 80)

for policy_name, policy_data in policies.items():
    if not policy_data.empty:
        days = len(policy_data)
        avg_sold = policy_data['Sold (Today)'].sum() / days
        avg_donated = policy_data['Donated (Today)'].sum() / days
        avg_wasted = policy_data['Wasted (Today)'].sum() / days
        
        print(f"{policy_name:<20} {avg_sold:<15.1f} {avg_donated:<18.1f} {avg_wasted:<16.1f}")

print("\n" + "=" * 80)



print("\n" + "=" * 80)

# ✅ MARKDOWN CORRELATION ANALYSIS
print("\nMARKDOWN CORRELATION ANALYSIS:")
print("-" * 80)
if "Markdown Policy" in df.columns:
    markdown_data = df[df["Markdown Policy"] != "Default"]
    if not markdown_data.empty:
        print("Markdown policy impact on key metrics:")
        markdown_summary = markdown_data.groupby("Markdown Policy").agg({
            "Daily Revenue": "mean",
            "Wasted (Today)": "mean",
            "Donated (Today)": "mean",
            "Sold (Today)": "mean"
        }).round(2)
        print(markdown_summary)
        
        print("\nKey correlations by markdown policy:")
        for policy in markdown_data["Markdown Policy"].unique():
            policy_data = markdown_data[markdown_data["Markdown Policy"] == policy]
            revenue_waste_corr = policy_data["Daily Revenue"].corr(policy_data["Wasted (Today)"])
            revenue_donated_corr = policy_data["Daily Revenue"].corr(policy_data["Donated (Today)"])
            print(f"  {policy}:")
            print(f"    Revenue vs Waste: {revenue_waste_corr:.3f}")
            print(f"    Revenue vs Donated: {revenue_donated_corr:.3f}")
    else:
        print("No markdown correlation data available")
else:
    print("Markdown Policy column not found in results")

# ✅ MULTIPLE RESTRICTIVE DONATION SETTINGS ANALYSIS
print("\nMULTIPLE RESTRICTIVE DONATION SETTINGS IMPACT:")
print("-" * 80)
restricted_all = df[df["Donation Policy"].str.contains("Restricted", na=False)]
if not restricted_all.empty:
    print("Restrictive donation settings tested:")
    unique_restricted = restricted_all["Donation Policy"].unique()
    for setting in unique_restricted:
        setting_data = restricted_all[restricted_all["Donation Policy"] == setting]
        avg_waste = setting_data["Wasted (Today)"].mean()
        avg_donated = setting_data["Donated (Today)"].mean()
        print(f"  {setting}:")
        print(f"    Avg Waste: {avg_waste:.2f}")
        print(f"    Avg Donated: {avg_donated:.2f}")
else:
    print("No multiple restrictive donation settings data available")

# ✅ GENERALIZATION AND POLICY EFFECTIVENESS
print("\nGENERALIZATION: POLICY EFFECTIVENESS RANKINGS:")
print("-" * 80)
# Calculate efficiency scores for all policies
policy_efficiency = {}
for policy_name, policy_data in policies.items():
    if not policy_data.empty:
        # Calculate normalized metrics
        avg_waste = policy_data["Wasted (Today)"].mean()
        avg_donated = policy_data["Donated (Today)"].mean()
        avg_revenue = policy_data["Daily Revenue"].mean()
        
        # Simple efficiency score (lower waste, higher donations, higher revenue)
        efficiency_score = (avg_donated - avg_waste + avg_revenue/100) / 3
        policy_efficiency[policy_name] = efficiency_score

# Sort by efficiency score
sorted_policies = sorted(policy_efficiency.items(), key=lambda x: x[1], reverse=True)
print("Policy effectiveness rankings (based on waste reduction, donations, and revenue):")
for i, (policy, score) in enumerate(sorted_policies, 1):
    print(f"  {i}. {policy}: {score:.3f}") 