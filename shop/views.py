from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import OrderForm


def shop(request):
    """Main shop listing page with filters and sorting"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    else:
        category = None
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Filter by size
    size = request.GET.get('size')
    if size:
        products = products.filter(available_sizes__contains=[size])
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['name', '-name', 'price', '-price', '-created_at', 'stock_quantity']
    if sort_by in valid_sorts:
        products = products.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'categories': categories,
        'selected_category': category,
        'search_query': search_query,
        'sort_by': sort_by,
        'min_price': min_price,
        'max_price': max_price,
        'page_obj': page_obj,
    }
    
    return render(request, 'shop/shop.html', context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    
    return render(request, 'shop/product_detail.html', context)


@login_required
def get_or_create_cart(user):
    """Helper function to get or create user's cart"""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@require_POST
@login_required
def add_to_cart(request):
    """Add product to cart (AJAX endpoint)"""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size', '')
    
    try:
        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart = get_or_create_cart(request.user)
        
        # Check if item already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        cart_count = cart.items.count()
        
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart!',
            'cart_count': cart_count,
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e),
        }, status=400)


@login_required
def view_cart(request):
    """View shopping cart"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()
    total = cart.get_total()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
    }
    
    return render(request, 'shop/cart.html', context)


@require_POST
@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = get_object_or_404(Cart, user=request.user)
        return JsonResponse({
            'success': True,
            'cart_total': float(cart.get_total()),
            'cart_count': cart.items.count(),
        })
    
    return redirect('shop:view_cart')


@require_POST
@login_required
def update_cart_item(request, item_id):
    """Update quantity of cart item"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = get_object_or_404(Cart, user=request.user)
        return JsonResponse({
            'success': True,
            'subtotal': float(cart_item.get_subtotal() if quantity > 0 else 0),
            'cart_total': float(cart.get_total()),
        })
    
    return redirect('shop:view_cart')


def featured_products(request):
    """Get featured products (for homepage widget)"""
    featured = Product.objects.filter(is_featured=True, is_active=True)[:8]
    context = {'featured_products': featured}
    return render(request, 'shop/featured_products.html', context)


@login_required
def checkout(request):
    """Checkout form — converts cart to Order and shows confirmation with share links"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('product').all()
    if not cart_items:
        return redirect('shop:shop')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total = 0
            order.save()

            total = 0
            for item in cart_items:
                oi = OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    size=item.size,
                )
                total += oi.get_subtotal()

            order.total = total
            order.save()

            # clear cart
            cart.items.all().delete()

            return redirect('shop:order_confirmation', order_id=order.pk)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {'full_name': f"{request.user.first_name} {request.user.last_name}".strip(), 'email': request.user.email}
        form = OrderForm(initial=initial)

    return render(request, 'shop/order_form.html', {'form': form, 'cart_items': cart_items})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    # Build whatsapp link (no plus sign, digits only expected by wa.me)
    wa_phone = ''
    if order.phone:
        digits = ''.join(ch for ch in order.phone if ch.isdigit())
        wa_phone = digits
    message_lines = [f"Order #{order.pk}", f"Name: {order.full_name}", f"Total: ${order.total}"]
    for it in order.items.all():
        message_lines.append(f"- {it.product.name} x{it.quantity} ({it.size})")
    message_lines.append(f"Shipping: {order.address}")
    message = "%0A".join([m.replace(' ', '%20') for m in message_lines])

    whatsapp_link = f"https://wa.me/{wa_phone}?text={message}" if wa_phone else ''
    mailto = f"mailto:{order.email}?subject=Order%20#{order.pk}&body={'%0A'.join([m.replace(' ', '%20') for m in message_lines])}"

    return render(request, 'shop/order_confirmation.html', {'order': order, 'whatsapp_link': whatsapp_link, 'mailto': mailto})
