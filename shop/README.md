# PyData Shop - E-Commerce System Setup Guide

## Overview
A modern, scalable e-commerce application built with Django and Tailwind CSS. Features a responsive navigation bar, product catalog with filtering, shopping cart, and admin management interface.

## 🚀 Quick Start

### 1. Create Database Migrations
```bash
# From the project root directory
python manage.py makemigrations shop
python manage.py migrate
```

### 2. Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 3. Run Development Server
```bash
python manage.py runserver
```

Visit:
- **Shop**: http://localhost:8000/shop/
- **Admin**: http://localhost:8000/admin/

---

## 📊 Models Structure

### Category
- **name**: Category name (e.g., "T-Shirts", "Hoodies", "Accessories")
- **slug**: URL-friendly identifier (auto-generated)
- **description**: Category description
- **image**: Category image

### Product
- **name**: Product name
- **slug**: URL-friendly identifier
- **category**: Foreign key to Category
- **description**: Detailed product description
- **short_description**: Brief description (200 chars)
- **price**: Current price
- **old_price**: Original price (for discount calculation)
- **image**: Main product image
- **gallery_images**: JSON array of additional images
- **available_sizes**: JSON array (e.g., ["S", "M", "L", "XL"])
- **stock_quantity**: Number of items in stock
- **is_featured**: Featured product flag
- **is_active**: Active/inactive status

### Cart
- **user**: One-to-one relationship with User
- **created_at**: When cart was created
- **updated_at**: Last update time

### CartItem
- **cart**: Foreign key to Cart
- **product**: Foreign key to Product
- **quantity**: Quantity ordered
- **size**: Selected size
- **added_at**: When item was added

---

## 🔧 Admin Setup

### Add Categories
1. Go to http://localhost:8000/admin/
2. Click "Categories"
3. Click "Add Category"
4. Fill in:
   - **Name**: e.g., "T-Shirts"
   - **Description**: e.g., "High-quality PyData Kampala t-shirts"
   - **Image**: Upload category image

### Add Products
1. Go to http://localhost:8000/admin/shop/product/
2. Click "Add Product"
3. Fill in all required fields:
   - **Name**: Product name
   - **Category**: Select category
   - **Description**: Detailed description
   - **Price**: Product price
   - **Image**: Main product image
   - **Available Sizes**: ["S", "M", "L", "XL"] (JSON format)
   - **Stock Quantity**: Number in stock
   - **Is Featured**: Check if you want it on featured section

---

## 🛣️ URL Routes

```
/shop/                              → Shop listing page (with filters)
/shop/product/<slug>/               → Product detail page
/shop/cart/                          → View shopping cart
/shop/cart/add/                      → Add to cart (POST)
/shop/cart/item/<id>/remove/         → Remove from cart (POST)
/shop/cart/item/<id>/update/         → Update item quantity (POST)
/shop/featured/                      → Featured products
```

---

## 🎨 Navigation Bar Features

### Desktop Navigation
- **🛍️ Merch / Shop**: Main CTA button (orange gradient)
- **📁 Categories**: Dropdown (T-Shirts, Hoodies, Accessories)
- **About**: Link to about page
- **Events**: Link to events page
- **Contact**: Link to conduct page
- **🛒 Cart**: Icon with item count
- **👤 User Account**: Dropdown for authenticated users
- **Search**: Search bar for products

### Mobile Navigation
- Hamburger menu
- Same navigation items in drawer
- Search bar in header
- All features accessible

---

## 🎯 Key Features

### Shop Page (`/shop/`)
✅ Product grid (3 columns on desktop)
✅ Filtering sidebar:
  - Category filter
  - Price range slider
  - Size selection
✅ Sorting options:
  - Latest
  - Price (Low-High)
  - Price (High-Low)
  - Name (A-Z)
  - Most In Stock
✅ Pagination (12 products per page)
✅ Search functionality
✅ Product status badges (In Stock, Limited, Out of Stock)
✅ Discount badges
✅ Featured product badges

### Product Detail Page (`/shop/product/<slug>/`)
✅ Large product image with zoom
✅ Image gallery with thumbnails
✅ Detailed product description
✅ Price with discount display
✅ Size selection (if available)
✅ Quantity selector
✅ Add to cart functionality
✅ Stock status indicator
✅ Related products section
✅ Star rating (placeholder)
✅ Share buttons (placeholder)

### Shopping Cart (`/shop/cart/`)
✅ List all cart items
✅ Product images and details
✅ Quantity adjustment
✅ Remove items
✅ Order summary
✅ Total calculation
✅ Proceed to checkout button
✅ Continue shopping link
✅ Money-back guarantee notice

---

## 🔐 Authentication

### Login Required For:
- Adding to cart
- Viewing cart
- Checking out

### Unauthenticated Users:
- Can browse products
- Can view product details
- See "Login to Buy" message
- Redirected to login for add-to-cart

---

## 💾 Sample Data Setup

### Using Django Shell
```bash
python manage.py shell
```

```python
from shop.models import Category, Product

# Create categories
cat_tshirts = Category.objects.create(
    name="T-Shirts",
    slug="tshirts",
    description="High-quality PyData Kampala t-shirts"
)

cat_hoodies = Category.objects.create(
    name="Hoodies",
    slug="hoodies",
    description="Comfortable hoodies for PyData enthusiasts"
)

# Create products
Product.objects.create(
    name="PyData Kampala Classic T-Shirt",
    slug="pydata-classic-tshirt",
    category=cat_tshirts,
    description="Premium cotton t-shirt with PyData Kampala logo. Available in multiple colors.",
    short_description="Classic PyData Kampala t-shirt",
    price=15.99,
    old_price=19.99,
    available_sizes=["S", "M", "L", "XL", "2XL"],
    stock_quantity=100,
    is_featured=True,
    is_active=True
)
```

---

## 🎨 Styling

### Color Scheme
- **Primary Orange**: `#f97316` (from-orange-500 to-orange-600)
- **Secondary Slate**: `#475569` (text-slate-700)
- **Accent Yellow**: `#fbbf24` (for ratings)
- **Success Green**: `#22c55e` (in-stock)
- **Error Red**: `#ef4444` (out-of-stock)

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

---

## 📝 Template Files

```
templates/
├── base.html                    (Updated navbar)
├── shop/
│   ├── shop.html               (Product listing with filters)
│   ├── product_detail.html     (Product detail page)
│   ├── cart.html               (Shopping cart)
│   └── featured_products.html  (Featured products)
```

---

## 📦 File Structure

```
shop/
├── __init__.py
├── apps.py
├── models.py                   (Product, Category, Cart, CartItem)
├── views.py                    (All view functions)
├── urls.py                     (URL routing)
├── admin.py                    (Admin configuration)
├── forms.py                    (Cart and add-to-cart forms)
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py        (Auto-generated)
└── tests.py                    (Test cases)
```

---

## 🔄 Next Steps / TODO

1. **Checkout System**
   - Payment gateway integration (Stripe/PayPal)
   - Order confirmation emails
   - Invoice generation

2. **User Accounts**
   - Order history
   - Wishlist
   - Address management
   - User reviews and ratings

3. **Inventory Management**
   - Low stock alerts
   - Automated restocking
   - SKU management

4. **Analytics**
   - Product view tracking
   - Sales reports
   - Popular items dashboard

5. **SEO Optimization**
   - Meta tags
   - Sitemap
   - Structured data

6. **Performance**
   - Product image optimization
   - Caching strategies
   - Database indexing

---

## 🐛 Troubleshooting

### Images Not Showing
- Check `MEDIA_URL` and `MEDIA_ROOT` in settings.py
- Verify image paths in product admin
- Ensure media folder exists: `media/products/`

### Cart Not Working
- Ensure user is authenticated
- Check CSRF token in forms
- Verify JavaScript is enabled
- Check browser console for errors

### Migrations Issues
```bash
# Reset migrations (careful with production!)
python manage.py migrate shop zero
python manage.py migrate shop
```

---

## 📚 Dependencies

- Django 6.0.3+
- Pillow (for image handling)
- All existing project dependencies

---

## 📄 License

Part of PyData Kampala project. See main LICENSE file.

---

## 🤝 Contributing

See CONTRIBUTING.md for contribution guidelines.

---

## 📞 Support

For issues or questions, please open an issue in the project repository.
