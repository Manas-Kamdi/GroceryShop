from django.core.management.base import BaseCommand
from GroceryShopApp.models import Product

class Command(BaseCommand):
    help = 'Set realistic Indian prices for products'

    def handle(self, *args, **options):
        # Realistic Indian grocery prices
        price_mapping = {
            'Fresh Organic Apples': 180.00,
            'Whole Grain Bread': 45.00,
            'Organic Milk 1L': 65.00,
            'Fresh Spinach': 25.00,
            'Free Range Eggs (12 pack)': 120.00,
            'Organic Bananas': 80.00,
            'Whole Chicken': 250.00,
            'Brown Rice 2kg': 180.00,
            'Fresh Carrots': 40.00,
            'Greek Yogurt': 95.00,
            'Fresh Salmon Fillet': 450.00,
            'Organic Tomatoes': 60.00,
            'Whole Wheat Pasta': 85.00,
            'Fresh Strawberries': 150.00,
            'Extra Virgin Olive Oil': 280.00
        }
        
        updated_count = 0
        
        for product in Product.objects.all():
            if product.name in price_mapping:
                product.price = price_mapping[product.name]
                product.save()
                updated_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f'Updated {product.name}: Rs. {product.price}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} products with Indian prices')
        )
