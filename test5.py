from inventory_manager_1 import Inventory
import random
import pandas as pd

# ✅ Products
products = [
    {"Product Name": "Milk_A", "Price per Unit": 2.5, "Shelf Life": 8}
]

# Scenarios - REALISTIC replenishment quantities for supermarket operations
# Explanation: 4-day cycle uses 400 units (100 units/day avg), 8-day cycle uses 600 units (75 units/day avg)
# This reflects realistic inventory management where more frequent replenishment allows smaller quantities
scenario_list = [
    {"scenario_id": 1, "replenish_days": 4, "reorder_quantity": 400, "threshold_level": 0.1, "td": 1, "pd": 0.3},
    {"scenario_id": 2, "replenish_days": 4, "reorder_quantity": 400, "threshold_level": 0.3, "td": 2, "pd": 0.3},
    {"scenario_id": 3, "replenish_days": 8, "reorder_quantity": 600, "threshold_level": 0.1, "td": 1, "pd": 0.3},
    {"scenario_id": 4, "replenish_days": 8, "reorder_quantity": 600, "threshold_level": 0.3, "td": 2, "pd": 0.3}
]

# ✅ REALISTIC demand parameters for supermarket operations
# Current parameters assume price and quality sensitive customers
theta_sets = [(0.6, 0.3, 0.1), (0.5, 0.3, 0.2), (0.4, 0.3, 0.3)]

# ✅ EXTREME SCENARIOS for sensitivity analysis
# Low sensitivity customers (high theta0 + theta2, low price/quality sensitivity)
extreme_theta_sets = [(0.8, 0.1, 0.2), (0.7, 0.1, 0.3), (0.6, 0.1, 0.4)]

# ✅ THETA SET LABELS for clear identification
theta_set_labels = {
    (0.6, 0.3, 0.1): "Regular Set 1 (High Base Demand)",
    (0.5, 0.3, 0.2): "Regular Set 2 (Balanced)",
    (0.4, 0.3, 0.3): "Regular Set 3 (High Age Sensitivity)",
    (0.8, 0.1, 0.2): "Extreme Set 1 (Low Price Sensitivity)",
    (0.7, 0.1, 0.3): "Extreme Set 2 (Low Quality Sensitivity)",
    (0.6, 0.1, 0.4): "Extreme Set 3 (Very Low Sensitivity)"
}

# All donation policies to test in one run
donation_policies = ["Early", "End", "Overstock", "Restricted"]

# ✅ MULTIPLE RESTRICTIVE DONATION SETTINGS
# Different weekday configurations to computationally measure impact
restrictive_settings = {
    "Restricted_2days_MonWed": {"name": "Restricted (Mon+Wed)", "days": [0, 2]},
    "Restricted_2days_MonFri": {"name": "Restricted (Mon+Fri)", "days": [0, 4]},
    "Restricted_2days_WedFri": {"name": "Restricted (Wed+Fri)", "days": [2, 4]},
    "Restricted_3days_MonWedFri": {"name": "Restricted (Mon+Wed+Fri)", "days": [0, 2, 4]},
    "Restricted_4days_MonThu": {"name": "Restricted (Mon-Thu)", "days": [0, 1, 2, 3]},
    "Restricted_5days_MonFri": {"name": "Restricted (Mon-Fri)", "days": [0, 1, 2, 3, 4]}
}

# ✅ Definition of WASTE for this simulation:
# WASTE = Products that expire and are neither sold nor donated

# 
# ✅ AGE-BASED DONATION ACCEPTANCE PROBABILITIES:
# - Fresh products (0-2 days): 90% acceptance rate
# - Near-fresh products (3-4 days): 70% acceptance rate  
# - Near-expiry products (5-6 days): 50% acceptance rate
# - Expired/old products (7+ days): 30% acceptance rate
# 
# This addresses the weak assumption that all expired products can be donated.
# In reality, donation organizations have strict quality and timing requirements.
# 

# not after they've already expired (which would be unrealistic).

def run_simulation(product_name, unit_price, shelf_life, scenario_id, replenish_days,
                   reorder_quantity, threshold_level, rho_bar, theta0, theta1, theta2, td, pd, donation_policy, allowed_donation_days=None, markdown_config=None, markdown_timing=None):

    p0 = unit_price
    l0 = shelf_life
    days_to_simulate = 90
    daily_customer_count = 100

    replenishment_frequency = replenish_days
    reorder_threshold = int(threshold_level * reorder_quantity)
    initial_stock = reorder_quantity

    alpha = random.gauss(1, 0.25)
    beta = random.gauss(1, 0.25)

    donation_mode = 1

    inv = Inventory(reorder_threshold=reorder_threshold,
                    donation_policy=donation_policy,
                    donation_mode=donation_mode,
                    allowed_donation_days=allowed_donation_days)

    # ✅ Pass markdown configuration for correlation analysis
    markdown_rates = markdown_config["rates"] if markdown_config else None
    markdown_timing = markdown_timing if markdown_timing else None

    inv.add_stock(product_name, unit_price, initial_stock, shelf_life, p0, l0, td, pd, markdown_rates, markdown_timing)

    results = []

    for day in range(1, days_to_simulate + 1):
        prev_total_donated = inv.total_donated
        prev_total_wasted = inv.total_wasted
        daily_sold, daily_discounted_sales, daily_total_revenue = 0, 0, 0.0

        inv.age_products()

        # ✅ Donation trigger - higher frequency for restricted policy
        if donation_policy.lower() == "restricted":
            # Higher trigger rate for restricted policy since it has day constraints
            trigger_chance = 0.25  # 25% chance per day
        else:
            trigger_chance = 0.10  # 10% chance per day for other policies
            
        if random.random() < trigger_chance:
            # Realistic threshold for overstock donations
            inv.handle_donations(td, pd, stock_threshold=200, current_day=day)

        # ✅ Sales
        for _ in range(daily_customer_count):
            product = inv.sell_product(theta0, theta1, theta2, alpha, beta)
            if product:
                daily_total_revenue += product.price
                daily_sold += 1
                if product.discounted:
                    daily_discounted_sales += 1

        inv.remove_expired_products()

        daily_donated = inv.total_donated - prev_total_donated
        daily_wasted = inv.total_wasted - prev_total_wasted
        daily_inventory = inv.get_inventory_count()

        if day % replenishment_frequency == 0:
            inv.add_stock(product_name, unit_price, reorder_quantity, shelf_life, p0, l0, td, pd, markdown_rates, markdown_timing)

        donation_log = inv.get_donation_summary()
        if daily_donated > 0 and donation_log:
            timings = list(set([entry["Timing"] for entry in donation_log]))
            timing_entry = timings[0] if len(timings) == 1 else ", ".join(timings)
        else:
            timing_entry = "None"

        results.append({
            "Scenario": scenario_id,
            "Day": day,
            "Product": product_name,
            "rho_bar": rho_bar,
            "theta0": theta0,
            "theta1": theta1,
            "theta2": theta2,
            "theta_set_label": theta_set_labels.get((theta0, theta1, theta2), f"Custom ({theta0}, {theta1}, {theta2})"),
            "theta_set_type": "Regular" if (theta0, theta1, theta2) in theta_sets else "Extreme",
            "td": td,
            "pd": pd,
            "Inventory (End of Day)": daily_inventory,
            "Sold (Today)": daily_sold,
            "Discounted Sales (Today)": daily_discounted_sales,
            "Donated (Today)": daily_donated,
            "Wasted (Today)": daily_wasted,
            "Daily Revenue": round(daily_total_revenue, 2),
            "Cumulative Sold": inv.total_sold,
            "Cumulative Discounted Sales": inv.total_discounted_sales,
            "Cumulative Donated": inv.total_donated,
            "Cumulative Wasted": inv.total_wasted,
            "Donation Timing": timing_entry,
            "Donation Policy": donation_policy,
            # ✅ Add markdown configuration for correlation analysis
            "Markdown Policy": markdown_config["name"] if markdown_config else "Default",
            "Markdown Timing": markdown_timing if markdown_timing else "Default",
            "Markdown Rates": str(markdown_config["rates"]) if markdown_config else "Default"
        })

    return results

# ✅ Run simulations for each donation policy SEPARATELY
all_results = []

# Test each donation policy separately
for policy in donation_policies:
    print(f"Running simulation for {policy} donation policy...")
    
    for product in products:
        for scenario in scenario_list:
            # ✅ Test both regular and extreme demand scenarios
            for theta_set in [theta_sets, extreme_theta_sets]:
                for theta0, theta1, theta2 in theta_set:
                    rho_small = (theta0 + theta2) / 4
                    rho_large = (theta0 + theta2) / 2
                    for rho_bar in [rho_small, rho_large]:
                        result = run_simulation(
                            product_name=product["Product Name"],
                            unit_price=product["Price per Unit"],
                            shelf_life=product["Shelf Life"],
                            scenario_id=scenario["scenario_id"],
                            replenish_days=scenario["replenish_days"],
                            reorder_quantity=scenario["reorder_quantity"],
                            threshold_level=scenario["threshold_level"],
                            rho_bar=rho_bar,
                            theta0=theta0,
                            theta1=theta1,
                            theta2=theta2,
                            td=scenario["td"],
                            pd=scenario["pd"],
                            donation_policy=policy
                        )
                        all_results.extend(result)

# ✅ Test multiple restrictive donation settings
print("Running simulations for multiple restrictive donation settings...")
for setting_key, setting_config in restrictive_settings.items():
    print(f"Running simulation for {setting_config['name']}...")

for product in products:
    for scenario in scenario_list:
        # Test both regular and extreme demand scenarios
        for theta_set in [theta_sets, extreme_theta_sets]:
            for theta0, theta1, theta2 in theta_set:
                rho_small = (theta0 + theta2) / 4
                rho_large = (theta0 + theta2) / 2
                for rho_bar in [rho_small, rho_large]:
                        result = run_simulation(
                            product_name=product["Product Name"],
                            unit_price=product["Price per Unit"],
                            shelf_life=product["Shelf Life"],
                            scenario_id=scenario["scenario_id"],
                            replenish_days=scenario["replenish_days"],
                            reorder_quantity=scenario["reorder_quantity"],
                            threshold_level=scenario["threshold_level"],
                            rho_bar=rho_bar,
                            theta0=theta0,
                            theta1=theta1,
                            theta2=theta2,
                            td=scenario["td"],
                            pd=scenario["pd"],
                            donation_policy="Restricted",
                            allowed_donation_days=setting_config["days"]
                        )
                        all_results.extend(result)

# ✅ CORRELATION ANALYSIS: Test different markdown discount rates and timing
print("Running correlation analysis for markdown policies...")

# ✅ MARKDOWN POLICIES for correlation analysis
markdown_configs = [
    # Conservative (original)
    {"name": "Conservative", "rates": [0.10, 0.20, 0.40, 0.60], "timing": 5},
    # Moderate (original)
    {"name": "Moderate", "rates": [0.15, 0.30, 0.50, 0.75], "timing": 5},
    # Aggressive (original)
    {"name": "Aggressive", "rates": [0.20, 0.40, 0.70, 0.85], "timing": 5},
    # Very Aggressive (original)
    {"name": "Very Aggressive", "rates": [0.25, 0.50, 0.80, 0.90], "timing": 5},
    # NEW: Ultra Aggressive
    {"name": "Ultra Aggressive", "rates": [0.30, 0.60, 0.85, 0.95], "timing": 5},
    # NEW: Extreme Aggressive
    {"name": "Extreme Aggressive", "rates": [0.40, 0.70, 0.90, 0.98], "timing": 5},
    # NEW: Early Ultra Aggressive (earlier timing)
    {"name": "Early Ultra", "rates": [0.30, 0.60, 0.85, 0.95], "timing": 6},
    # NEW: Late Ultra Aggressive (later timing)
    {"name": "Late Ultra", "rates": [0.30, 0.60, 0.85, 0.95], "timing": 4}
]

# Test different markdown timing (days before expiry)
markdown_timing = [3, 4, 5, 6]  # Start markdown 3, 4, 5, or 6 days before expiry

for markdown_config in markdown_configs:
    print(f"Testing {markdown_config['name']} markdown rates...")
    
    for timing in markdown_timing:
        for product in products:
            for scenario in scenario_list:
                # Test with regular theta sets only for correlation analysis
                for theta0, theta1, theta2 in theta_sets:
                    rho_bar = (theta0 + theta2) / 4  # Use consistent rho_bar
                    
                    # Create temporary product with modified markdown rates
                    temp_product = product.copy()
                    temp_product["markdown_rates"] = markdown_config["rates"]
                    temp_product["markdown_timing"] = timing
                    
                    result = run_simulation(
                        product_name=product["Product Name"],
                        unit_price=product["Price per Unit"],
                        shelf_life=product["Shelf Life"],
                        scenario_id=scenario["scenario_id"],
                        replenish_days=scenario["replenish_days"],
                        reorder_quantity=scenario["reorder_quantity"],
                        threshold_level=scenario["threshold_level"],
                        rho_bar=rho_bar,
                        theta0=theta0,
                        theta1=theta1,
                        theta2=theta2,
                        td=scenario["td"],
                        pd=scenario["pd"],
                        donation_policy="Early",  # Use Early policy for correlation analysis
                        markdown_config={"name": markdown_config["name"], "rates": markdown_config["rates"]},
                        markdown_timing=markdown_config["timing"]
                    )
                    all_results.extend(result)

df = pd.DataFrame(all_results)
df["Relative Revenue (%)"] = df.groupby(["Product", "Donation Policy"])["Daily Revenue"].transform(lambda x: (x / x.max()) * 100)

# ✅ Save combined results
df.to_csv("multi_product_results_all_policies.csv", index=False)
print("✅ Simulation completed. Results saved to multi_product_results_all_policies.csv")

# ✅ Print simulation assumptions and definitions
print("\n" + "="*80)
print("SIMULATION PARAMETERS:")
print("="*80)
print("Replenishment: 4-day (400 units), 8-day (600 units)")
print("Markdown: Progressive discounting (20%, 40%, 70%, 85%)")
print("Donation Acceptance: Age-based (95%, 85%, 75%, 65%, 45%)")
print("Customer Types: Regular (price sensitive), Extreme (price insensitive)")
print("Restrictive Settings: 2-5 weekdays")
print("="*80)
