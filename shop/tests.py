from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Product, Cart, CartItem


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="T-Shirts",
            slug="tshirts",
            description="Cotton t-shirts"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "T-Shirts")
        self.assertEqual(self.category.slug, "tshirts")

    def test_category_str(self):
        self.assertEqual(str(self.category), "T-Shirts")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="T-Shirts",
            slug="tshirts"
        )
        self.product = Product.objects.create(
            name="PyData T-Shirt",
            slug="pydata-tshirt",
            category=self.category,
            description="Quality t-shirt",
            short_description="T-shirt",
            price=15.99,
            stock_quantity=50,
            is_active=True
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "PyData T-Shirt")
        self.assertEqual(self.product.price, 15.99)

    def test_product_str(self):
        self.assertEqual(str(self.product), "PyData T-Shirt")

    def test_discount_calculation(self):
        self.product.old_price = 19.99
        self.product.save()
        self.assertEqual(self.product.discount_percentage, 20)

    def test_slug_auto_generation(self):
        product = Product.objects.create(
            name="New Product",
            category=self.category,
            description="Test",
            price=10.00,
            stock_quantity=10
        )
        self.assertEqual(product.slug, "new-product")


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation(self):
        self.assertEqual(self.cart.user, self.user)

    def test_cart_str(self):
        self.assertEqual(str(self.cart), f"Cart for {self.user.username}")


class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(
            name="T-Shirts",
            slug="tshirts"
        )
        self.product = Product.objects.create(
            name="PyData T-Shirt",
            slug="pydata-tshirt",
            category=self.category,
            description="Quality t-shirt",
            price=15.99,
            stock_quantity=50
        )
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2,
            size="M"
        )

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertEqual(self.cart_item.size, "M")

    def test_cart_item_subtotal(self):
        expected_subtotal = self.product.price * 2
        self.assertEqual(self.cart_item.get_subtotal(), expected_subtotal)


class ShopViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.category = Category.objects.create(
            name="T-Shirts",
            slug="tshirts"
        )
        self.product = Product.objects.create(
            name="PyData T-Shirt",
            slug="pydata-tshirt",
            category=self.category,
            description="Quality t-shirt",
            short_description="T-shirt",
            price=15.99,
            stock_quantity=50,
            is_active=True
        )

    def test_shop_page_loads(self):
        response = self.client.get(reverse('shop:shop'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/shop.html')
        self.assertIn('products', response.context)

    def test_product_detail_page_loads(self):
        response = self.client.get(
            reverse('shop:product_detail', args=[self.product.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_detail.html')
        self.assertEqual(response.context['product'], self.product)

    def test_product_detail_404_for_inactive(self):
        self.product.is_active = False
        self.product.save()
        response = self.client.get(
            reverse('shop:product_detail', args=[self.product.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_product_filtering_by_category(self):
        response = self.client.get(
            reverse('shop:shop'),
            {'category': 'tshirts'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('selected_category', response.context)

    def test_product_search(self):
        response = self.client.get(
            reverse('shop:shop'),
            {'search': 'PyData'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('search_query', response.context)

    def test_product_sorting(self):
        response = self.client.get(
            reverse('shop:shop'),
            {'sort': 'price'}
        )
        self.assertEqual(response.status_code, 200)


class CartViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.category = Category.objects.create(
            name="T-Shirts",
            slug="tshirts"
        )
        self.product = Product.objects.create(
            name="PyData T-Shirt",
            slug="pydata-tshirt",
            category=self.category,
            description="Quality t-shirt",
            price=15.99,
            stock_quantity=50,
            is_active=True
        )

    def test_view_cart_requires_login(self):
        response = self.client.get(reverse('shop:view_cart'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/login/', response.url)

    def test_view_cart_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('shop:view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/cart.html')

    def test_add_to_cart_requires_login(self):
        response = self.client.post(
            reverse('shop:add_to_cart'),
            {'product_id': self.product.id, 'quantity': 1}
        )
        self.assertEqual(response.status_code, 302)

    def test_add_to_cart_creates_cart_item(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('shop:add_to_cart'),
            {'product_id': self.product.id, 'quantity': 2},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().quantity, 2)


class AdminInterfaceTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass'
        )
        self.client = Client()

    def test_admin_site_loads(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
