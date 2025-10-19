from django.core.management.base import BaseCommand
from GroceryShopApp.models import Product

class Command(BaseCommand):
    help = 'Update product prices to rupees (convert from dollars to rupees)'

    def handle(self, *args, **options):
        # Conversion rate: 1 USD = 83 INR (approximate)
        conversion_rate = 83
        
        products = Product.objects.all()
        updated_count = 0
        
        for product in products:
            # Convert price from dollars to rupees
            new_price = float(product.price) * conversion_rate
            product.price = round(new_price, 2)
            product.save()
            updated_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Updated {product.name}: Rs. {product.price}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} products to rupees')
        )
