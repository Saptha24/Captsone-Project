import random

class Product:
    def __init__(self, name, price, stock, shelf_life, p0, l0, td, pd, markdown_rates=None, markdown_timing=None):
        self.name = name
        self.price = price
        self.stock = stock
        self.shelf_life = shelf_life
        self.age = 0
        self.discounted = False
        self.p0 = p0  # original price
        self.l0 = l0  # original shelf life
        self.td = td
        self.pd = pd
        # ✅ Support for dynamic markdown rates and timing
        self.markdown_rates = markdown_rates or [0.20, 0.40, 0.70, 0.85]  # Default aggressive rates
        self.markdown_timing = markdown_timing or 5  # Default: start 5 days before expiry

    # def age_one_day(self):
    #     self.age += 1
    #     if self.age >= self.shelf_life - 2 and not self.discounted:
    #         self.price *= 0.5
    #         self.discounted = True

    def age_one_day(self):
        self.age += 1
        days_left = self.shelf_life - self.age

        # ✅ DYNAMIC MARKDOWN POLICIES for correlation analysis
        # Use configurable markdown rates and timing
        if days_left == self.markdown_timing and self.discounted is False:
            self.price = round(self.p0 * (1 - self.markdown_rates[0]), 2)
            self.discounted = f"{self.markdown_rates[0]*100:.0f}%"

        elif days_left == (self.markdown_timing - 1) and self.discounted == f"{self.markdown_rates[0]*100:.0f}%":
            self.price = round(self.p0 * (1 - self.markdown_rates[1]), 2)
            self.discounted = f"{self.markdown_rates[1]*100:.0f}%"

        elif days_left == (self.markdown_timing - 2) and self.discounted == f"{self.markdown_rates[1]*100:.0f}%":
            self.price = round(self.p0 * (1 - self.markdown_rates[2]), 2)
            self.discounted = f"{self.markdown_rates[2]*100:.0f}%"

        elif days_left == (self.markdown_timing - 3) and self.discounted == f"{self.markdown_rates[2]*100:.0f}%":
            self.price = round(self.p0 * (1 - self.markdown_rates[3]), 2)
            self.discounted = f"{self.markdown_rates[3]*100:.0f}%"


    def is_expired(self):
        return self.age >= self.shelf_life

    """def get_demand_probability(self, theta0, theta1, theta2, alpha, beta):
        term1 = theta0
        term2 = theta1 * ((1 - self.price / self.p0) ** alpha)
        term3 = theta2 * ((1 - self.age / self.l0) ** beta)
        return term1 + term2 + term3"""
    
    def get_demand_probability(self, theta0, theta1, theta2, alpha, beta):
        # Exact demand probability formula
        price_term = (1 - (self.price / self.p0)) ** alpha
        age_term = (1 - (self.age / self.l0)) ** beta

        rho = theta0 + theta1 * price_term + theta2 * age_term
        return max(0, min(1, rho))  # Clamp to [0, 1]