from django.core.management.base import BaseCommand
from GroceryShopApp.models import Product

class Command(BaseCommand):
    help = 'Add washroom and hygiene products to the database'

    def handle(self, *args, **options):
        washroom_products = [
            {
                'name': 'Harpic Toilet Cleaner 500ml',
                'description': 'Powerful toilet cleaner that kills 99.9% of germs and bacteria. Leaves your toilet sparkling clean.',
                'price': 85.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 25
            },
            {
                'name': 'Dettol Hand Sanitizer 100ml',
                'description': 'Alcohol-based hand sanitizer that kills 99.9% of germs. Perfect for on-the-go hygiene.',
                'price': 45.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 50
            },
            {
                'name': 'Lifebuoy Soap 75g (Pack of 4)',
                'description': 'Antibacterial soap that provides 24-hour protection against germs. Gentle on skin.',
                'price': 60.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 40
            },
            {
                'name': 'Colgate Toothpaste 150g',
                'description': 'Complete care toothpaste with fluoride for strong teeth and healthy gums.',
                'price': 55.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 30
            },
            {
                'name': 'Lizol Floor Cleaner 1L',
                'description': 'Multi-surface floor cleaner that kills germs and leaves a fresh fragrance.',
                'price': 120.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 20
            },
            {
                'name': 'Dettol Antiseptic Liquid 100ml',
                'description': 'Antiseptic liquid for first aid and general hygiene. Kills germs effectively.',
                'price': 35.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 35
            },
            {
                'name': 'Vim Dishwash Liquid 500ml',
                'description': 'Powerful dishwashing liquid that cuts through grease and leaves dishes sparkling clean.',
                'price': 65.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 25
            },
            {
                'name': 'Pears Soap 75g (Pack of 3)',
                'description': 'Gentle glycerin soap for sensitive skin. Moisturizes while cleansing.',
                'price': 75.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 30
            },
            {
                'name': 'Closeup Toothpaste 100g',
                'description': 'Red gel toothpaste with cooling crystals for fresh breath and strong teeth.',
                'price': 40.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 35
            },
            {
                'name': 'Himalaya Face Wash 100ml',
                'description': 'Natural face wash with neem and turmeric. Gentle cleansing for all skin types.',
                'price': 95.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 20
            },
            {
                'name': 'Dettol Hand Wash 200ml',
                'description': 'Antibacterial hand wash that kills germs and keeps hands soft and clean.',
                'price': 70.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 25
            },
            {
                'name': 'Patanjali Kesh Kanti Shampoo 200ml',
                'description': 'Natural herbal shampoo for healthy hair growth and scalp care.',
                'price': 80.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 15
            },
            {
                'name': 'Lux Soap 75g (Pack of 5)',
                'description': 'Luxurious soap with moisturizing cream for soft and smooth skin.',
                'price': 90.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 30
            },
            {
                'name': 'Sensodyne Toothpaste 75g',
                'description': 'Sensitive teeth toothpaste that provides relief from tooth sensitivity.',
                'price': 110.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 20
            },
            {
                'name': 'Domex Toilet Cleaner 500ml',
                'description': 'Powerful toilet cleaner with bleach that removes tough stains and kills germs.',
                'price': 75.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 25
            },
            {
                'name': 'Pond\'s Face Wash 100ml',
                'description': 'Gentle face wash that removes dirt and oil while keeping skin soft and supple.',
                'price': 65.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 25
            },
            {
                'name': 'Head & Shoulders Shampoo 200ml',
                'description': 'Anti-dandruff shampoo that keeps scalp healthy and hair beautiful.',
                'price': 85.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 20
            },
            {
                'name': 'Dettol Multi-Use Disinfectant 500ml',
                'description': 'Multi-purpose disinfectant for cleaning and sanitizing various surfaces.',
                'price': 95.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 15
            },
            {
                'name': 'Colgate Mouthwash 250ml',
                'description': 'Antibacterial mouthwash that kills germs and provides long-lasting fresh breath.',
                'price': 55.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 25
            },
            {
                'name': 'Himalaya Baby Soap 75g',
                'description': 'Gentle baby soap with natural ingredients. Safe for delicate baby skin.',
                'price': 35.00,
                'category': 'Washroom & Hygiene',
                'stock_quantity': 20
            }
        ]

        created_count = 0
        for product_data in washroom_products:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created product: {product.name} - Rs. {product.price}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} washroom & hygiene products')
        )
