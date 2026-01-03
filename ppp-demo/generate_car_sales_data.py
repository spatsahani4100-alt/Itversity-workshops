import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# US Auto Industry Seasonal Pattern - Monthly Multipliers
MONTHLY_MULTIPLIERS = {
    1: 0.75,   # January - Low (post-holiday)
    2: 0.80,   # February - Low (winter)
    3: 1.10,   # March - High (spring, tax refunds)
    4: 1.15,   # April - High (spring)
    5: 1.25,   # May - Peak (spring peak)
    6: 1.30,   # June - Peak (summer peak)
    7: 1.25,   # July - Peak (summer)
    8: 1.10,   # August - High (back-to-school)
    9: 0.95,   # September - Moderate (model transition)
    10: 1.00,  # October - Moderate
    11: 1.05,  # November - Moderate
    12: 1.20   # December - Peak (year-end clearance)
}

# Data generation parameters
BASE_RECORDS_PER_MONTH = 100000
START_YEAR = 2015
END_YEAR = 2024
OUTPUT_FOLDER = 'car_sales_data'

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Car makes and models with realistic prices
car_inventory = [
    {'make': 'Toyota', 'model': 'Camry', 'base_price': 28000, 'category': 'Sedan'},
    {'make': 'Toyota', 'model': 'RAV4', 'base_price': 32000, 'category': 'SUV'},
    {'make': 'Toyota', 'model': 'Corolla', 'base_price': 22000, 'category': 'Sedan'},
    {'make': 'Honda', 'model': 'Accord', 'base_price': 29000, 'category': 'Sedan'},
    {'make': 'Honda', 'model': 'CR-V', 'base_price': 33000, 'category': 'SUV'},
    {'make': 'Honda', 'model': 'Civic', 'base_price': 24000, 'category': 'Sedan'},
    {'make': 'Ford', 'model': 'F-150', 'base_price': 42000, 'category': 'Truck'},
    {'make': 'Ford', 'model': 'Explorer', 'base_price': 38000, 'category': 'SUV'},
    {'make': 'Ford', 'model': 'Escape', 'base_price': 30000, 'category': 'SUV'},
    {'make': 'Chevrolet', 'model': 'Silverado', 'base_price': 40000, 'category': 'Truck'},
    {'make': 'Chevrolet', 'model': 'Equinox', 'base_price': 29000, 'category': 'SUV'},
    {'make': 'Chevrolet', 'model': 'Malibu', 'base_price': 26000, 'category': 'Sedan'},
    {'make': 'Tesla', 'model': 'Model 3', 'base_price': 45000, 'category': 'Electric'},
    {'make': 'Tesla', 'model': 'Model Y', 'base_price': 52000, 'category': 'Electric'},
    {'make': 'BMW', 'model': '3 Series', 'base_price': 45000, 'category': 'Luxury'},
    {'make': 'BMW', 'model': 'X5', 'base_price': 65000, 'category': 'Luxury'},
    {'make': 'Mercedes', 'model': 'C-Class', 'base_price': 48000, 'category': 'Luxury'},
    {'make': 'Mercedes', 'model': 'GLE', 'base_price': 62000, 'category': 'Luxury'},
    {'make': 'Nissan', 'model': 'Altima', 'base_price': 27000, 'category': 'Sedan'},
    {'make': 'Nissan', 'model': 'Rogue', 'base_price': 31000, 'category': 'SUV'},
    {'make': 'Hyundai', 'model': 'Sonata', 'base_price': 26500, 'category': 'Sedan'},
    {'make': 'Hyundai', 'model': 'Tucson', 'base_price': 29500, 'category': 'SUV'},
    {'make': 'Mazda', 'model': 'CX-5', 'base_price': 30000, 'category': 'SUV'},
    {'make': 'Mazda', 'model': 'Mazda3', 'base_price': 23500, 'category': 'Sedan'},
]

colors = ['White', 'Black', 'Silver', 'Gray', 'Blue', 'Red', 'Green', 'Brown']
dealerships = ['Downtown Motors', 'Westside Auto', 'Eastside Dealers', 'North Point Cars', 'South Bay Autos']
payment_methods = ['Cash', 'Finance', 'Lease']
finance_weights = [0.15, 0.60, 0.25]  # More realistic distribution

salespeople = [
    'John Smith', 'Sarah Johnson', 'Michael Brown', 'Emily Davis', 'Robert Wilson',
    'Jennifer Martinez', 'David Anderson', 'Lisa Taylor', 'James Thomas', 'Mary Jackson'
]

states = ['CA', 'TX', 'FL', 'NY', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']


def get_days_in_month(year, month):
    """Get the number of days in a given month"""
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    else:  # February
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return 29
        else:
            return 28


def generate_month_data(year, month, num_records, customer_id_offset, sale_id_offset):
    """Generate sales data for a specific month"""
    sales_data = []
    days_in_month = get_days_in_month(year, month)
    
    # Adjust car year based on the data year
    if year <= 2016:
        car_year_choices = [year - 1, year]
        car_year_weights = [0.3, 0.7]
    else:
        car_year_choices = [year - 1, year]
        car_year_weights = [0.3, 0.7]
    
    for i in range(num_records):
        # Random day within the month
        day = random.randint(1, days_in_month)
        sale_date = datetime(year, month, day)
        
        # Select random car
        car = random.choice(car_inventory)
        
        # Add price variation (-5% to +15%)
        price_variation = random.uniform(-0.05, 0.15)
        sale_price = round(car['base_price'] * (1 + price_variation), 2)
        
        # Generate other attributes
        color = random.choice(colors)
        dealership = random.choice(dealerships)
        payment_method = random.choices(payment_methods, weights=finance_weights)[0]
        salesperson = random.choice(salespeople)
        state = random.choice(states)
        
        # Car year
        car_year = random.choices(car_year_choices, weights=car_year_weights)[0]
        
        # Mileage (new cars have 5-50 miles)
        mileage = random.randint(5, 50)
        
        # Customer ID (anonymous)
        customer_id = f'CUST{customer_id_offset + i:07d}'
        
        # Sale ID
        sale_id = f'SALE{sale_id_offset + i:08d}'
        
        # Commission (2-5% of sale price)
        commission_rate = random.uniform(0.02, 0.05)
        commission = round(sale_price * commission_rate, 2)
        
        sales_data.append({
            'sale_id': sale_id,
            'sale_date': sale_date.strftime('%Y-%m-%d'),
            'customer_id': customer_id,
            'car_make': car['make'],
            'car_model': car['model'],
            'car_year': car_year,
            'category': car['category'],
            'color': color,
            'mileage': mileage,
            'sale_price': sale_price,
            'payment_method': payment_method,
            'dealership': dealership,
            'salesperson': salesperson,
            'state': state,
            'commission': commission
        })
    
    return sales_data


# Main generation loop
print("=" * 80)
print("CAR SALES DATA GENERATOR - US AUTO INDUSTRY SEASONAL PATTERN")
print("=" * 80)
print(f"\nGenerating data from {START_YEAR} to {END_YEAR}")
print(f"Base records per month: {BASE_RECORDS_PER_MONTH:,}")
print(f"Output folder: {OUTPUT_FOLDER}/")
print("\nMonthly multipliers applied:")
for month_num, multiplier in MONTHLY_MULTIPLIERS.items():
    month_name = datetime(2024, month_num, 1).strftime('%B')
    expected_records = int(BASE_RECORDS_PER_MONTH * multiplier)
    print(f"  {month_name:12s} ({month_num:2d}): {multiplier:.2f}x = ~{expected_records:,} records")

print("\n" + "=" * 80)
print("Starting generation...\n")

total_records = 0
total_revenue = 0
customer_id_offset = 1000000
sale_id_offset = 20000000
monthly_stats = []

for year in range(START_YEAR, END_YEAR + 1):
    for month in range(1, 13):
        # Calculate number of records for this month
        num_records = int(BASE_RECORDS_PER_MONTH * MONTHLY_MULTIPLIERS[month])
        
        # Generate data for this month
        month_data = generate_month_data(year, month, num_records, customer_id_offset, sale_id_offset)
        
        # Create DataFrame
        df = pd.DataFrame(month_data)
        df = df.sort_values('sale_date').reset_index(drop=True)
        
        # Calculate revenue for this month
        month_revenue = df['sale_price'].sum()
        
        # Save to CSV file
        output_filename = f"{OUTPUT_FOLDER}/sales_{year}_{month:02d}.csv"
        df.to_csv(output_filename, index=False)
        
        # Update counters
        total_records += num_records
        total_revenue += month_revenue
        customer_id_offset += num_records
        sale_id_offset += num_records
        
        # Store stats
        monthly_stats.append({
            'year': year,
            'month': month,
            'records': num_records,
            'revenue': month_revenue
        })
        
        # Progress reporting
        month_name = datetime(year, month, 1).strftime('%B')
        print(f"✓ {year}-{month:02d} ({month_name:12s}): {num_records:>7,} records | "
              f"Revenue: ${month_revenue:>14,.2f} | File: {output_filename}")

print("\n" + "=" * 80)
print("GENERATION COMPLETE!")
print("=" * 80)

# Summary statistics
print(f"\nTotal files generated: {len(monthly_stats)}")
print(f"Total records: {total_records:,}")
print(f"Total revenue: ${total_revenue:,.2f}")
print(f"Average sale price: ${total_revenue / total_records:,.2f}")

# Seasonal analysis
stats_df = pd.DataFrame(monthly_stats)
print("\n" + "-" * 80)
print("SEASONAL ANALYSIS")
print("-" * 80)

print("\nAverage records by month (across all years):")
monthly_avg = stats_df.groupby('month')['records'].mean()
for month_num, avg_records in monthly_avg.items():
    month_name = datetime(2024, month_num, 1).strftime('%B')
    multiplier = MONTHLY_MULTIPLIERS[month_num]
    print(f"  {month_name:12s}: {avg_records:>8,.0f} records ({multiplier:.2f}x)")

print("\nTotal records by year:")
yearly_totals = stats_df.groupby('year')['records'].sum()
for year, total in yearly_totals.items():
    print(f"  {year}: {total:>10,} records")

# Calculate quarterly stats
stats_df['quarter'] = stats_df['month'].apply(lambda m: (m - 1) // 3 + 1)
quarterly_avg = stats_df.groupby('quarter')['records'].sum()
print("\nTotal records by quarter (all years combined):")
for quarter, total in quarterly_avg.items():
    print(f"  Q{quarter}: {total:>10,} records")

print("\n" + "=" * 80)
print(f"All files saved in: {OUTPUT_FOLDER}/")
print("=" * 80)
