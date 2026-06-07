from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Order, UserProfile

class DeliveryBoyTests(TestCase):
    def setUp(self):
        # Create users
        self.client_user = User.objects.create_user(username="customer", password="password123")
        self.delivery_user = User.objects.create_user(username="deliveryboy", password="password123")
        
        # Ensure profiles exist
        self.client_profile, _ = UserProfile.objects.get_or_create(user=self.client_user)
        self.delivery_profile, _ = UserProfile.objects.get_or_create(user=self.delivery_user)
        self.delivery_profile.is_delivery_boy = True
        self.delivery_profile.save()
        
        # Create order
        self.order = Order.objects.create(
            user=self.client_user,
            order_number="ORD-TEST123",
            total_amount=150.00,
            order_status="confirmed",
            payment_status="paid",
            delivery_name="Customer",
            delivery_phone="1234567890",
            delivery_address="123 Street",
            delivery_area="Area",
            delivery_pincode="123456"
        )

    def test_toggle_delivery_status(self):
        self.client_profile.is_delivery_boy = False
        self.client_profile.save()
        self.client.login(username="customer", password="password123")
        
        # Toggle status (activate)
        response = self.client.post(reverse("toggle_delivery_status"))
        self.client_profile.refresh_from_db()
        self.assertTrue(self.client_profile.is_delivery_boy)
        self.assertRedirects(response, reverse("delivery_dashboard"))
        
        # Toggle status (deactivate)
        response = self.client.post(reverse("toggle_delivery_status"))
        self.client_profile.refresh_from_db()
        self.assertFalse(self.client_profile.is_delivery_boy)
        self.assertRedirects(response, reverse("profile"))

    def test_delivery_dashboard_permission(self):
        # Customer (not delivery boy) should be redirected
        self.client.login(username="customer", password="password123")
        response = self.client.get(reverse("delivery_dashboard"))
        self.assertRedirects(response, reverse("profile"))

        # Delivery boy should be allowed
        self.client.login(username="deliveryboy", password="password123")
        response = self.client.get(reverse("delivery_dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_accept_order(self):
        self.client.login(username="deliveryboy", password="password123")
        
        # Accept order
        response = self.client.post(reverse("delivery_accept_order", args=[self.order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        
        self.order.refresh_from_db()
        self.assertEqual(self.order.delivery_boy, self.delivery_user)
        self.assertEqual(self.order.order_status, "processing")

    def test_update_delivery_status(self):
        self.order.delivery_boy = self.delivery_user
        self.order.order_status = "processing"
        self.order.delivery_otp = "1234"
        self.order.save()
        
        self.client.login(username="deliveryboy", password="password123")
        
        # Update to shipped (does not require OTP)
        response = self.client.post(reverse("delivery_update_status", args=[self.order.id, "shipped"]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_status, "shipped")
        
        # Update to delivered with no OTP (should fail)
        response = self.client.post(reverse("delivery_update_status", args=[self.order.id, "delivered"]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["success"])
        self.assertIn("OTP is required", response.json()["error"])

        # Update to delivered with wrong OTP (should fail)
        response = self.client.post(
            reverse("delivery_update_status", args=[self.order.id, "delivered"]),
            data=dict(otp="0000")
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["success"])
        self.assertIn("Invalid OTP", response.json()["error"])
        
        # Update to delivered with correct OTP (should succeed)
        response = self.client.post(
            reverse("delivery_update_status", args=[self.order.id, "delivered"]),
            data=dict(otp="1234"),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_status, "delivered")
        self.assertEqual(self.order.payment_status, "paid")

