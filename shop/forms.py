from django import forms
from .models import CartItem, Product, Category, Order


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(
        attrs={'class': 'w-16 text-center border border-slate-300 rounded py-1'}
    ))
    size = forms.ChoiceField(required=False, widget=forms.Select(
        attrs={'class': 'px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500'}
    ))

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        if product and product.available_sizes:
            self.fields['size'].choices = [(s, s) for s in product.available_sizes]
            self.fields['size'].required = True


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(
                attrs={'min': '1', 'class': 'w-16 text-center border border-slate-300 rounded py-1'}
            )
        }


class ProductForm(forms.ModelForm):
    """Form for creating and editing products in the portal"""
    available_sizes = forms.MultipleChoiceField(
        choices=[
            ('XS', 'Extra Small'),
            ('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
            ('XL', 'Extra Large'),
            ('2XL', '2XL'),
            ('3XL', '3XL'),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'space-y-2'}
        ),
        help_text="Select all available sizes for this product"
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'short_description', 'price', 'old_price', 
                  'image', 'available_sizes', 'stock_quantity', 'is_featured', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg'}),
            'category': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg', 'rows': 5}),
            'short_description': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg', 'step': '0.01'}),
            'old_price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'rounded'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.available_sizes:
            self.fields['available_sizes'].initial = self.instance.available_sizes

    def clean_available_sizes(self):
        """Convert selected sizes back to list format"""
        sizes = self.cleaned_data.get('available_sizes', [])
        return list(sizes) if sizes else []


class CategoryForm(forms.ModelForm):
    """Form for creating and editing product categories in the portal"""
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg', 'placeholder': 'e.g., T-Shirts, Mugs, Hats'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg', 'rows': 4, 'placeholder': 'Brief description of this category'}),
            'image': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded', 'rows': 3}),
        }
