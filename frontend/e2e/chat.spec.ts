import { expect, test } from '@playwright/test'

async function login(page: import('@playwright/test').Page) {
  const email = `chat-${Date.now()}@test.com`
  const password = 'password123'

  await page.goto('/register')
  await page.fill('[name="display_name"]', 'Chat User')
  await page.fill('[name="email"]', email)
  await page.fill('[name="password"]', password)
  await page.click('button[type="submit"]')
  await expect(page).toHaveURL(/\/login$/)

  await page.fill('[name="email"]', email)
  await page.fill('[name="password"]', password)
  await page.click('button[type="submit"]')
  await expect(page).toHaveURL(/\/chat(\/.*)?$/)
}

test('sends message and receives AI response', async ({ page }) => {
  await login(page)

  await page.goto('/chat')
  await expect(page).toHaveURL(/\/chat(\/.*)?$/)

  await page.fill('[data-testid="message-input"]', 'What is the latest tech news?')
  await page.press('[data-testid="message-input"]', 'Enter')

  await expect(page.locator('[data-testid="assistant-message"]').first()).toBeVisible({ timeout: 30000 })
})

test('suggested questions click fills input', async ({ page }) => {
  await login(page)

  await page.goto('/chat')
  await expect(page).toHaveURL(/\/chat(\/.*)?$/)

  await page.locator('[data-testid="suggested-question"]').first().click()
  await expect(page.locator('[data-testid="message-input"]')).not.toBeEmpty()
})
