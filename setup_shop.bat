@echo off
REM PyData Kampala Shop Setup Script (Windows)
REM This script automates the setup process for the e-commerce shop

cls
echo ======================================
echo.  PyData Kampala Shop Setup
echo ======================================
echo.

REM Check if we're in the right directory
if not exist "manage.py" (
    echo Error: manage.py not found. Please run this script from the project root.
    pause
    exit /b 1
)

REM Step 1: Create migrations
echo [Step 1] Creating database migrations...
python manage.py makemigrations shop
if errorlevel 1 (
    echo Error: Failed to create migrations
    pause
    exit /b 1
)
echo Migrations created successfully.
echo.

REM Step 2: Apply migrations
echo [Step 2] Applying migrations to database...
python manage.py migrate
if errorlevel 1 (
    echo Error: Failed to apply migrations
    pause
    exit /b 1
)
echo Migrations applied successfully.
echo.

REM Step 3: Run tests
set /p run_tests="Run tests to verify installation? (y/n): "
if /i "%run_tests%"=="y" (
    echo [Step 3] Running tests...
    python manage.py test shop
    echo.
)

REM Step 4: Summary
cls
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo Next steps:
echo 1. Create a superuser: python manage.py createsuperuser
echo 2. Start development server: python manage.py runserver
echo 3. Go to http://localhost:8000/admin/
echo 4. Add products and categories
echo.
echo Access the shop at: http://localhost:8000/shop/
echo.
echo For more information, see:
echo   - SHOP_COMPLETE_SUMMARY.md
echo   - SHOP_IMPLEMENTATION.md
echo   - SHOP_QUICK_REFERENCE.md
echo.
pause
