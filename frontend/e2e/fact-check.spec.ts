import { expect, test } from '@playwright/test'

test('fact check works without login', async ({ page }) => {
	await page.goto('/fact-check')

	await page.fill('[data-testid="claim-input"]', 'The earth is round')
	await page.click('[data-testid="verify-button"]')

	await expect(page.locator('[data-testid="verdict-card"]')).toBeVisible({ timeout: 30000 })

	const verdict = await page.locator('[data-testid="verdict-badge"]').textContent()
	expect(['TRUE', 'FALSE', 'UNVERIFIED']).toContain((verdict ?? '').trim())
})
