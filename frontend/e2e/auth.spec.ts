import { expect, test } from '@playwright/test'

async function registerAndLogin(page: import('@playwright/test').Page) {
	const email = `test-${Date.now()}@test.com`
	const password = 'password123'

	await page.goto('/register')
	await page.fill('[name="display_name"]', 'Test User')
	await page.fill('[name="email"]', email)
	await page.fill('[name="password"]', password)
	await page.click('button[type="submit"]')
	await expect(page).toHaveURL(/\/login$/)

	await page.fill('[name="email"]', email)
	await page.fill('[name="password"]', password)
	await page.click('button[type="submit"]')
	await expect(page).toHaveURL(/\/chat(\/.*)?$/)
}

test('full auth flow: register -> login -> dashboard', async ({ page }) => {
	await registerAndLogin(page)
})

test('redirects to login when not authenticated', async ({ page }) => {
	await page.goto('/chat')
	await expect(page).toHaveURL(/\/login$/)
})

test('logout clears session and redirects to login', async ({ page }) => {
	await registerAndLogin(page)

	await page.click('[data-testid="logout-button"]')
	await expect(page).toHaveURL(/\/login$/)

	await page.goto('/chat')
	await expect(page).toHaveURL(/\/login$/)
})
