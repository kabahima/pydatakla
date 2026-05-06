#!/bin/bash
# PyData Kampala Shop Setup Script
# This script automates the setup process for the e-commerce shop

echo "======================================"
echo "🛍️  PyData Kampala Shop Setup"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo -e "${RED}✗ Error: manage.py not found. Please run this script from the project root.${NC}"
    exit 1
fi

# Step 1: Create migrations
echo -e "${BLUE}Step 1: Creating database migrations...${NC}"
python manage.py makemigrations shop
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Migrations created successfully${NC}"
else
    echo -e "${RED}✗ Failed to create migrations${NC}"
    exit 1
fi
echo ""

# Step 2: Apply migrations
echo -e "${BLUE}Step 2: Applying migrations to database...${NC}"
python manage.py migrate
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Migrations applied successfully${NC}"
else
    echo -e "${RED}✗ Failed to apply migrations${NC}"
    exit 1
fi
echo ""

# Step 3: Collect static files (optional, for production)
read -p "Collect static files for production? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Step 3: Collecting static files...${NC}"
    python manage.py collectstatic --noinput
    echo -e "${GREEN}✓ Static files collected${NC}"
    echo ""
fi

# Step 4: Run tests
read -p "Run tests to verify installation? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Step 4: Running tests...${NC}"
    python manage.py test shop
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ All tests passed${NC}"
    else
        echo -e "${RED}✗ Some tests failed${NC}"
    fi
    echo ""
fi

# Step 5: Summary
echo "======================================"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Create a superuser: python manage.py createsuperuser"
echo "2. Start development server: python manage.py runserver"
echo "3. Go to http://localhost:8000/admin/"
echo "4. Add products and categories"
echo ""
echo "Access the shop at: http://localhost:8000/shop/"
echo ""
echo "For more information, see:"
echo "  - SHOP_COMPLETE_SUMMARY.md"
echo "  - SHOP_IMPLEMENTATION.md"
echo "  - SHOP_QUICK_REFERENCE.md"
echo ""
