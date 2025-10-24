from django.core.management.base import BaseCommand
from GroceryShopApp.models import Product

class Command(BaseCommand):
    help = 'Create sample products for testing'

    def handle(self, *args, **options):
        sample_products = [
            {
                'name': 'Fresh Organic Apples',
                'description': 'Crisp and juicy organic apples, perfect for snacking or baking.',
                'price': 120.00,
                'stock_quantity': 50,
                'category': 'Fruits & Vegetables'
            },
            {
                'name': 'Whole Grain Bread',
                'description': 'Nutritious whole grain bread made with premium ingredients.',
                'price': 45.00,
                'stock_quantity': 30,
                'category': 'Bakery'
            },
            {
                'name': 'Organic Milk 1L',
                'description': 'Fresh organic milk from grass-fed cows.',
                'price': 80.00,
                'stock_quantity': 25,
                'category': 'Dairy & Eggs'
            },
            {
                'name': 'Fresh Spinach',
                'description': 'Fresh, leafy spinach perfect for salads and cooking.',
                'price': 25.00,
                'stock_quantity': 40,
                'category': 'Fruits & Vegetables'
            },
            {
                'name': 'Free Range Eggs (12 pack)',
                'description': 'Farm-fresh free range eggs from happy hens.',
                'price': 60.00,
                'stock_quantity': 20,
                'category': 'Dairy & Eggs'
            },
            {
                'name': 'Organic Bananas',
                'description': 'Sweet and ripe organic bananas, great for smoothies.',
                'price': 50.00,
                'stock_quantity': 35,
                'category': 'Fruits & Vegetables'
            },
            {
                'name': 'Whole Chicken',
                'description': 'Fresh whole chicken, perfect for roasting.',
                'price': 180.00,
                'stock_quantity': 15,
                'category': 'Meat & Seafood'
            },
            {
                'name': 'Brown Rice 2kg',
                'description': 'Premium brown rice, a healthy grain option.',
                'price': 120.00,
                'stock_quantity': 25,
                'category': 'Pantry'
            },
            {
                'name': 'Fresh Carrots',
                'description': 'Sweet and crunchy fresh carrots, great for snacking.',
                'price': 30.00,
                'stock_quantity': 45,
                'category': 'Fruits & Vegetables'
            },
            {
                'name': 'Greek Yogurt',
                'description': 'Creamy Greek yogurt, high in protein.',
                'price': 65.00,
                'stock_quantity': 20,
                'category': 'Dairy & Eggs'
            },
            {
                'name': 'Fresh Salmon Fillet',
                'description': 'Premium fresh salmon fillet, rich in omega-3.',
                'price': 350.00,
                'stock_quantity': 10,
                'category': 'Meat & Seafood'
            },
            {
                'name': 'Organic Tomatoes',
                'description': 'Juicy organic tomatoes, perfect for salads and cooking.',
                'price': 40.00,
                'stock_quantity': 30,
                'category': 'Fruits & Vegetables'
            },
            {
                'name': 'Whole Wheat Pasta',
                'description': 'Nutritious whole wheat pasta, great for healthy meals.',
                'price': 55.00,
                'stock_quantity': 40,
                'category': 'Pantry'
            },
            {
                'name': 'Fresh Strawberries',
                'description': 'Sweet and juicy fresh strawberries, perfect for desserts.',
                'price': 150.00,
                'stock_quantity': 25,
                'category': 'Fruits & Vegetables'
            },
            {
                'name': 'Extra Virgin Olive Oil',
                'description': 'Premium extra virgin olive oil, perfect for cooking.',
                'price': 280.00,
                'stock_quantity': 20,
                'category': 'Pantry'
            },
            {
                'name': 'Toilet Paper (4 pack)',
                'description': 'Soft and absorbent toilet paper, 4 rolls.',
                'price': 120.00,
                'stock_quantity': 30,
                'category': 'Washroom & Hygiene'
            },
            {
                'name': 'Shampoo 400ml',
                'description': 'Gentle shampoo for all hair types.',
                'price': 180.00,
                'stock_quantity': 25,
                'category': 'Washroom & Hygiene'
            },
            {
                'name': 'Toothpaste',
                'description': 'Fluoride toothpaste for healthy teeth.',
                'price': 85.00,
                'stock_quantity': 40,
                'category': 'Washroom & Hygiene'
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
