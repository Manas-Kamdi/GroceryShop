from django.core.management.base import BaseCommand
from GroceryShopApp.models import Product
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Add products with images, details, and prices to the database'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, help='Product name')
        parser.add_argument('--description', type=str, help='Product description')
        parser.add_argument('--price', type=float, help='Product price')
        parser.add_argument('--category', type=str, help='Product category')
        parser.add_argument('--stock', type=int, default=10, help='Stock quantity')
        parser.add_argument('--image', type=str, help='Path to product image file')

    def handle(self, *args, **options):
        # Interactive mode if no arguments provided
        if not any(options.values()):
            self.interactive_mode()
        else:
            self.create_product(options)

    def interactive_mode(self):
        """Interactive mode for adding products"""
        self.stdout.write(self.style.SUCCESS('=== Add New Product ==='))
        
        name = input('Product Name: ')
        description = input('Product Description: ')
        price = float(input('Price (₹): '))
        category = input('Category: ')
        stock = int(input('Stock Quantity (default 10): ') or 10)
        image_path = input('Image Path (optional): ')
        
        product_data = {
            'name': name,
            'description': description,
            'price': price,
            'category': category,
            'stock_quantity': stock,
        }
        
        if image_path and os.path.exists(image_path):
            product_data['image'] = image_path
        
        self.create_product(product_data)

    def create_product(self, data):
        """Create a product with the given data"""
        try:
            product = Product.objects.create(
                name=data['name'],
                description=data['description'],
                price=data['price'],
                category=data['category'],
                stock_quantity=data.get('stock_quantity', 10)
            )
            
            # Handle image if provided
            if 'image' in data and data['image']:
                if os.path.exists(data['image']):
                    # Copy image to media directory
                    import shutil
                    from pathlib import Path
                    
                    media_dir = settings.MEDIA_ROOT / 'products'
                    media_dir.mkdir(exist_ok=True)
                    
                    filename = f"{product.id}_{os.path.basename(data['image'])}"
                    dest_path = media_dir / filename
                    
                    shutil.copy2(data['image'], dest_path)
                    product.image = f'products/{filename}'
                    product.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Image copied to: {dest_path}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Image file not found: {data["image"]}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Product created: {product.name} (₹{product.price})')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating product: {str(e)}')
            )

    def add_sample_products(self):
        """Add sample products with different categories"""
        sample_products = [
            {
                'name': 'Premium Basmati Rice 1kg',
                'description': 'Long grain basmati rice, perfect for biryani and pulao',
                'price': 120.00,
                'category': 'Grains',
                'stock_quantity': 50
            },
            {
                'name': 'Fresh Mangoes (1 dozen)',
                'description': 'Sweet and juicy alphonso mangoes, perfect for summer',
                'price': 180.00,
                'category': 'Fruits',
                'stock_quantity': 30
            },
            {
                'name': 'Organic Turmeric Powder 100g',
                'description': 'Pure organic turmeric powder, great for cooking and health',
                'price': 45.00,
                'category': 'Spices',
                'stock_quantity': 25
            },
            {
                'name': 'Fresh Chicken Breast 500g',
                'description': 'Fresh chicken breast, perfect for healthy cooking',
                'price': 180.00,
                'category': 'Meat',
                'stock_quantity': 15
            },
            {
                'name': 'Paneer 200g',
                'description': 'Fresh cottage cheese, great for curries and snacks',
                'price': 60.00,
                'category': 'Dairy',
                'stock_quantity': 20
            }
        ]
        
        for product_data in sample_products:
            self.create_product(product_data)
        
        self.stdout.write(
            self.style.SUCCESS('✅ Sample products added successfully!')
        )
