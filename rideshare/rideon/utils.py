"""
Utility functions for ride calculations
"""
from decimal import Decimal

# Centralized fare calculation constants
BASE_FARE = Decimal('100.00')  # Base fare in Naira
PER_KM_RATE = Decimal('50.00')  # Rate per kilometer in Naira

def calculate_fare(distance_km):
    """
    Calculate ride fare based on distance
    
    Args:
        distance_km (float): Distance in kilometers
        
    Returns:
        Decimal: Calculated fare in Naira
    """
    if not distance_km or distance_km < 0:
        return BASE_FARE
    
    distance = Decimal(str(distance_km))
    return BASE_FARE + (distance * PER_KM_RATE)

def get_fare_info():
    """
    Get fare calculation information for frontend display
    
    Returns:
        dict: Dictionary containing base fare and per km rate
    """
    return {
        'base_fare': float(BASE_FARE),
        'per_km_rate': float(PER_KM_RATE),
        'currency': 'NGN',
        'currency_symbol': '₦'
    }
