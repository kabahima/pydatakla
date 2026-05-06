# 🛍️ Shop System - Quick Reference Guide

## 📋 Common Tasks

### 1. Add a New Product

**Via Admin Panel:**
1. Go to http://localhost:8000/admin/
2. Click "Products" → "Add Product"
3. Fill in:
   - Name: "PyData Kampala Hoodie"
   - Slug: "pydata-hoodie" (auto-filled)
   - Category: Select "Hoodies"
   - Description: Detailed product description
   - Short Description: Brief 1-2 line description
   - Price: 29.99
   - Old Price: 39.99 (optional, for showing discount)
   - Image: Upload main product image
   - Gallery Images: `["url1", "url2"]` (JSON format)
   - Available Sizes: `["S", "M", "L", "XL", "2XL"]` (JSON format)
   - Stock Quantity: 100
   - Is Featured: ✓ (for homepage)
   - Is Active: ✓ (to show on site)
4. Save

---

### 2. Create a Category

**Via Admin:**
1. Go to http://localhost:8000/admin/
2. Click "Categories" → "Add Category"
3. Fill in:
   - Name: "Hoodies"
   - Description: "Comfortable hoodies for PyData enthusiasts"
   - Image: (optional)
4. Save

---

### 3. Update Product Inventory

**Via Admin:**
1. Go to Products
2. Click product to edit
3. Change "Stock Quantity"
4. Save

---

### 4. Mark Product as Featured

**Via Admin:**
1. Go to Products
2. Click product to edit
3. Check "Is Featured"
4. Save
→ Will appear in `/shop/featured/` page

---

### 5. Run Tests

```bash
python manage.py test shop
```

**Run specific test:**
```bash
python manage.py test shop.tests.ProductModelTest
```

---

## 🔗 Important URLs

| URL | Purpose |
|-----|---------|
| `/shop/` | Main shop page |
| `/shop/product/pydata-tshirt/` | Product detail (slug format) |
| `/shop/cart/` | Shopping cart |
| `/admin/shop/product/` | Manage products |
| `/admin/shop/category/` | Manage categories |

---

## 🎨 Template Layout

### shop.html Structure
```
Page Header
├── Breadcrumb
├── Title & Description
└── Main Content
    ├── Sidebar (Filters)
    │   ├── Categories
    │   ├── Price Range
    │   └── Size
    └── Grid (Products)
        ├── Sort Options
        ├── Product Cards
        │   ├── Image
        │   ├── Name & Description
        │   ├── Price
        │   └── Buttons
        └── Pagination
```

### product_detail.html Structure
```
Breadcrumb Navigation
├── Main Content
│   ├── Left Column (Image Gallery)
│   │   ├── Main Image
│   │   └── Thumbnails
│   └── Right Column (Details)
│       ├── Title & Category
│       ├── Rating
│       ├── Price
│       ├── Description
│       ├── Size Selector
│       ├── Quantity Selector
│       ├── Add to Cart Button
│       └── Share Buttons
└── Related Products Section
```

### cart.html Structure
```
Cart Header
├── If Has Items
│   ├── Left Column (Items List)
│   │   └── Cart Items
│   │       ├── Image
│   │       ├── Details
│   │       ├── Quantity Controls
│   │       └── Remove Button
│   └── Right Column (Summary)
│       ├── Subtotal
│       ├── Shipping
│       ├── Tax
│       ├── Total
│       └── Checkout Button
└── If Empty
    └── Empty Message with Shop Link
```

---

## 🔍 Search & Filter Examples

### Search for T-Shirts by Size M
```
/shop/?search=pydata&size=M
```

### Filter by Price Range
```
/shop/?category=tshirts&min_price=10&max_price=30
```

### Sort by Price (Low-High)
```
/shop/?sort=price
```

### Combination Filter
```
/shop/?category=hoodies&size=L&sort=-price&search=classic
```

---

## 📊 Database Queries Examples

### Get all products in a category
```python
from shop.models import Product, Category

category = Category.objects.get(slug='tshirts')
products = Product.objects.filter(category=category, is_active=True)
```

### Get featured products
```python
featured = Product.objects.filter(is_featured=True, is_active=True)[:8]
```

### Get user's cart
```python
from shop.models import Cart

cart = Cart.objects.get(user=request.user)
total = cart.get_total()
```

### Add item to cart
```python
from shop.models import Cart, CartItem

cart = Cart.objects.get_or_create(user=user)[0]
CartItem.objects.create(
    cart=cart,
    product=product,
    quantity=2,
    size='M'
)
```

### Calculate discount
```python
product.discount_percentage  # Returns percentage (e.g., 20)
```

---

## 🎯 Template Tags & Filters Used

```django
{# Display product price #}
<span>${{ product.price }}</span>

{# Display discounted price #}
{% if product.old_price %}
    <span>${{ product.old_price }} (original)</span>
{% endif %}

{# Reverse URL with parameters #}
<a href="{% url 'shop:shop' %}?category=tshirts">T-Shirts</a>

{# Format number #}
{{ product.price|floatformat:2 }}

{# Pagination #}
{% if page_obj.has_next %}
    <a href="?page={{ page_obj.next_page_number }}">Next</a>
{% endif %}

{# Truncate text #}
{{ product.name|truncatewords:5 }}
```

---

## 🛡️ Security Considerations

✅ **CSRF Protection**
```django
{% csrf_token %}  {# Include in all forms #}
```

✅ **Authentication**
```django
{% if user.is_authenticated %}
    {# Show checkout #}
{% else %}
    {# Show login prompt #}
{% endif %}
```

✅ **SQL Injection Prevention**
```python
# ❌ DON'T
products = Product.objects.raw(f"SELECT * FROM shop_product WHERE name = '{name}'")

# ✅ DO
products = Product.objects.filter(name=name)
```

---

## 📱 Mobile Responsive Breakpoints

```tailwind
Base (mobile):           < 640px
sm: (small tablets)      ≥ 640px
md: (tablets)            ≥ 768px
lg: (laptops)            ≥ 1024px
xl: (desktops)           ≥ 1280px
2xl: (large screens)     ≥ 1536px
```

Example:
```django
<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
    {# 1 col mobile, 2 sm, 3 md, 4 lg #}
</div>
```

---

## 🐛 Common Issues & Solutions

### Issue: Images not showing
**Solution:**
```bash
# Check media folder exists
ls media/products/

# Add to settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Issue: Cart says login required
**Solution:**
- Ensure user is authenticated
- Check `@login_required` decorator on view
- Clear browser cookies and login again

### Issue: Sort not working
**Solution:**
```python
# Valid sort options:
valid_sorts = ['name', '-name', 'price', '-price', '-created_at', 'stock_quantity']

# Use one of these in URL:
/shop/?sort=price        # Ascending
/shop/?sort=-price       # Descending (-prefix)
```

### Issue: Pagination links broken
**Solution:**
- Ensure all filter parameters are preserved in links:
```django
{% if page_obj.has_next %}
    <a href="?page={{ page_obj.next_page_number }}&search={{ search_query }}&sort={{ sort_by }}">
        Next
    </a>
{% endif %}
```

---

## 📈 Performance Tips

### 1. Use Select/Prefetch Related
```python
# Good ✅
products = Product.objects.select_related('category')

# Bad ❌
products = Product.objects.all()
for p in products:
    print(p.category)  # Extra query per product!
```

### 2. Add Database Indexes
```python
class Meta:
    indexes = [
        models.Index(fields=['slug']),
        models.Index(fields=['category']),
        models.Index(fields=['is_featured']),
    ]
```

### 3. Cache Queries
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def featured_products(request):
    return render(...)
```

---

## 🚀 Deployment Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Set `ALLOWED_HOSTS` correctly
- [ ] Configure static files collection
- [ ] Set up media files storage (Cloudinary, S3)
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up SSL/HTTPS
- [ ] Run `python manage.py collectstatic`
- [ ] Run migrations on production
- [ ] Create superuser on production
- [ ] Set up logging

---

## 📚 Related Documentation

- [Django Models](https://docs.djangoproject.com/en/6.0/topics/db/models/)
- [Django Admin](https://docs.djangoproject.com/en/6.0/ref/contrib/admin/)
- [Django Views](https://docs.djangoproject.com/en/6.0/topics/http/views/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Django ORM Queries](https://docs.djangoproject.com/en/6.0/topics/db/queries/)

---

## 💡 Pro Tips

1. **Always use slugs in URLs** - Better for SEO and readability
2. **Test with different user roles** - Anonymous, authenticated, admin
3. **Use Django admin actions** - Bulk update products
4. **Cache expensive queries** - Use Django's cache framework
5. **Monitor database queries** - Use Django Debug Toolbar in development
6. **Write tests as you develop** - Catch bugs early
7. **Use form validation** - Never trust user input
8. **Keep templates DRY** - Use includes and extends
9. **Optimize images** - Use compression tools
10. **Document code** - Future you will thank present you

---

**Last Updated:** May 6, 2026
**Version:** 1.0 (Initial Release)
