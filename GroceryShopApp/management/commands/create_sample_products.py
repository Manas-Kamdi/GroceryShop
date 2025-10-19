from django.core.management.base import BaseCommand
from GroceryShopApp.models import Product

class Command(BaseCommand):
    help = 'Create sample products for testing'

    def handle(self, *args, **options):
        sample_products = [
            {
                'name': 'Fresh Organic Apples',
                'description': 'Crisp and juicy organic apples, perfect for snacking or baking.',
                'price': 3.99,
                'stock_quantity': 50,
                'category': 'Fruits'
            },
            {
                'name': 'Whole Grain Bread',
                'description': 'Nutritious whole grain bread made with premium ingredients.',
                'price': 2.49,
                'stock_quantity': 30,
                'category': 'Bakery'
            },
            {
                'name': 'Organic Milk 1L',
                'description': 'Fresh organic milk from grass-fed cows.',
                'price': 4.99,
                'stock_quantity': 25,
                'category': 'Dairy'
            },
            {
                'name': 'Fresh Spinach',
                'description': 'Fresh, leafy spinach perfect for salads and cooking.',
                'price': 1.99,
                'stock_quantity': 40,
                'category': 'Vegetables'
            },
            {
                'name': 'Free Range Eggs (12 pack)',
                'description': 'Farm-fresh free range eggs from happy hens.',
                'price': 3.49,
                'stock_quantity': 20,
                'category': 'Dairy'
            },
            {
                'name': 'Organic Bananas',
                'description': 'Sweet and ripe organic bananas, great for smoothies.',
                'price': 2.99,
                'stock_quantity': 35,
                'category': 'Fruits'
            },
            {
                'name': 'Whole Chicken',
                'description': 'Fresh whole chicken, perfect for roasting.',
                'price': 8.99,
                'stock_quantity': 15,
                'category': 'Meat'
            },
            {
                'name': 'Brown Rice 2kg',
                'description': 'Premium brown rice, a healthy grain option.',
                'price': 5.99,
                'stock_quantity': 25,
                'category': 'Grains'
            },
            {
                'name': 'Fresh Carrots',
                'description': 'Sweet and crunchy fresh carrots, great for snacking.',
                'price': 1.49,
                'stock_quantity': 45,
                'category': 'Vegetables'
            },
            {
                'name': 'Greek Yogurt',
                'description': 'Creamy Greek yogurt, high in protein.',
                'price': 3.79,
                'stock_quantity': 20,
                'category': 'Dairy'
            },
            {
                'name': 'Fresh Salmon Fillet',
                'description': 'Premium fresh salmon fillet, rich in omega-3.',
                'price': 12.99,
                'stock_quantity': 10,
                'category': 'Seafood'
            },
            {
                'name': 'Organic Tomatoes',
                'description': 'Juicy organic tomatoes, perfect for salads and cooking.',
                'price': 2.79,
                'stock_quantity': 30,
                'category': 'Vegetables'
            },
            {
                'name': 'Whole Wheat Pasta',
                'description': 'Nutritious whole wheat pasta, great for healthy meals.',
                'price': 2.29,
                'stock_quantity': 40,
                'category': 'Grains'
            },
            {
                'name': 'Fresh Strawberries',
                'description': 'Sweet and juicy fresh strawberries, perfect for desserts.',
                'price': 4.49,
                'stock_quantity': 25,
                'category': 'Fruits'
            },
            {
                'name': 'Extra Virgin Olive Oil',
                'description': 'Premium extra virgin olive oil, perfect for cooking.',
                'price': 7.99,
                'stock_quantity': 20,
                'category': 'Pantry'
            }
        ]

        created_count = 0
        for product_data in sample_products:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created product: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new products')
        )
