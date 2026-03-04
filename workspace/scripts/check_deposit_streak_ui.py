#!/usr/bin/env python3
"""
Manual QA: Check Deposit Streak bonuses on PROD UI after Python script deposits.
Uses Playwright to login, navigate to bonuses page, and take screenshots.
"""

import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

async def check_bonuses_ui():
    """
    Login to Minebit PROD, navigate to bonuses page, take screenshots.
    """
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='Europe/Vienna'
        )

        # Test user credentials
        email = "demo1772643519424@nextcode.tech"
        password = "Qweasd123!"

        page = await context.new_page()

        # Navigate to login page
        await page.goto("https://minebit-casino.prod.sofon.one", wait_until="networkidle")
        await page.screenshot(path=f"/tmp/minebit_home_{datetime.now().strftime('%H%M%S')}.png")

        print("📸 Screenshot: Homepage saved")

        # Find and click login button
        try:
            # Try multiple selectors for login button
            login_button = await page.wait_for_selector(
                "button:has-text('Log in'), button:has-text('Login'), [data-testid*='login'], a[href*='login']",
                timeout=5000
            )
            await login_button.click()
            print("✅ Login button clicked")
        except Exception as e:
            print(f"⚠️ Could not find login button: {e}")
            print("🔍 Page content (first 500 chars):")
            print(await page.content()[:500])
            await browser.close()
            return

        # Wait for login form
        await page.wait_for_load_state("networkidle")

        # Fill login form
        try:
            email_input = await page.wait_for_selector("input[type='email'], input[name*='email'], input[placeholder*='email']", timeout=5000)
            await email_input.fill(email)
            print(f"✅ Email filled: {email}")

            password_input = await page.wait_for_selector("input[type='password'], input[name*='password'], input[placeholder*='password']", timeout=5000)
            await password_input.fill(password)
            print("✅ Password filled")

            # Submit form
            submit_button = await page.wait_for_selector("button[type='submit'], button:has-text('Log in'), button:has-text('Login')", timeout=5000)
            await submit_button.click()
            print("✅ Login form submitted")

        except Exception as e:
            print(f"❌ Could not fill login form: {e}")
            await page.screenshot(path=f"/tmp/login_form_error_{datetime.now().strftime('%H%M%S')}.png")
            await browser.close()
            return

        # Wait for login to complete
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(2)

        # Take screenshot after login
        await page.screenshot(path=f"/tmp/minebit_logged_in_{datetime.now().strftime('%H%M%S')}.png", full_page=True)
        print("📸 Screenshot: Logged in page saved (full page)")

        # Navigate to bonuses page
        try:
            # Try to find bonuses link/button
            bonuses_link = await page.wait_for_selector(
                "a:has-text('Bonus'), a:has-text('Bonuses'), [data-testid*='bonus'], nav a[href*='bonus']",
                timeout=10000
            )
            await bonuses_link.click()
            print("✅ Navigated to bonuses page")
        except Exception as e:
            print(f"⚠️ Could not find bonuses link: {e}")
            print("🔍 Trying direct URL...")
            await page.goto("https://minebit-casino.prod.sofon.one/bonuses", wait_until="networkidle")

        # Wait for bonuses to load
        await asyncio.sleep(2)

        # Take screenshot of bonuses page
        await page.screenshot(path=f"/tmp/minebit_bonuses_{datetime.now().strftime('%H%M%S')}.png", full_page=True)
        print("📸 Screenshot: Bonuses page saved (full page)")

        # Check for bonus cards
        bonus_cards = await page.locator("[data-testid*='bonus'], .bonus-card, [class*='bonus']").all()
        print(f"\n🎁 Found {len(bonus_cards)} bonus elements on page")

        # Try to find Deposit Streak bonus
        try:
            deposit_streak = await page.wait_for_selector(":has-text('Deposit Streak'), :has-text('deposit streak'), :has-text('streak')", timeout=5000)
            if deposit_streak:
                print("✅ Deposit Streak bonus found on page!")
                # Screenshot the specific element
                await deposit_streak.screenshot(path=f"/tmp/deposit_streak_bonus_{datetime.now().strftime('%H%M%S')}.png")
                print("📸 Screenshot: Deposit Streak bonus element saved")
        except:
            print("❌ Deposit Streak bonus NOT found on page")

        # Check for any active bonuses
        print("\n🔍 Checking for active bonuses...")
        try:
            active_bonuses = await page.locator(":has-text('Claim'), :has-text('Active'), :has-text('Available')").all()
            print(f"   Found {len(active_bonuses)} potentially active bonuses")
        except:
            print("   No active bonuses found")

        # Keep browser open for manual inspection
        print("\n⏸️ Browser stays open for manual inspection. Press Ctrl+C to close.")
        try:
            await asyncio.sleep(60)  # Keep open for 60 seconds
        except KeyboardInterrupt:
            print("\n👋 Closing browser...")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_bonuses_ui())
