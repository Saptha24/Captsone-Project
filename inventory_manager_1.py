from product_1 import Product
import random

class Inventory:
    def __init__(self, reorder_threshold=10, donation_policy="end", donation_mode=1, allowed_donation_days=None):
        self.products = []
        self.reorder_threshold = reorder_threshold
        self.donation_policy = donation_policy  
        self.donation_mode = donation_mode 
        self.donation_log = [] 
        # ✅ Support for multiple restrictive donation settings
        self.allowed_donation_days = allowed_donation_days or [0, 2, 4]  # Default: Mon, Wed, Fri

        # Stats
        self.total_sold = 0
        self.total_discounted_sales = 0
        self.total_donated = 0
        self.total_wasted = 0
        self.total_reorders = 0

    def add_stock(self, name, price, quantity, shelf_life, p0, l0, td, pd, markdown_rates=None, markdown_timing=None):
        for _ in range(quantity):
            self.products.append(Product(name, price, 1, shelf_life, p0, l0, td, pd, markdown_rates, markdown_timing))
        self.total_reorders += 1

    def age_products(self):
        for p in self.products:
            p.age_one_day()
        # ✅ Reset daily donation log at the start of each day
        self.donation_log.clear()

    def remove_expired_products(self):
        still_good = []
        for p in self.products:
            if p.is_expired():
                if self.donation_mode == 3:
                    self.total_donated += 1  # Mode 3: donate expired products
                else:
                    self.total_wasted += 1
            else:
                still_good.append(p)
        self.products = still_good

    def get_inventory_count(self):
        return len(self.products)

    def sell_product(self, theta0, theta1, theta2, alpha, beta):
        if not self.products:
            return None

        best_product = None
        best_prob = 0

        for product in self.products:
            prob = product.get_demand_probability(theta0, theta1, theta2, alpha, beta)
            if prob > best_prob:
                best_product = product
                best_prob = prob

        if best_product and random.random() < best_prob:
            self.products.remove(best_product)
            self.total_sold += 1
            if best_product.discounted:
                self.total_discounted_sales += 1
            return best_product
        return None

    def check_and_reorder(self, name, price, shelf_life, reorder_quantity, p0, l0, td, pd):
        reordered = False
        if self.get_inventory_count() < self.reorder_threshold:
            self.add_stock(name, price, reorder_quantity, shelf_life, p0, l0, td, pd)
            reordered = True
        return reordered

    def handle_donations(self, td, pd, stock_threshold=50, current_day=None):
        self.daily_donations = 0
        # ✅ Ensure fresh log every time donations are handled
        self.donation_log.clear()

        for p in list(self.products):
            donate_flag = False
            timing = None
            donation_accepted = False

            # ✅ Age-based acceptance probability function
            def get_acceptance_rate(age, shelf_life):
                """Age-based donation acceptance rate with higher probabilities for expired products"""
                if age <= 2:  # Fresh products (0-2 days)
                    return 0.95  # Increased from 0.90
                elif age <= 4:  # Near-fresh (3-4 days)
                    return 0.85  # Increased from 0.70
                elif age <= 6:  # Near-expiry (5-6 days)
                    return 0.75  # Increased from 0.50
                elif age <= shelf_life:  # Expired but within shelf life range
                    return 0.65  # Increased from 0.30
                else:  # Very old (beyond shelf life)
                    return 0.45  # Still reasonable for very old products

            # ✅ End-of-life donation - donate EXACTLY when product expires
            if self.donation_policy.lower() == "end":
                if p.age == p.shelf_life:  # ✅ EXACTLY on expiry day, not after
                    acceptance_rate = get_acceptance_rate(p.age, p.shelf_life)
                    if random.random() < acceptance_rate:
                        donate_flag = True
                        timing = f"End of Shelf Life (Accepted, {acceptance_rate*100:.0f}%)"
                        donation_accepted = True
                    else:
                        # Product becomes waste if donation is rejected
                        donate_flag = False
                        timing = f"End of Shelf Life (Rejected, {acceptance_rate*100:.0f}%)"
                elif p.age > p.shelf_life:
                    # Product is already expired - should have been handled earlier
                    # This should not happen in "End of Shelf Life" policy
                    donate_flag = False
                    timing = "Already Expired (Missed Donation Window)"

            # ✅ Early donation with age-based acceptance
            elif self.donation_policy.lower() == "early":
                prob = random.random()
                if p.age >= p.shelf_life:
                    # Expired products
                    acceptance_rate = get_acceptance_rate(p.age, p.shelf_life)
                    if random.random() < acceptance_rate:
                        donate_flag = True
                        timing = f"End of Shelf Life (Accepted, {acceptance_rate*100:.0f}%)"
                        donation_accepted = True
                    else:
                        donate_flag = False
                        timing = f"End of Shelf Life (Rejected, {acceptance_rate*100:.0f}%)"
                elif p.age >= (p.shelf_life - td):
                    # Near expiry: during markdown period
                    acceptance_rate = get_acceptance_rate(p.age, p.shelf_life)
                    if random.random() < acceptance_rate:
                        donate_flag = True
                        timing = f"During Markdown (Accepted, {acceptance_rate*100:.0f}%)"
                        donation_accepted = True
                    else:
                        donate_flag = False
                        timing = f"During Markdown (Rejected, {acceptance_rate*100:.0f}%)"
                elif prob < pd:
                    # Fresh products: before markdown
                    acceptance_rate = get_acceptance_rate(p.age, p.shelf_life)
                    if random.random() < acceptance_rate:
                        donate_flag = True
                        timing = f"Before Markdown (Accepted, {acceptance_rate*100:.0f}%)"
                        donation_accepted = True
                    else:
                        donate_flag = False
                        timing = f"Before Markdown (Rejected, {acceptance_rate*100:.0f}%)"

            # ✅ Overstock donation with age-based acceptance
            elif self.donation_policy.lower() == "overstock":
                if self.get_inventory_count() > stock_threshold:
                    acceptance_rate = get_acceptance_rate(p.age, p.shelf_life)
                    if random.random() < acceptance_rate:
                        donate_flag = True
                        timing = f"Overstock (Accepted, {acceptance_rate*100:.0f}%)"
                        donation_accepted = True
                    else:
                        donate_flag = False
                        timing = f"Overstock (Rejected, {acceptance_rate*100:.0f}%)"

            # ✅ RESTRICTED donation policy with age-based acceptance
            elif self.donation_policy.lower() == "restricted":
                # ✅ Use actual simulation day to determine day of week
                if current_day is not None:
                    # 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday, 6=Sunday
                    current_day_of_week = (current_day - 1) % 7  # Adjust for 1-based day numbering
                else:
                    # Fallback to old method if current_day not provided
                    current_day_of_week = (len(self.donation_log) + 1) % 7
                
                # ✅ Use configurable donation days instead of hardcoded
                if current_day_of_week in self.allowed_donation_days:
                    prob = random.random()
                    if p.age >= p.shelf_life:
                        # Expired products
                        acceptance_rate = get_acceptance_rate(p.age, p.shelf_life)
                        if random.random() < acceptance_rate:
                            donate_flag = True
                            timing = f"End of Shelf Life (Restricted Day, Accepted, {acceptance_rate*100:.0f}%)"
                            donation_accepted = True
                        else:
                            donate_flag = False
                            timing = f"End of Shelf Life (Restricted Day, Rejected, {acceptance_rate*100:.0f}%)"
                    elif p.age >= (p.shelf_life - td):
                        # Near expiry: during markdown period
                        acceptance_rate = get_acceptance_rate(p.age, p.shelf_life)
                        if random.random() < acceptance_rate:
                            donate_flag = True
                            timing = f"During Markdown (Restricted Day, Accepted, {acceptance_rate*100:.0f}%)"
                            donation_accepted = True
                        else:
                            donate_flag = False
                            timing = f"During Markdown (Restricted Day, Rejected, {acceptance_rate*100:.0f}%)"
                    elif prob < pd:
                        # Fresh products: before markdown
                        acceptance_rate = get_acceptance_rate(p.age, p.shelf_life)
                        if random.random() < acceptance_rate:
                            donate_flag = True
                            timing = f"Before Markdown (Restricted Day, Accepted, {acceptance_rate*100:.0f}%)"
                            donation_accepted = True
                        else:
                            donate_flag = False
                            timing = f"Before Markdown (Restricted Day, Rejected, {acceptance_rate*100:.0f}%)"

            # ✅ Apply donation or waste based on acceptance
            if donate_flag and donation_accepted:
                self.products.remove(p)
                self.daily_donations += 1
                self.total_donated += 1
                self.donation_log.append({
                    "Product": p.name,
                    "Timing": timing,
                    "Age": p.age,
                    "Shelf_Life": p.shelf_life
                })
            elif not donate_flag or not donation_accepted:
                # Product becomes waste if donation is rejected or not attempted
                if timing and "Rejected" in timing:
                    # Remove from inventory and count as waste
                    self.products.remove(p)
                    self.total_wasted += 1
                    self.donation_log.append({
                        "Product": p.name,
                        "Timing": timing,
                        "Age": p.age,
                        "Shelf_Life": p.shelf_life,
                        "Status": "Waste"
                })

    def get_donation_summary(self):
        return self.donation_log
