# News AI — Frontend Roadmap

**Proje:** News AI — AI Ajanlı Haber Platformu  
**Stack:** Next.js 15 (App Router) · Tailwind CSS · Zustand · TanStack Query  
**Test Stack:** Jest · React Testing Library · Playwright (E2E)  
**Phase 1:** Project Setup & Layout (1 hafta)  
**Phase 2:** Auth Ekranları (1 hafta)  
**Phase 3:** Chat Sayfası — Screen 1 (1.5 hafta)  
**Phase 4:** Fact Check Engine — Screen 2 (1 hafta)  
**Phase 5:** News Feed — Screen 3 (1 hafta)  
**Phase 6:** Trending — Screen 4 (0.5 hafta)  
**Phase 7:** Category Sayfaları — Screen 5 & 6 (1 hafta)  
**Phase 8:** Polish, Testing & Deploy Hazırlığı (1 hafta)  

---

## 📋 İçindekiler

### Phase 1: Project Setup & Layout
- [Phase 1 Overview](#-phase-1-overview)
- [Week 1: Kurulum, Tema, Sidebar, API Client](#-week-1-kurulum-tema-sidebar-api-client)
- [Phase 1 Success Metrics](#-phase-1-success-metrics)

### Phase 2: Auth Ekranları
- [Phase 2 Overview](#-phase-2-overview)
- [Week 2: Login, Register, Auth State](#-week-2-login-register-auth-state)
- [Phase 2 Success Metrics](#-phase-2-success-metrics)

### Phase 3: Chat Sayfası
- [Phase 3 Overview](#-phase-3-overview)
- [Week 3: Chat UI & Mesaj Gönderme](#-week-3-chat-ui--mesaj-gönderme)
- [Week 4 (ilk yarı): Konuşma Yönetimi & Streaming](#-week-4-ilk-yarı-konuşma-yönetimi--streaming)
- [Phase 3 Success Metrics](#-phase-3-success-metrics)

### Phase 4: Fact Check Engine
- [Phase 4 Overview](#-phase-4-overview)
- [Week 4 (ikinci yarı): Fact Check UI](#-week-4-ikinci-yarı-fact-check-ui)
- [Phase 4 Success Metrics](#-phase-4-success-metrics)

### Phase 5: News Feed
- [Phase 5 Overview](#-phase-5-overview)
- [Week 5: News Feed UI & Filtreler](#-week-5-news-feed-ui--filtreler)
- [Phase 5 Success Metrics](#-phase-5-success-metrics)

### Phase 6: Trending
- [Phase 6 Overview](#-phase-6-overview)
- [Week 6 (ilk yarı): Trending UI](#-week-6-ilk-yarı-trending-ui)
- [Phase 6 Success Metrics](#-phase-6-success-metrics)

### Phase 7: Category Sayfaları
- [Phase 7 Overview](#-phase-7-overview)
- [Week 6 (ikinci yarı) & Week 7: Sports & Technology Sayfaları](#-week-6-ikinci-yarı--week-7-sports--technology-sayfaları)
- [Phase 7 Success Metrics](#-phase-7-success-metrics)

### Phase 8: Polish, Testing & Deploy Hazırlığı
- [Phase 8 Overview](#-phase-8-overview)
- [Week 8: Polish, Responsive, Deploy](#-week-8-polish-responsive-deploy)
- [Phase 8 Success Metrics](#-phase-8-success-metrics)

---

## 🎯 Phase 1 Overview

### Scope

**Dahil:**
- Next.js 15 App Router proje kurulumu
- Tailwind CSS + dark navy tema (projenin tasarım sistemi)
- Zustand store kurulumu (auth, ui)
- TanStack Query kurulumu ve API client
- Kalıcı sol sidebar (tüm sayfalarda ortak)
- Layout bileşenleri
- Route koruması (auth olmadan korumalı sayfalara erişim engeli)
- Jest + React Testing Library test altyapısı
- Playwright E2E test altyapısı

**Hariç:**
- Sayfa içerikleri (Phase 3+)
- Backend entegrasyonu (Phase 2'den itibaren)

### Definition of Done

- [x] `npm run dev` sorunsuz çalışıyor
- [x] Dark navy tema tüm bileşenlerde tutarlı
- [x] Sidebar tüm sayfalarda görünüyor
- [x] Korumalı route'a token olmadan gidilince `/login`'e yönlendiriyor
- [x] API client `NEXT_PUBLIC_API_URL`'den base URL okuyor
- [x] `npm test` → test altyapısı çalışıyor, temel component testleri geçiyor

---

## 📅 Week 1: Kurulum, Tema, Sidebar, API Client

**Hedef:** Proje iskeleti, tasarım sistemi, layout, API client, test altyapısı

---

### Task 1.1: Next.js Proje Kurulumu

**Tahmini Süre:** 1 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `frontend/` klasörüne git, Next.js projesi oluştur:
  ```bash
  cd frontend
  npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
  ```
- [x] Gerekli paketleri yükle:
  ```bash
  npm install @tanstack/react-query @tanstack/react-query-devtools
  npm install zustand
  npm install axios
  npm install lucide-react
  npm install clsx tailwind-merge
  npm install sonner
  npm install react-markdown
  ```
- [x] `frontend/` klasör yapısını oluştur:
  ```
  frontend/
  ├── src/
  │   ├── app/
  │   │   ├── (auth)/
  │   │   │   ├── login/
  │   │   │   │   └── page.tsx
  │   │   │   └── register/
  │   │   │       └── page.tsx
  │   │   ├── (dashboard)/
  │   │   │   ├── layout.tsx          # sidebar buraya
  │   │   │   ├── chat/
  │   │   │   │   ├── page.tsx
  │   │   │   │   └── [id]/
  │   │   │   │       └── page.tsx
  │   │   │   ├── fact-check/
  │   │   │   │   └── page.tsx
  │   │   │   ├── feed/
  │   │   │   │   └── page.tsx
  │   │   │   ├── trending/
  │   │   │   │   └── page.tsx
  │   │   │   ├── category/
  │   │   │   │   └── [slug]/
  │   │   │   │       └── page.tsx
  │   │   │   ├── settings/
  │   │   │   │   └── page.tsx
  │   │   │   └── saved/
  │   │   │       └── page.tsx
  │   │   ├── layout.tsx              # root layout
  │   │   ├── page.tsx                # / → /chat yönlendirme
  │   │   └── globals.css
  │   ├── components/
  │   │   ├── layout/
  │   │   │   ├── Sidebar.tsx
  │   │   │   ├── TopBar.tsx
  │   │   │   └── AuthGuard.tsx
  │   │   ├── chat/
  │   │   ├── news/
  │   │   ├── fact-check/
  │   │   └── ui/
  │   │       ├── Button.tsx
  │   │       ├── Input.tsx
  │   │       ├── Badge.tsx
  │   │       ├── Card.tsx
  │   │       ├── Spinner.tsx
  │   │       └── Skeleton.tsx
  │   ├── lib/
  │   │   ├── api.ts
  │   │   ├── queryClient.ts
  │   │   └── utils.ts
  │   ├── stores/
  │   │   ├── authStore.ts
  │   │   └── uiStore.ts
  │   ├── hooks/
  │   │   ├── useAuth.ts
  │   │   ├── useConversations.ts
  │   │   ├── useMessages.ts
  │   │   ├── useNews.ts
  │   │   ├── useFactCheck.ts
  │   │   └── useTrending.ts
  │   └── types/
  │       ├── auth.ts
  │       ├── conversation.ts
  │       ├── news.ts
  │       └── factCheck.ts
  ├── __tests__/              # Jest + RTL unit/integration testleri
  │   ├── components/
  │   │   ├── ui/
  │   │   ├── chat/
  │   │   ├── news/
  │   │   └── fact-check/
  │   ├── hooks/
  │   └── stores/
  ├── e2e/                    # Playwright E2E testleri
  │   ├── auth.spec.ts
  │   ├── chat.spec.ts
  │   ├── fact-check.spec.ts
  │   └── news-feed.spec.ts
  ├── public/
  ├── Dockerfile
  ├── .env.example
  ├── jest.config.ts
  ├── jest.setup.ts
  ├── playwright.config.ts
  └── next.config.ts
  ```
- [x] `frontend/.env.example` oluştur:
  ```
  NEXT_PUBLIC_API_URL=http://localhost:8001
  ```

---

### Task 1.2: Tailwind Tema — Dark Navy Tasarım Sistemi

**Tahmini Süre:** 2 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `tailwind.config.ts` içinde özel renk paleti tanımla:
  ```ts
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#050a14',
          900: '#0a1628',
          800: '#0f2040',
          700: '#1a3358',
          600: '#1e3a6e',
          500: '#2a4f8f',
        },
        accent: {
          blue:  '#3b82f6',
          cyan:  '#06b6d4',
        },
        verdict: {
          false:  '#ef4444',
          unverified: '#f59e0b',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    }
  }
  ```
- [x] `globals.css` güncelle:
  ```css
  :root {
    --bg-primary: #0a1628;
    --bg-secondary: #0f2040;
    --bg-card: #1a3358;
    --border: #1e3a6e;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent: #3b82f6;
  }

  body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
  }

  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: var(--bg-secondary); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
  ```
- [x] `src/lib/utils.ts` oluştur:
  ```ts
  import { clsx, type ClassValue } from 'clsx'
  import { twMerge } from 'tailwind-merge'

  export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs))
  }
  ```

---

### Task 1.3: API Client & TanStack Query Kurulumu

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `src/lib/api.ts` oluştur:
  ```ts
  import axios from 'axios'

  export const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    withCredentials: true,
  })

  api.interceptors.request.use((config) => {
    const token = useAuthStore.getState().accessToken
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  })

  api.interceptors.response.use(
    (res) => res,
    async (error) => {
      if (error.response?.status === 401) {
        try {
          const { data } = await axios.post(
            `${process.env.NEXT_PUBLIC_API_URL}/auth/refresh`,
            {},
            { withCredentials: true }
          )
          useAuthStore.getState().setAccessToken(data.access_token)
          error.config.headers.Authorization = `Bearer ${data.access_token}`
          return axios(error.config)
        } catch {
          useAuthStore.getState().logout()
          window.location.href = '/login'
        }
      }
      return Promise.reject(error)
    }
  )
  ```
- [x] `src/lib/queryClient.ts` oluştur:
  ```ts
  import { QueryClient } from '@tanstack/react-query'

  export const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 1000 * 60 * 5,
        retry: 1,
      },
    },
  })
  ```
- [x] Root layout'a `QueryClientProvider` ve `ReactQueryDevtools` ekle

---

### Task 1.4: Zustand Store'ları

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/stores/authStore.test.ts` oluştur:
  ```ts
  import { renderHook, act } from '@testing-library/react'
  import { useAuthStore } from '@/stores/authStore'

  beforeEach(() => {
    useAuthStore.setState({ accessToken: null, user: null })
  })

  test('initial state has no accessToken', () => {
    const { result } = renderHook(() => useAuthStore())
    expect(result.current.accessToken).toBeNull()
  })

  test('setAccessToken updates state', () => {
    const { result } = renderHook(() => useAuthStore())
    act(() => result.current.setAccessToken('test-token'))
    expect(result.current.accessToken).toBe('test-token')
  })

  test('logout clears accessToken and user', () => {
    const { result } = renderHook(() => useAuthStore())
    act(() => {
      result.current.setAccessToken('token')
      result.current.setUser({ id: '1', email: 'a@b.com', display_name: 'Test', role: 'user', email_verified_at: null, created_at: '' })
      result.current.logout()
    })
    expect(result.current.accessToken).toBeNull()
    expect(result.current.user).toBeNull()
  })

  test('isAuthenticated returns true when token exists', () => {
    const { result } = renderHook(() => useAuthStore())
    act(() => result.current.setAccessToken('some-token'))
    expect(result.current.isAuthenticated()).toBe(true)
  })

  test('isAuthenticated returns false when no token', () => {
    const { result } = renderHook(() => useAuthStore())
    expect(result.current.isAuthenticated()).toBe(false)
  })
  ```
- [x] `src/stores/authStore.ts` oluştur:
  ```ts
  import { create } from 'zustand'
  import { persist } from 'zustand/middleware'

  interface User {
    id: string
    email: string
    display_name: string
    role: 'user' | 'admin'
    email_verified_at: string | null
    created_at: string
  }

  interface AuthStore {
    accessToken: string | null
    user: User | null
    setAccessToken: (token: string) => void
    setUser: (user: User) => void
    logout: () => void
    isAuthenticated: () => boolean
  }

  export const useAuthStore = create<AuthStore>()(
    persist(
      (set, get) => ({
        accessToken: null,
        user: null,
        setAccessToken: (token) => set({ accessToken: token }),
        setUser: (user) => set({ user }),
        logout: () => set({ accessToken: null, user: null }),
        isAuthenticated: () => !!get().accessToken,
      }),
      { name: 'newsai-auth', partialize: (s) => ({ user: s.user }) }
    )
  )
  ```
- [x] `src/stores/uiStore.ts` oluştur:
  ```ts
  interface UIStore {
    sidebarCollapsed: boolean
    toggleSidebar: () => void
    activeConversationId: string | null
    setActiveConversation: (id: string | null) => void
  }
  ```
- [x] `src/types/` altındaki type dosyalarını oluştur (backend response şemalarıyla birebir eşleşsin)

---

### Task 1.5: Sidebar Bileşeni

**Tahmini Süre:** 3 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/layout/Sidebar.test.tsx` oluştur:
  ```tsx
  import { render, screen } from '@testing-library/react'
  import { Sidebar } from '@/components/layout/Sidebar'

  jest.mock('next/navigation', () => ({ usePathname: () => '/chat', useRouter: () => ({}) }))

  test('renders News AI logo', () => {
    render(<Sidebar />)
    expect(screen.getByText(/News AI/i)).toBeInTheDocument()
  })

  test('renders all navigation links', () => {
    render(<Sidebar />)
    expect(screen.getByText(/Chat/i)).toBeInTheDocument()
    expect(screen.getByText(/Fact Check/i)).toBeInTheDocument()
    expect(screen.getByText(/News Feed/i)).toBeInTheDocument()
    expect(screen.getByText(/Trending/i)).toBeInTheDocument()
  })

  test('renders category links', () => {
    render(<Sidebar />)
    expect(screen.getByText(/World/i)).toBeInTheDocument()
    expect(screen.getByText(/Technology/i)).toBeInTheDocument()
    expect(screen.getByText(/Sports/i)).toBeInTheDocument()
  })

  test('active link has highlight class', () => {
    render(<Sidebar />)
    const chatLink = screen.getByText(/Chat/i).closest('a')
    expect(chatLink).toHaveClass('bg-navy-600')
  })
  ```
- [x] `src/components/layout/Sidebar.tsx` oluştur:
  - [x] Sol kenar, sabit (sticky), tam yükseklik
  - [x] Üst: "News AI" logo + ikon
  - [x] Ana navigasyon linkleri:
    - Chat (`/chat`) — ikon: MessageSquare
    - Fact Check (`/fact-check`) — ikon: ShieldCheck
    - News Feed (`/feed`) — ikon: Newspaper
    - Trending (`/trending`) — ikon: TrendingUp
  - [x] Alt kısımda "Categories" başlığı:
    - World (`/category/world`)
    - Economy (`/category/economy`)
    - Sports (`/category/sports`)
    - Technology (`/category/technology`)
  - [x] En altta: Settings ikonu + kullanıcı adı + logout butonu
  - [x] Aktif link highlight (navy-600 arka plan, accent-blue sol border)
  - [x] Collapse/expand butonu (uiStore'dan)
  - [x] Mobilde overlay olarak açılır
- [x] `src/components/layout/TopBar.tsx` oluştur:
  - [x] Arama ikonu (şimdilik dekoratif)
  - [x] Sağda bildirim ikonu
  - [x] Mevcut sayfanın başlığı (dinamik)

---

### Task 1.6: Dashboard Layout & AuthGuard

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/layout/AuthGuard.test.tsx` oluştur:
  ```tsx
  import { render, screen } from '@testing-library/react'
  import { AuthGuard } from '@/components/layout/AuthGuard'

  const mockReplace = jest.fn()
  jest.mock('next/navigation', () => ({
    useRouter: () => ({ replace: mockReplace }),
  }))

  test('redirects to login when not authenticated', () => {
    jest.mock('@/stores/authStore', () => ({
      useAuthStore: () => ({ isAuthenticated: () => false }),
    }))
    render(<AuthGuard><div>Protected</div></AuthGuard>)
    expect(mockReplace).toHaveBeenCalledWith('/login')
  })

  test('renders children when authenticated', () => {
    jest.mock('@/stores/authStore', () => ({
      useAuthStore: () => ({ isAuthenticated: () => true }),
    }))
    render(<AuthGuard><div>Protected Content</div></AuthGuard>)
    expect(screen.getByText('Protected Content')).toBeInTheDocument()
  })

  test('shows spinner while checking auth', () => {
    render(<AuthGuard><div>Content</div></AuthGuard>)
    // Başlangıç yükleme durumunda spinner görünmeli
    expect(screen.queryByRole('status')).toBeDefined()
  })
  ```
- [x] `src/app/(dashboard)/layout.tsx` oluştur:
  ```tsx
  export default function DashboardLayout({ children }) {
    return (
      <AuthGuard>
        <div className="flex h-screen bg-navy-900">
          <Sidebar />
          <main className="flex-1 overflow-auto">
            <TopBar />
            {children}
          </main>
        </div>
      </AuthGuard>
    )
  }
  ```
- [x] `src/components/layout/AuthGuard.tsx` oluştur:
  - [x] `useAuthStore`'dan `isAuthenticated` kontrol et
  - [x] Token yoksa `router.replace('/login')`
  - [x] Kontrol sırasında Spinner göster
- [x] `src/app/page.tsx` → `/chat`'e redirect
- [x] Root layout'a `QueryClientProvider` ve `<Toaster>` ekle

---

### Task 1.7: UI Primitive Bileşenleri

**Tahmini Süre:** 2 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/ui/Button.test.tsx` oluştur:
  ```tsx
  import { render, screen, fireEvent } from '@testing-library/react'
  import { Button } from '@/components/ui/Button'

  test('renders with label', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  test('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click</Button>)
    fireEvent.click(screen.getByText('Click'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  test('disabled button does not call onClick', () => {
    const handleClick = jest.fn()
    render(<Button disabled onClick={handleClick}>Disabled</Button>)
    fireEvent.click(screen.getByText('Disabled'))
    expect(handleClick).not.toHaveBeenCalled()
  })

  test('shows spinner when loading', () => {
    render(<Button loading>Loading</Button>)
    expect(screen.getByRole('status')).toBeInTheDocument()
  })

  test('danger variant has red styling', () => {
    render(<Button variant="danger">Delete</Button>)
    const btn = screen.getByText('Delete').closest('button')
    expect(btn?.className).toMatch(/red|danger/)
  })
  ```
- [x] `src/components/ui/Button.tsx`:
  - [x] Variant'lar: `primary`, `secondary`, `ghost`, `danger`
  - [x] Size'lar: `sm`, `md`, `lg`
  - [x] Loading state (Spinner ile), `aria-busy` attribute
  - [x] Disabled state
- [x] `src/components/ui/Input.tsx`:
  - [x] Dark navy background
  - [x] Focus ring (accent-blue)
  - [x] Error state (kırmızı border + hata mesajı), `aria-invalid`
  - [x] Label desteği
- [x] `src/components/ui/Badge.tsx`:
  - [x] Variant'lar: `default`, `success`, `danger`, `warning`, `info`
  - [x] Verdict badge'i için özel renkler (yeşil/kırmızı/sarı)
- [x] `src/components/ui/Card.tsx`: navy-700 arka plan, border, rounded-lg
- [x] `src/components/ui/Spinner.tsx`: dönen yükleme animasyonu, `role="status"`
- [x] `src/components/ui/Skeleton.tsx`: loading placeholder animasyonu
- [x] Ekstra test — `__tests__/components/ui/Primitives.test.tsx`:
  - [x] `Input` label + error + `aria-invalid`
  - [x] `Badge` variant render
  - [x] `Card` content render
  - [x] `Spinner` `role="status"`
  - [x] `Skeleton` `aria-hidden`

---

### Task 1.8: Test Altyapısı (Jest + Playwright)

**Tahmini Süre:** 2 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Jest + React Testing Library kurulumu:
  ```bash
  npm install -D jest jest-environment-jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event
  npm install -D @types/jest ts-jest
  ```
- [x] `jest.config.ts` oluştur:
  ```ts
  import type { Config } from 'jest'
  import nextJest from 'next/jest'

  const createJestConfig = nextJest({ dir: './' })

  const config: Config = {
    coverageProvider: 'v8',
    testEnvironment: 'jsdom',
    setupFilesAfterFramework: ['<rootDir>/jest.setup.ts'],
    moduleNameMapper: {
      '^@/(.*)$': '<rootDir>/src/$1',
    },
    testPathPattern: '__tests__/**/*.test.{ts,tsx}',
  }

  export default createJestConfig(config)
  ```
- [x] `jest.setup.ts` oluştur:
  ```ts
  import '@testing-library/jest-dom'
  ```
- [x] Playwright kurulumu:
  ```bash
  npm install -D @playwright/test
  npx playwright install
  ```
- [x] `playwright.config.ts` oluştur:
  ```ts
  import { defineConfig, devices } from '@playwright/test'

  export default defineConfig({
    testDir: './e2e',
    fullyParallel: true,
    retries: process.env.CI ? 2 : 0,
    use: {
      baseURL: 'http://localhost:3000',
      trace: 'on-first-retry',
    },
    projects: [
      { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    ],
    webServer: {
      command: 'npm run dev',
      url: 'http://localhost:3000',
      reuseExistingServer: !process.env.CI,
    },
  })
  ```
- [x] `package.json`'a test scriptleri ekle:
  ```json
  {
    "scripts": {
      "test": "jest",
      "test:watch": "jest --watch",
      "test:coverage": "jest --coverage",
      "test:e2e": "playwright test"
    }
  }
  ```
- [x] `npm test` → altyapı çalışıyor, `__tests__/stores/authStore.test.ts` geçiyor

---

### Task 1.9: Frontend Dockerfile

**Tahmini Süre:** 0.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `frontend/Dockerfile` oluştur:
  ```dockerfile
  FROM node:20-alpine

  WORKDIR /app

  COPY package*.json ./
  RUN npm install

  COPY . .

  EXPOSE 3000

  CMD ["npm", "run", "dev"]
  ```
- [x] `frontend/.dockerignore` oluştur:
  ```
  node_modules
  .next
  .env.example
  ```

---

### 📊 Phase 1 Success Metrics

- [x] `npm run dev` → `http://localhost:3000` açılıyor
- [x] `/chat` sayfasına gidilince sidebar görünüyor
- [x] Auth olmadan `/chat`'e gidilince `/login`'e yönlendiriyor
- [x] Sidebar'daki tüm linkler doğru route'a gidiyor
- [x] Dark navy tema tüm bileşenlerde tutarlı görünüyor
- [x] `docker compose up -d` ile frontend container ayağa kalkıyor
- [x] `npm test` → authStore testleri, Sidebar testleri, Button testleri geçiyor

---

## 🎯 Phase 2 Overview

### Scope

**Dahil:**
- Login sayfası
- Register sayfası
- Form validasyonu (client-side)
- Auth API entegrasyonu
- Token yönetimi (accessToken Zustand'da, refresh cookie'de)
- Giriş sonrası `/chat`'e yönlendirme

**Hariç:**
- OAuth (Google/GitHub) butonu
- Şifre sıfırlama sayfası (backend hazır, opsiyonel)

### Definition of Done

- [x] Login formu çalışıyor, hata mesajları gösteriliyor
- [x] Register formu çalışıyor
- [x] Giriş sonrası token Zustand'a yazılıyor
- [x] Korumalı sayfalara erişim sağlanıyor
- [x] Logout çalışıyor, token temizleniyor
- [x] `npm test` → auth hook testleri, login/register form testleri geçiyor

---

## 📅 Week 2: Login, Register, Auth State

**Hedef:** Auth sayfaları, form yönetimi, token akışı

---

### Task 2.1: TypeScript Tipleri — Auth

**Tahmini Süre:** 0.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `src/types/auth.ts` oluştur:
  ```ts
  export interface LoginRequest {
    email: string
    password: string
  }

  export interface RegisterRequest {
    email: string
    password: string
    display_name: string
  }

  export interface TokenResponse {
    access_token: string
    token_type: string
    expires_in: number
  }

  export interface User {
    id: string
    email: string
    display_name: string
    role: 'user' | 'admin'
    email_verified_at: string | null
    created_at: string
  }
  ```

---

### Task 2.2: Auth Hook'ları

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/hooks/useAuth.test.ts` oluştur:
  ```ts
  import { renderHook, waitFor } from '@testing-library/react'
  import { createWrapper } from '../test-utils'
  import { useLogin, useRegister, useMe } from '@/hooks/useAuth'
  import { api } from '@/lib/api'

  jest.mock('@/lib/api')

  test('useLogin sets access token on success', async () => {
    (api.post as jest.Mock).mockResolvedValueOnce({
      data: { access_token: 'mock-token', token_type: 'bearer', expires_in: 900 }
    })
    const { result } = renderHook(() => useLogin(), { wrapper: createWrapper() })
    result.current.mutate({ email: 'test@test.com', password: 'pass123' })
    await waitFor(() => expect(result.current.isSuccess).toBe(true))
  })

  test('useLogin returns error on 401', async () => {
    (api.post as jest.Mock).mockRejectedValueOnce({ response: { status: 401 } })
    const { result } = renderHook(() => useLogin(), { wrapper: createWrapper() })
    result.current.mutate({ email: 'bad@test.com', password: 'wrong' })
    await waitFor(() => expect(result.current.isError).toBe(true))
  })

  test('useMe returns null when not authenticated', () => {
    const { result } = renderHook(() => useMe(), { wrapper: createWrapper() })
    expect(result.current.data).toBeUndefined()
  })
  ```
- [x] `src/hooks/useAuth.ts` oluştur:
  ```ts
  export function useLogin() {
    return useMutation({
      mutationFn: async (data: LoginRequest) => {
        const res = await api.post<TokenResponse>('/auth/login', data)
        return res.data
      },
      onSuccess: (data) => {
        useAuthStore.getState().setAccessToken(data.access_token)
        queryClient.invalidateQueries({ queryKey: ['me'] })
      }
    })
  }

  export function useRegister() { ... }
  export function useLogout() { ... }
  export function useMe() {
    return useQuery({
      queryKey: ['me'],
      queryFn: () => api.get<User>('/users/me').then(r => r.data),
      enabled: !!useAuthStore.getState().accessToken,
    })
  }
  ```
- [x] Ekstra test — `useRegister sends register payload` senaryosu eklendi

---

### Task 2.3: Login Sayfası

**Tahmini Süre:** 2 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/auth/LoginForm.test.tsx` oluştur:
  ```tsx
  import { render, screen, fireEvent, waitFor } from '@testing-library/react'
  import userEvent from '@testing-library/user-event'
  import LoginPage from '@/app/(auth)/login/page'

  test('renders email and password inputs', () => {
    render(<LoginPage />)
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
  })

  test('shows error when submitting empty form', async () => {
    render(<LoginPage />)
    fireEvent.click(screen.getByRole('button', { name: /giriş/i }))
    await waitFor(() => {
      expect(screen.getByText(/boş olamaz|gerekli/i)).toBeInTheDocument()
    })
  })

  test('shows error for invalid email format', async () => {
    render(<LoginPage />)
    await userEvent.type(screen.getByLabelText(/email/i), 'notanemail')
    fireEvent.click(screen.getByRole('button', { name: /giriş/i }))
    await waitFor(() => {
      expect(screen.getByText(/geçerli.*email/i)).toBeInTheDocument()
    })
  })

  test('login button shows loading state during submission', async () => {
    render(<LoginPage />)
    await userEvent.type(screen.getByLabelText(/email/i), 'test@test.com')
    await userEvent.type(screen.getByLabelText(/password/i), 'password123')
    fireEvent.click(screen.getByRole('button', { name: /giriş/i }))
    expect(screen.getByRole('button', { name: /giriş/i })).toBeDisabled()
  })

  test('shows locked account message on 423', async () => {
    jest.mock('@/hooks/useAuth', () => ({
      useLogin: () => ({
        mutate: () => {},
        error: { response: { status: 423 } },
        isError: true,
      })
    }))
    render(<LoginPage />)
    await waitFor(() => {
      expect(screen.getByText(/kilitlendi/i)).toBeInTheDocument()
    })
  })
  ```
- [x] `src/app/(auth)/login/page.tsx` oluştur:
  - [x] Ortalanmış kart layout (navy-800 arka plan)
  - [x] "News AI" logo/başlık üstte
  - [x] Email input
  - [x] Password input (göster/gizle toggle)
  - [x] "Giriş Yap" butonu (loading state ile)
  - [x] Hata mesajı (API'den gelen: "E-posta veya şifre hatalı")
  - [x] "Hesabın yok mu? Kayıt ol" linki
  - [x] Başarılı girişte `/chat`'e yönlendirme
- [x] Form validasyonu:
  - [x] Email format kontrolü
  - [x] Şifre boş olamaz
  - [x] Submit butonuna basılmadan hata gösterme
- [x] 423 (hesap kilitli) için özel mesaj: "Hesabınız geçici olarak kilitlendi"

---

### Task 2.4: Register Sayfası

**Tahmini Süre:** 2 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/auth/RegisterForm.test.tsx` oluştur:
  ```tsx
  test('renders all required fields', () => {
    render(<RegisterPage />)
    expect(screen.getByLabelText(/display name/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
  })

  test('shows error when password is too short', async () => {
    render(<RegisterPage />)
    await userEvent.type(screen.getByLabelText(/password/i), 'short')
    fireEvent.blur(screen.getByLabelText(/password/i))
    await waitFor(() => {
      expect(screen.getByText(/8 karakter/i)).toBeInTheDocument()
    })
  })

  test('shows 409 error when email already exists', async () => {
    // Mock useRegister ile 409 simüle et
    ...
    await waitFor(() => {
      expect(screen.getByText(/zaten kullanılıyor/i)).toBeInTheDocument()
    })
  })
  ```
- [x] `src/app/(auth)/register/page.tsx` oluştur:
  - [x] Display name input
  - [x] Email input
  - [x] Password input (min 8 karakter göstergesi)
  - [x] "Kayıt Ol" butonu (loading state ile)
  - [x] Başarılı kayıt → login sayfasına yönlendirme + "Kayıt başarılı" toast
  - [x] 409 (email zaten kullanılıyor) için özel mesaj
- [x] Form validasyonu:
  - [x] Display name: min 2 karakter
  - [x] Email: format kontrolü
  - [x] Password: min 8 karakter, anlık gösterge
- [x] Ekstra test — `redirects to login and shows success toast on successful register` senaryosu eklendi

---

### Task 2.5: Toast Bildirimleri

**Tahmini Süre:** 1 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — auth işlemlerinde toast çağrısını test et:
  ```tsx
  import { toast } from 'sonner'
  jest.mock('sonner', () => ({ toast: { success: jest.fn(), error: jest.fn() } }))

  test('shows success toast on register', async () => {
    // Register işlemini simüle et
    ...
    expect(toast.success).toHaveBeenCalledWith(expect.stringMatching(/Hoş geldin/i))
  })
  ```
- [x] Root layout'a `<Toaster>` ekle (dark tema ile)
- [x] Auth işlemlerinde toast kullan:
  - [x] Kayıt başarılı: "Hoş geldin! Giriş yapabilirsin."
  - [x] Giriş başarılı: "Tekrar hoş geldin, [display_name]!"
  - [x] Çıkış: "Güvenli çıkış yapıldı."
  - [x] Hata: API'den gelen hata mesajı
- [x] Ekstra test — `__tests__/hooks/useAuthToasts.test.ts` ile login/logout/error toast senaryoları eklendi

---

### 📊 Phase 2 Success Metrics

- [x] Login formu yanlış şifrede hata gösteriyor
- [x] Başarılı girişte `/chat`'e yönlendiriyor
- [x] Sayfa yenilenince token refresh ile oturum devam ediyor
- [x] Logout sonrası korumalı sayfaya gidilince `/login`'e yönlendiriyor
- [x] Register → Login akışı sorunsuz
- [x] `npm test` → LoginForm, RegisterForm, useAuth hook testleri geçiyor

---

## 🎯 Phase 3 Overview

### Scope

**Dahil:**
- Chat ana sayfası (Screen 1)
- Boş durum (welcome screen + suggested questions)
- Mesaj gönderme formu
- Kullanıcı mesajı (sağ) + AI cevabı (sol) layout'u
- Kaynak linkleri (Tavily'den gelen sources)
- Konuşma listesi sidebar içinde
- Yeni konuşma başlatma
- Streaming desteği (backend hazırsa)

**Hariç:**
- Konuşma arama
- Mesaj kopyalama

### Definition of Done

- [x] Kullanıcı mesaj gönderebiliyor
- [x] AI cevabı kaynaklar ile birlikte görünüyor
- [x] Boş state'de suggested questions görünüyor
- [x] Konuşma listesi sidebar'da görünüyor
- [x] `npm test` → chat bileşen testleri geçiyor

---

## 📅 Week 3: Chat UI & Mesaj Gönderme

**Hedef:** Chat arayüzü, mesaj bileşenleri, API entegrasyonu

---

### Task 3.1: TypeScript Tipleri — Conversation

**Tahmini Süre:** 0.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `src/types/conversation.ts` oluştur:
  ```ts
  export interface Conversation {
    id: string
    title: string
    updated_at: string
  }

  export interface Message {
    id: string
    role: 'user' | 'assistant' | 'system'
    content: string
    sources: Source[] | null
    created_at: string
  }

  export interface Source {
    title: string
    url: string
    snippet: string
  }

  export interface ConversationDetail extends Conversation {
    messages: Message[]
  }
  ```

---

### Task 3.2: Conversation Hook'ları

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/hooks/useConversations.test.ts` oluştur:
  ```ts
  test('useConversations fetches conversation list', async () => {
    (api.get as jest.Mock).mockResolvedValueOnce({
      data: [{ id: '1', title: 'Test Conv', updated_at: '2024-01-01' }]
    })
    const { result } = renderHook(() => useConversations(), { wrapper: createWrapper() })
    await waitFor(() => expect(result.current.isSuccess).toBe(true))
    expect(result.current.data).toHaveLength(1)
  })

  test('useSendMessage adds optimistic user message', async () => {
    (api.post as jest.Mock).mockResolvedValueOnce({
      data: { id: '2', role: 'assistant', content: 'AI response', sources: null, created_at: '' }
    })
    // Optimistic update: kullanıcı mesajı anında görünmeli
    ...
  })
  ```
- [x] `src/hooks/useConversations.ts` oluştur:
  ```ts
  export function useConversations() {
    return useQuery({
      queryKey: ['conversations'],
      queryFn: () => api.get<Conversation[]>('/conversations').then(r => r.data)
    })
  }

  export function useCreateConversation() {
    return useMutation({
      mutationFn: () => api.post<Conversation>('/conversations'),
      onSuccess: (data) => {
        queryClient.invalidateQueries({ queryKey: ['conversations'] })
        router.push(`/chat/${data.data.id}`)
      }
    })
  }

  export function useDeleteConversation() { ... }
  ```
- [x] `src/hooks/useMessages.ts` oluştur (optimistic update dahil)
- [x] Ekstra test — `__tests__/hooks/useMessages.test.ts` ile optimistic user message ve assistant response cache güncellemesi eklendi
- [x] Ekstra test — `useDeleteConversation` için cache invalidation senaryosu eklendi

---

### Task 3.3: Mesaj Bileşenleri

**Tahmini Süre:** 2.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/chat/AssistantMessage.test.tsx` oluştur:
  ```tsx
  test('renders AI response content', () => {
    render(<AssistantMessage content="Here is your news summary" sources={null} />)
    expect(screen.getByText(/Here is your news summary/)).toBeInTheDocument()
  })

  test('renders sources when provided', () => {
    const sources = [{ title: 'BBC News', url: 'http://bbc.com', snippet: 'snippet' }]
    render(<AssistantMessage content="News" sources={sources} />)
    expect(screen.getByText('BBC News')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'BBC News' })).toHaveAttribute('href', 'http://bbc.com')
  })

  test('does not render sources section when sources is null', () => {
    render(<AssistantMessage content="News" sources={null} />)
    expect(screen.queryByText(/Sources/i)).not.toBeInTheDocument()
  })

  test('sources links open in new tab', () => {
    const sources = [{ title: 'CNN', url: 'http://cnn.com', snippet: '' }]
    render(<AssistantMessage content="News" sources={sources} />)
    expect(screen.getByRole('link', { name: 'CNN' })).toHaveAttribute('target', '_blank')
  })
  ```
- [x] `src/components/chat/UserMessage.tsx`:
  - [x] Sağa yaslanmış balon, navy-600 arka plan
  - [x] Kullanıcı avatarı (display_name'in ilk harfi)
- [x] `src/components/chat/AssistantMessage.tsx`:
  - [x] Sola yaslanmış, News AI ikonu sol üstte
  - [x] Markdown render desteği (`react-markdown`)
  - [x] Altta "Sources" bölümü (sources varsa):
    ```tsx
    <div className="mt-3 flex flex-wrap gap-2">
      {sources.map(source => (
        <a href={source.url} target="_blank" rel="noopener noreferrer" className="source-chip">
          {source.title}
        </a>
      ))}
    </div>
    ```
- [x] `src/components/chat/TypingIndicator.tsx`: 3 nokta animasyonu
- [x] `src/components/chat/MessageList.tsx`: mesajları map'le, yeni mesajda otomatik scroll
- [x] Ekstra test — `__tests__/components/chat/UserMessage.test.tsx`, `TypingIndicator.test.tsx`, `MessageList.test.tsx` eklendi

---

### Task 3.4: Mesaj Gönderme Formu

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/chat/MessageInput.test.tsx` oluştur:
  ```tsx
  test('renders textarea', () => {
    render(<MessageInput onSend={jest.fn()} disabled={false} />)
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  test('does not submit empty message', () => {
    const onSend = jest.fn()
    render(<MessageInput onSend={onSend} disabled={false} />)
    fireEvent.click(screen.getByRole('button'))
    expect(onSend).not.toHaveBeenCalled()
  })

  test('submits on Enter key', async () => {
    const onSend = jest.fn()
    render(<MessageInput onSend={onSend} disabled={false} />)
    await userEvent.type(screen.getByRole('textbox'), 'Hello{Enter}')
    expect(onSend).toHaveBeenCalledWith('Hello')
  })

  test('does not submit on Shift+Enter', async () => {
    const onSend = jest.fn()
    render(<MessageInput onSend={onSend} disabled={false} />)
    await userEvent.type(screen.getByRole('textbox'), 'Hello{Shift>}{Enter}')
    expect(onSend).not.toHaveBeenCalled()
  })

  test('send button is disabled when prop disabled=true', () => {
    render(<MessageInput onSend={jest.fn()} disabled={true} />)
    expect(screen.getByRole('button')).toBeDisabled()
  })

  test('shows character count', async () => {
    render(<MessageInput onSend={jest.fn()} disabled={false} />)
    await userEvent.type(screen.getByRole('textbox'), 'Test message')
    expect(screen.getByText(/12.*4000/)).toBeInTheDocument()
  })
  ```
- [x] `src/components/chat/MessageInput.tsx`:
  - [x] `textarea` (Enter gönderir, Shift+Enter satır atlar)
  - [x] Dinamik yükseklik (max 5 satır)
  - [x] Gönder butonu (Send ikonu)
  - [x] Boş mesaj gönderilemiyor
  - [x] Pending state'inde devre dışı
  - [x] Karakter sayacı (4000 limit)

---

### Task 3.5: Welcome Screen & Suggested Questions

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/chat/WelcomeScreen.test.tsx` oluştur:
  ```tsx
  test('renders welcome heading', () => {
    render(<WelcomeScreen onSuggestClick={jest.fn()} />)
    expect(screen.getByText(/Welcome to News AI/i)).toBeInTheDocument()
  })

  test('renders 3 suggested questions', () => {
    render(<WelcomeScreen onSuggestClick={jest.fn()} />)
    const cards = screen.getAllByRole('button')
    expect(cards.length).toBeGreaterThanOrEqual(3)
  })

  test('clicking suggested question calls onSuggestClick', () => {
    const onSuggestClick = jest.fn()
    render(<WelcomeScreen onSuggestClick={onSuggestClick} />)
    fireEvent.click(screen.getAllByRole('button')[0])
    expect(onSuggestClick).toHaveBeenCalledWith(expect.any(String))
  })
  ```
- [x] `src/components/chat/WelcomeScreen.tsx`:
  - [x] Ortalanmış rocket/AI ikonu
  - [x] "Welcome to News AI" başlığı
  - [x] 3 adet suggested question kartı
  - [x] Mesaj listesi boşsa göster, dolu ise gizle
- [x] Ekstra test — `__tests__/components/chat/WelcomeScreenVisibility.test.tsx` ile gizli durumda render etmeme senaryosu eklendi

---

### Task 3.6: Chat Sayfaları

**Tahmini Süre:** 2 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `src/app/(dashboard)/chat/page.tsx` → `useCreateConversation` ile otomatik konuşma oluştur
- [x] `src/app/(dashboard)/chat/[id]/page.tsx`:
  - [x] `useMessages(id)` ile mesajları çek
  - [x] `<MessageList>` + `<MessageInput>` layout'u
  - [x] Conversation bulunamazsa (404) → `/chat`'e yönlendirme
- [x] Ekstra test — `__tests__/components/chat/ChatPages.test.tsx` ile auto-create, render ve 404 redirect senaryoları eklendi

---

### Task 3.7: Sidebar'a Konuşma Listesi

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/chat/ConversationList.test.tsx` oluştur:
  ```tsx
  test('renders conversation titles', () => {
    const conversations = [
      { id: '1', title: 'Conv 1', updated_at: '2024-01-01' },
      { id: '2', title: 'Conv 2', updated_at: '2024-01-02' }
    ]
    render(<ConversationList conversations={conversations} activeId={null} onDelete={jest.fn()} />)
    expect(screen.getByText('Conv 1')).toBeInTheDocument()
    expect(screen.getByText('Conv 2')).toBeInTheDocument()
  })

  test('shows delete button on hover', async () => {
    const conversations = [{ id: '1', title: 'Conv 1', updated_at: '2024-01-01' }]
    render(<ConversationList conversations={conversations} activeId={null} onDelete={jest.fn()} />)
    await userEvent.hover(screen.getByText('Conv 1'))
    expect(screen.getByRole('button', { name: /delete|sil/i })).toBeInTheDocument()
  })

  test('calls onDelete when delete button clicked', async () => {
    const onDelete = jest.fn()
    const conversations = [{ id: '1', title: 'Conv 1', updated_at: '2024-01-01' }]
    render(<ConversationList conversations={conversations} activeId={null} onDelete={onDelete} />)
    await userEvent.hover(screen.getByText('Conv 1'))
    fireEvent.click(screen.getByRole('button', { name: /delete|sil/i }))
    expect(onDelete).toHaveBeenCalledWith('1')
  })
  ```
- [x] `src/components/chat/ConversationList.tsx`:
  - [x] `useConversations()` ile listeyi çek
  - [x] Her konuşma: başlık + tarih (relative: "2 saat önce")
  - [x] Aktif konuşma highlight
  - [x] Hover'da sil ikonu
  - [x] "Yeni Sohbet" butonu listenin üstünde

---

## 📅 Week 4 (ilk yarı): Konuşma Yönetimi & Streaming

**Hedef:** Konuşma yönetimi (silme, arşivleme), SSE streaming

---

### Task 4.1: Konuşma Yönetimi

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — konuşma silme confirm dialog testleri (+ başlık düzenleme testleri):
  ```tsx
  test('shows confirm dialog before deleting conversation', async () => {
    ...
    fireEvent.click(screen.getByRole('button', { name: /sil/i }))
    expect(screen.getByText(/emin misiniz/i)).toBeInTheDocument()
  })

  test('cancelling delete dialog does not call delete mutation', async () => {
    ...
    fireEvent.click(screen.getByRole('button', { name: /iptal/i }))
    expect(mockDelete).not.toHaveBeenCalled()
  })
  ```
- [x] Konuşma silme:
  - [x] Hover'daki silme ikonuna tıklayınca confirm dialog
  - [x] `useDeleteConversation` mutation
  - [x] Silinen konuşma listeden kaldırılır, aktifse `/chat`'e yönlendirilir
- [x] Konuşma başlığı düzenleme:
  - [x] Başlığa çift tıklanınca inline edit moduna geçiş
  - [x] Enter ile kaydet, Escape ile iptal

**Ekstra testler:** `__tests__/components/chat/ConversationListManagement.test.tsx` — 6 test (delete dialog, title editing)

---

### Task 4.2: Streaming Desteği (Backend Hazırsa)

**Tahmini Süre:** 2 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] SSE bağlantısı için hook yaz:
  ```ts
  export function useStreamMessage(conversationId: string) {
    const [streamContent, setStreamContent] = useState('')
    const [isStreaming, setIsStreaming] = useState(false)

    const sendStreaming = async (content: string) => {
      setIsStreaming(true)
      setStreamContent('')
      const response = await fetch(
        `${API_URL}/conversations/${conversationId}/messages/stream`,
        { method: 'POST', headers: { Authorization: `Bearer ${token}` }, body: JSON.stringify({ content }) }
      )
      const reader = response.body?.getReader()
      // SSE token'larını oku, state'e yaz
    }
    return { sendStreaming, streamContent, isStreaming }
  }
  ```
- [x] AssistantMessage'a streaming sırasında kayan imleç animasyonu ekle

**Test dosyaları:** 
- `__tests__/hooks/useStreamMessage.test.ts` — 5 test (hook initialization, streaming, content accumulation)
- `__tests__/components/chat/AssistantMessageStreaming.test.tsx` — 6 test (cursor animation, streaming state)

---

### 📊 Phase 3 Success Metrics

- [x] Mesaj gönderildiğinde kullanıcı mesajı anında görünüyor (optimistic update)
- [x] AI cevabı kaynaklarla birlikte geliyor
- [x] Suggested question'a tıklayınca input'a yazılıyor
- [x] Konuşma listesi sidebar'da güncel sırada görünüyor
- [x] Silinmiş konuşma listeden kaldırılıyor
- [x] `npm test` → MessageInput, AssistantMessage, WelcomeScreen, ConversationList testleri geçiyor

---

## 🎯 Phase 4 Overview

### Scope

**Dahil:**
- Fact Check Engine sayfası (Screen 2)
- Claim input alanı
- Verdict kartı (TRUE/FALSE/UNVERIFIED)
- Kaynak listesi
- Son doğrulamalar paneli

### Definition of Done

- [x] Claim gönderilince verdict kartı görünüyor
- [x] Kaynaklar tıklanabilir linkler olarak görünüyor
- [x] Son doğrulamalar listesi yükleniyor
- [x] Loading state animasyonlu görünüyor
- [x] `npm test` → VerdictCard, ClaimInput testleri geçiyor

---

## 📅 Week 4 (ikinci yarı): Fact Check UI

**Hedef:** Fact check sayfası, verdict bileşeni, geçmiş listesi

---

### Task 4.3: TypeScript Tipleri — Fact Check

**Tahmini Süre:** 0.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `src/types/factCheck.ts` oluştur:
  ```ts
  export type Verdict = 'TRUE' | 'FALSE' | 'UNVERIFIED'

  export interface FactCheck {
    id: string
    claim: string
    verdict: Verdict
    explanation: string
    sources: Source[]
    confidence_score: number
    created_at: string
  }
  ```

---

### Task 4.4: Fact Check Hook'ları

**Tahmini Süre:** 1 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/hooks/useFactCheck.test.ts` oluştur:
  ```ts
  test('useRunFactCheck sends claim to API', async () => {
    (api.post as jest.Mock).mockResolvedValueOnce({
      data: { id: '1', claim: 'test', verdict: 'TRUE', explanation: 'True.', sources: [], confidence_score: 0.9, created_at: '' }
    })
    const { result } = renderHook(() => useRunFactCheck(), { wrapper: createWrapper() })
    result.current.mutate('test claim')
    await waitFor(() => expect(result.current.isSuccess).toBe(true))
    expect(api.post).toHaveBeenCalledWith('/fact-check', { claim: 'test claim' })
  })

  test('useRunFactCheck invalidates fact-check-history on success', async () => {
    const invalidate = jest.spyOn(queryClient, 'invalidateQueries')
    ...
    await waitFor(() => expect(invalidate).toHaveBeenCalledWith({ queryKey: ['fact-check-history'] }))
  })
  ```
- [x] `src/hooks/useFactCheck.ts` oluştur:
  ```ts
  export function useRunFactCheck() {
    return useMutation({
      mutationFn: (claim: string) =>
        api.post<FactCheck>('/fact-check', { claim }).then(r => r.data),
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ['fact-check-history'] })
      }
    })
  }

  export function useFactCheckHistory() {
    return useQuery({
      queryKey: ['fact-check-history'],
      queryFn: () => api.get<FactCheck[]>('/fact-check/history').then(r => r.data),
      enabled: !!useAuthStore.getState().accessToken,
    })
  }
  ```

---

### Task 4.5: Fact Check Bileşenleri

**Tahmini Süre:** 3 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/fact-check/VerdictCard.test.tsx` oluştur (6 test)
- [x] `src/components/fact-check/ClaimInput.tsx`:
  - [x] Büyük textarea (claim veya URL yapıştırılır)
  - [x] "Verify Claim" butonu — loading state'inde "Verifying..." yazar
  - [x] Placeholder: "Paste a claim, headline, or URL to verify..."
- [x] `src/components/fact-check/VerdictCard.tsx`:
  - [x] Büyük verdict badge (TRUE=yeşil, FALSE=kırmızı, UNVERIFIED=sarı)
  - [x] Confidence score progress bar (0-100%)
  - [x] Explanation metni
  - [x] Kaynak listesi (tıklanabilir linkler)
  - [x] Loading state: skeleton animasyonu (`data-testid="verdict-skeleton"`)
- [x] `src/components/fact-check/RecentVerifications.tsx`:
  - [x] Scrollable liste
  - [x] Her kart: claim metni (kısaltılmış) + verdict badge + tarih
- [x] `src/app/(dashboard)/fact-check/page.tsx`:
  - [x] Üstte ClaimInput
  - [x] Ortada VerdictCard (sonuç geldikten sonra)
  - [x] Sağda RecentVerifications paneli

**Ekstra Testler:** `__tests__/components/fact-check/ClaimInput.test.tsx` (7 test) ve `__tests__/components/fact-check/RecentVerifications.test.tsx` (5 test) eklendi

---

### 📊 Phase 4 Success Metrics

- [x] Claim girilip verify'a basılınca loading animasyonu başlıyor
- [x] Verdict kartı doğru renkle görünüyor (TRUE=yeşil, FALSE=kırmızı)
- [x] Kaynaklar tıklanınca yeni sekmede açılıyor
- [x] Giriş yapılmadan da fact check çalışıyor
- [x] Giriş yapılınca geçmiş paneli doluyor
- [x] `npm test` → VerdictCard, ClaimInput, RecentVerifications testleri geçiyor (18 test, tümü ✅)

---

## 🎯 Phase 5 Overview

### Scope

**Dahil:**
- News Feed sayfası (Screen 3)
- Today / This Week / This Month sekme filtreleri
- Haber kartları (başlık, kaynak, tarih, AI özeti, link)
- AI özeti yükleme butonu (özetlenmemiş kartlar için)
- Makale kaydetme butonu

### Definition of Done

- [x] News Feed sekme filtreleri çalışıyor
- [x] Kartlar düzgün görünüyor, AI özeti var
- [x] Makale kaydetme çalışıyor
- [x] Loading skeleton gösteriliyor
- [x] `npm test` → NewsCard, PeriodFilter testleri geçiyor

---

## 📅 Week 5: News Feed UI & Filtreler

**Hedef:** News feed sayfası, kart bileşeni, filtreler, kaydetme

---

### Task 5.1: TypeScript Tipleri — News

**Tahmini Süre:** 0.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `src/types/news.ts` oluştur:
  ```ts
  export interface Article {
    title: string
    url: string
    source_name: string
    published_at: string | null
    ai_summary: string | null
    category: string
  }

  export interface SavedArticle extends Article {
    id: string
    saved_at: string
  }

  export type FeedPeriod = 'today' | 'week' | 'month'
  ```

---

### Task 5.2: News Hook'ları

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/hooks/useNews.test.ts` oluştur (8 test):
  - [x] useNewsFeed fetches with correct params
  - [x] useNewsFeed fetches with different categories and periods
  - [x] useNewsFeed handles API errors
  - [x] useNewsFeed returns empty array
  - [x] useSaveArticle saves article successfully
  - [x] useSaveArticle shows 409 error toast on duplicate
  - [x] useSaveArticle shows generic error toast on other errors
  - [x] useSaveArticle invalidates cache on success
- [x] `src/hooks/useNews.ts` oluştur:
  ```ts
  export function useNewsFeed(category: string, period: FeedPeriod) {
    return useQuery({
      queryKey: ['news-feed', category, period],
      queryFn: async () => {
        const { data } = await api.get<Article[]>('/news/feed', {
          params: { category, period },
        })
        return data
      },
    })
  }

  export function useSaveArticle() {
    return useMutation({
      mutationFn: async (article: Article) => {
        const { data } = await api.post<SavedArticle>('/news/saved', article)
        return data
      },
      onSuccess: () => {
        toast.success('Article saved successfully!')
        queryClient.invalidateQueries({ queryKey: ['news-feed'] })
        queryClient.invalidateQueries({ queryKey: ['saved-articles'] })
      },
      onError: (error: any) => {
        if (error.response?.status === 409) {
          toast.error('Bu makale zaten kaydedilmiş!')
        } else {
          toast.error('Makale kaydedilirken bir hata oluştu.')
        }
      },
    })
  }
  ```

---

### Task 5.3: News Feed Bileşenleri

**Tahmini Süre:** 3 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/news/NewsCard.test.tsx` oluştur:
  ```tsx
  test('renders article title and source', () => {
    render(<NewsCard article={{ title: 'Big News', url: 'http://news.com', source_name: 'BBC', published_at: '2024-01-01', ai_summary: 'Summary text', category: 'technology' }} />)
    expect(screen.getByText('Big News')).toBeInTheDocument()
    expect(screen.getByText('BBC')).toBeInTheDocument()
  })

  test('shows Summarize button when ai_summary is null', () => {
    render(<NewsCard article={{ title: 'News', url: 'http://n.com', source_name: 'CNN', published_at: null, ai_summary: null, category: 'world' }} />)
    expect(screen.getByRole('button', { name: /summarize/i })).toBeInTheDocument()
  })

  test('does not show Summarize button when ai_summary exists', () => {
    render(<NewsCard article={{ title: 'News', url: 'http://n.com', source_name: 'CNN', published_at: null, ai_summary: 'Already summarized', category: 'world' }} />)
    expect(screen.queryByRole('button', { name: /summarize/i })).not.toBeInTheDocument()
  })

  test('bookmark button toggles saved state', async () => {
    const onSave = jest.fn()
    render(<NewsCard article={{ title: 'News', url: 'http://n.com', source_name: 'CNN', published_at: null, ai_summary: null, category: 'world' }} onSave={onSave} />)
    fireEvent.click(screen.getByRole('button', { name: /bookmark|kaydet/i }))
    expect(onSave).toHaveBeenCalled()
  })

  test('Read Full Article link opens in new tab', () => {
    render(<NewsCard article={{ title: 'News', url: 'http://n.com', source_name: 'CNN', published_at: null, ai_summary: null, category: 'world' }} />)
    const link = screen.getByRole('link', { name: /read full/i })
    expect(link).toHaveAttribute('target', '_blank')
    expect(link).toHaveAttribute('href', 'http://n.com')
  })
  ```
- [x] `src/components/news/NewsCard.tsx`
- [x] `src/components/news/NewsCardSkeleton.tsx`
- [x] `src/components/news/PeriodFilter.tsx`:
  - [x] Today / This Week / This Month tab'ları
  - [x] Aktif tab accent-blue alt border
- [x] `src/app/(dashboard)/feed/page.tsx`

---

### 📊 Phase 5 Success Metrics

- [x] Today sekmesinde bugünün haberleri geliyor
- [x] AI özeti olmayan kartlarda "Summarize" butonu görünüyor
- [x] Bookmark'a basınca saved articles'a ekleniyor
- [x] 409 durumunda "zaten kaydedilmiş" toast'u çıkıyor
- [x] `npm test` → NewsCard testleri geçiyor (7/7 tests passing)

---

## 🎯 Phase 6 Overview

### Scope

**Dahil:**
- Trending sayfası (Screen 4 — "Global Pulse")
- Kategori filter chip'leri
- Trending kart grid'i (büyük görselli)
- `view_count` bazlı sıralama

---

## 📅 Week 6 (ilk yarı): Trending UI

**Hedef:** Trending sayfası, kart grid'i, kategori filtreleri

---

### Task 6.1: Trending Hook'ları

**Tahmini Süre:** 1 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/hooks/useTrending.test.ts` oluştur (3 test):
  - [x] topic ile `/news/trending` çağrısı
  - [x] topic olmadan `/news/trending` çağrısı
  - [x] API error handling
- [x] `src/hooks/useTrending.ts` oluştur:
  ```ts
  export function useTrending(topic?: string) {
    return useQuery({
      queryKey: ['trending', topic],
      queryFn: () => api.get<Article[]>('/news/trending', { params: { topic } }).then(r => r.data),
      staleTime: 1000 * 60 * 5,
    })
  }
  ```

---

### Task 6.2: Trending Bileşenleri

**Tahmini Süre:** 2.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/news/CategoryChips.test.tsx` oluştur:
  ```tsx
  test('renders all category chips', () => {
    render(<CategoryChips activeChip={null} onSelect={jest.fn()} />)
    expect(screen.getByText(/Technology/i)).toBeInTheDocument()
    expect(screen.getByText(/Finance/i)).toBeInTheDocument()
  })

  test('active chip has accent styling', () => {
    render(<CategoryChips activeChip="Technology" onSelect={jest.fn()} />)
    const chip = screen.getByText('Technology').closest('button')
    expect(chip?.className).toMatch(/accent|active|bg-accent/)
  })

  test('clicking chip calls onSelect with chip name', () => {
    const onSelect = jest.fn()
    render(<CategoryChips activeChip={null} onSelect={onSelect} />)
    fireEvent.click(screen.getByText(/Technology/i))
    expect(onSelect).toHaveBeenCalledWith('Technology')
  })
  ```
- [x] `src/components/news/CategoryChips.tsx`
- [x] `src/components/news/TrendingCard.tsx`
- [x] `src/app/(dashboard)/trending/page.tsx`

**Ekstra Testler (Task 6.2 kapsamında eklendi):**
- [x] `__tests__/components/news/TrendingCard.test.tsx` (2 test)
- [x] `__tests__/components/news/TrendingPage.test.tsx` (2 test)

**Doğrulama:**
- [x] `npm test -- __tests__/components/news/CategoryChips.test.tsx __tests__/components/news/TrendingCard.test.tsx __tests__/components/news/TrendingPage.test.tsx`

---

### 📊 Phase 6 Success Metrics

- [x] Trending sayfası "Global Pulse" başlığıyla açılıyor
- [x] Kategori chip'lerine tıklanınca kartlar filtreleniyor
- [x] Kartlar `view_count`'a göre sıralı geliyor
- [x] `npm test` → CategoryChips testleri geçiyor

---

## 🎯 Phase 7 Overview

### Scope

**Dahil:**
- Sports sayfası (Screen 5) — sub-kategori chip'leri ile
- Technology sayfası (Screen 6) — 3 sütunlu grid
- Dinamik `/category/[slug]` route (her kategori için çalışır)

---

## 📅 Week 6 (ikinci yarı) & Week 7: Sports & Technology Sayfaları

**Hedef:** Kategori sayfaları, sub-kategori filtreleri, dinamik routing

---

### Task 7.1: Kategori Hook'ları

**Tahmini Süre:** 1 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/hooks/useNews.test.ts` içine `useCategoryNews` testleri eklendi (3 test):
  - [x] subcategory + page parametreleri ile API çağrısı
  - [x] default page (1) ve undefined subcategory
  - [x] API error handling
- [x] `src/hooks/useNews.ts`'e ekle:
  ```ts
  export function useCategoryNews(category: string, subcategory?: string, page = 1) {
    return useQuery({
      queryKey: ['category-news', category, subcategory, page],
      queryFn: () => api.get<Article[]>(`/news/category/${category}`, {
        params: { subcategory, page, page_size: 12 }
      }).then(r => r.data),
      staleTime: 1000 * 60 * 10,
    })
  }
  ```

**Doğrulama:**
- [x] `npm test -- __tests__/hooks/useNews.test.ts`

---

### Task 7.2: Kategori Sayfası Bileşenleri

**Tahmini Süre:** 3 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/news/SubCategoryChips.test.tsx` oluştur:
  ```tsx
  test('renders sports subcategories for sports category', () => {
    render(<SubCategoryChips category="sports" activeSubcategory={null} onSelect={jest.fn()} />)
    expect(screen.getByText(/Football/i)).toBeInTheDocument()
    expect(screen.getByText(/Basketball/i)).toBeInTheDocument()
  })

  test('renders technology subcategories for technology category', () => {
    render(<SubCategoryChips category="technology" activeSubcategory={null} onSelect={jest.fn()} />)
    expect(screen.getByText(/AI/i)).toBeInTheDocument()
    expect(screen.getByText(/Semiconductors/i)).toBeInTheDocument()
  })

  test('clicking subcategory updates URL query param', async () => {
    const mockPush = jest.fn()
    jest.mock('next/navigation', () => ({ useRouter: () => ({ push: mockPush }), useSearchParams: () => new URLSearchParams() }))
    render(<SubCategoryChips category="sports" activeSubcategory={null} onSelect={jest.fn()} />)
    fireEvent.click(screen.getByText(/Football/i))
    expect(mockPush).toHaveBeenCalledWith(expect.stringContaining('football'))
  })
  ```
- [x] `src/components/news/SubCategoryChips.tsx`
- [x] `src/components/news/CategoryHeader.tsx`
- [x] `src/app/(dashboard)/category/[slug]/page.tsx`:
  - [x] `slug`'dan kategori adını oku
  - [x] Geçersiz slug → 404 sayfası
  - [x] Sports için: büyük featured card (üstte) + 2 sütun grid (altta)
  - [x] Technology için: 3 sütunlu grid
  - [x] Sayfalama (12'şer kart, "Load More" butonu)

**Doğrulama:**
- [x] `npm test -- __tests__/components/news/SubCategoryChips.test.tsx`

---

### 📊 Phase 7 Success Metrics

- [x] `/category/sports` Sports Central başlığıyla açılıyor
- [x] Football chip'ine tıklanınca sadece football haberleri geliyor
- [x] `/category/technology` 3 sütunlu grid ile açılıyor
- [x] "Load More" ile sonraki sayfa yükleniyor
- [x] Geçersiz kategori slug'ında 404 sayfası görünüyor
- [x] `npm test` → SubCategoryChips testleri geçiyor

---

## 🎯 Phase 8 Overview

### Scope

**Dahil:**
- Responsive tasarım (mobil, tablet, desktop)
- Loading ve error state'lerinin tüm sayfalarda tamamlanması
- Kullanıcı tercihleri sayfası (Settings)
- Saved Articles sayfası
- Performance optimizasyonu
- Playwright E2E testleri
- Frontend Dockerfile production build
- Deploy ortamı konfigürasyonu

---

## 📅 Week 8: Polish, Responsive, Deploy

**Hedef:** Eksik ekranlar, responsive, E2E testler, production build

---

### Task 8.1: Settings Sayfası

**Tahmini Süre:** 2 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/settings/PreferencesForm.test.tsx` oluştur:
  ```tsx
  test('renders language selector', () => {
    render(<SettingsPage />)
    expect(screen.getByLabelText(/language/i)).toBeInTheDocument()
  })

  test('renders AI tone selector', () => {
    render(<SettingsPage />)
    expect(screen.getByLabelText(/ai tone/i)).toBeInTheDocument()
  })

  test('save button calls PATCH preferences API', async () => {
    (api.patch as jest.Mock).mockResolvedValueOnce({ data: {} })
    render(<SettingsPage />)
    fireEvent.click(screen.getByRole('button', { name: /kaydet/i }))
    await waitFor(() => expect(api.patch).toHaveBeenCalledWith('/users/me/preferences', expect.any(Object)))
  })
  ```
- [x] `src/app/(dashboard)/settings/page.tsx` oluştur:
  - [x] Profil bölümü: display_name güncelleme
  - [x] Tercihler bölümü:
    - [x] Kategori seçimi (multi-select chip'ler)
    - [x] Dil seçimi (TR / EN)
    - [x] AI tonu (Neutral / Formal / Casual)
    - [x] Email digest toggle
  - [x] "Değişiklikleri Kaydet" butonu
  - [x] Hesabı sil butonu (danger zone)
- [x] Sidebar'a Settings linki ekle (dişli ikonu, en altta)

**Ekstra Testler (Task 8.1 kapsamında eklendi):**
- [x] `__tests__/components/layout/Sidebar.test.tsx` icine `renders settings link in footer` senaryosu eklendi

**Doğrulama:**
- [x] `npm test -- __tests__/components/settings/PreferencesForm.test.tsx __tests__/components/layout/Sidebar.test.tsx`

---

### Task 8.2: Saved Articles Sayfası

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `src/app/(dashboard)/saved/page.tsx` oluştur:
  - [x] `useSavedArticles()` ile liste çek
  - [x] Kategori filtresi
  - [x] Her kart: NewsCard ile aynı tasarım + sil butonu
  - [x] Boş state: "Henüz makale kaydetmediniz"
- [x] Sidebar'a "Saved" linki ekle (Bookmark ikonu)

**Ekstra Testler (Task 8.2 kapsamında eklendi):**
- [x] `__tests__/components/news/SavedPage.test.tsx`
- [x] `__tests__/hooks/useNews.test.ts` içine `useSavedArticles` senaryosu eklendi
- [x] `__tests__/components/layout/Sidebar.test.tsx` içine `renders saved link in footer` senaryosu eklendi

**Doğrulama:**
- [x] `npm test -- __tests__/components/news/SavedPage.test.tsx __tests__/hooks/useNews.test.ts __tests__/components/layout/Sidebar.test.tsx`

---

### Task 8.3: Playwright E2E Testleri

**Tahmini Süre:** 3 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `e2e/auth.spec.ts` oluştur:
  ```ts
  import { test, expect } from '@playwright/test'

  test('full auth flow: register → login → dashboard', async ({ page }) => {
    await page.goto('/register')
    await page.fill('[name="display_name"]', 'Test User')
    await page.fill('[name="email"]', `test-${Date.now()}@test.com`)
    await page.fill('[name="password"]', 'password123')
    await page.click('button[type="submit"]')
    await expect(page).toHaveURL('/login')
    // Login
    await page.fill('[name="email"]', `test-${Date.now()}@test.com`)
    await page.fill('[name="password"]', 'password123')
    await page.click('button[type="submit"]')
    await expect(page).toHaveURL('/chat')
  })

  test('redirects to login when not authenticated', async ({ page }) => {
    await page.goto('/chat')
    await expect(page).toHaveURL('/login')
  })

  test('logout clears session and redirects to login', async ({ page }) => {
    // Giriş yap
    ...
    await page.click('[data-testid="logout-button"]')
    await expect(page).toHaveURL('/login')
    // Tekrar /chat'e gitmeye çalış
    await page.goto('/chat')
    await expect(page).toHaveURL('/login')
  })
  ```
- [x] `e2e/chat.spec.ts` oluştur:
  ```ts
  test('sends message and receives AI response', async ({ page }) => {
    // Login ol
    ...
    await page.goto('/chat')
    await page.fill('[data-testid="message-input"]', 'What is the latest tech news?')
    await page.press('[data-testid="message-input"]', 'Enter')
    // AI cevabı bekle (uzun sürebilir)
    await expect(page.locator('[data-testid="assistant-message"]')).toBeVisible({ timeout: 30000 })
  })

  test('suggested questions click fills input', async ({ page }) => {
    ...
    await page.goto('/chat')
    await page.click('[data-testid="suggested-question"]')
    await expect(page.locator('[data-testid="message-input"]')).not.toBeEmpty()
  })
  ```
- [x] `e2e/fact-check.spec.ts` oluştur:
  ```ts
  test('fact check works without login', async ({ page }) => {
    await page.goto('/fact-check')
    await page.fill('[data-testid="claim-input"]', 'The earth is round')
    await page.click('[data-testid="verify-button"]')
    await expect(page.locator('[data-testid="verdict-card"]')).toBeVisible({ timeout: 30000 })
    const verdict = await page.locator('[data-testid="verdict-badge"]').textContent()
    expect(['TRUE', 'FALSE', 'UNVERIFIED']).toContain(verdict)
  })
  ```

**Ekstra Uyum (Task 8.3 kapsamında eklendi):**
- [x] Chat ve fact-check akışları için gerekli `data-testid` alanları eklendi
- [x] Chat başlangıç ekranında suggested question tıklaması input'u dolduracak şekilde bağlandı
- [x] Auth store kalıcılığı `accessToken` içerecek şekilde güncellendi

**Doğrulama:**
- [x] `npm run test:e2e -- e2e/auth.spec.ts e2e/chat.spec.ts e2e/fact-check.spec.ts`

---

### Task 8.4: Responsive Tasarım

**Tahmini Süre:** 3 saat

**Durum:** ⬜ BEKLEMEDE

**Yapılacaklar:**
- [ ] Test önce — Playwright ile responsive test:
  ```ts
  test('sidebar is hidden by default on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 })
    await page.goto('/chat')
    await expect(page.locator('[data-testid="sidebar"]')).not.toBeVisible()
  })

  test('hamburger opens sidebar on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 })
    await page.goto('/chat')
    await page.click('[data-testid="hamburger-menu"]')
    await expect(page.locator('[data-testid="sidebar"]')).toBeVisible()
  })
  ```
- [ ] Sidebar — mobilde: varsayılan kapalı, hamburger ile açılır, dışarıya tıklanınca kapanır
- [ ] News grid'leri: mobil 1 sütun, tablet 2 sütun, desktop 3-4 sütun
- [ ] Chat sayfası mobilde: tam ekran mesaj alanı, input altta sabit
- [ ] Tüm sayfalarda min 320px genişlikte test et

---

### Task 8.5: Error ve Empty State'ler

**Tahmini Süre:** 1.5 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] Test önce — `__tests__/components/ErrorState.test.tsx` oluştur:
  ```tsx
  test('error state shows retry button', () => {
    const onRetry = jest.fn()
    render(<ErrorState message="Yüklenemedi" onRetry={onRetry} />)
    expect(screen.getByRole('button', { name: /tekrar/i })).toBeInTheDocument()
  })

  test('retry button calls onRetry', () => {
    const onRetry = jest.fn()
    render(<ErrorState message="Yüklenemedi" onRetry={onRetry} />)
    fireEvent.click(screen.getByRole('button', { name: /tekrar/i }))
    expect(onRetry).toHaveBeenCalledTimes(1)
  })
  ```
- [x] Global error boundary bileşeni yaz
- [x] Her `useQuery` için error state UI: "Yüklenemedi. Tekrar dene" butonu
- [x] Empty state'ler:
  - [x] Konuşma listesi boşsa: "Henüz sohbet yok. Yeni bir sohbet başlat."
  - [x] Fact check geçmişi boşsa: "Henüz doğrulama yapmadınız."
  - [x] Saved articles boşsa: "Henüz makale kaydetmediniz."
- [x] 404 sayfası: `/app/not-found.tsx`

**Ekstra Testler (Task 8.5 kapsamında eklendi):**
- [x] `__tests__/components/chat/ConversationList.test.tsx` içine empty state senaryosu eklendi
- [x] `__tests__/components/fact-check/RecentVerifications.test.tsx` empty state metni roadmap ile hizalandi
- [x] `__tests__/components/chat/ChatPages.test.tsx` chat landing davranisina gore guncellendi

**Doğrulama:**
- [x] `npm test -- __tests__/components/ErrorState.test.tsx __tests__/components/chat/ConversationList.test.tsx __tests__/components/fact-check/RecentVerifications.test.tsx __tests__/components/news/SavedPage.test.tsx`
- [x] `npm test -- __tests__/components/chat/ChatPages.test.tsx __tests__/components/news/TrendingPage.test.tsx __tests__/components/fact-check/RecentVerifications.test.tsx __tests__/components/ErrorState.test.tsx __tests__/components/chat/ConversationList.test.tsx __tests__/components/news/SavedPage.test.tsx`

---

### Task 8.6: Production Dockerfile

**Tahmini Süre:** 1 saat

**Durum:** ⬜ BEKLEMEDE

**Yapılacaklar:**
- [ ] `frontend/Dockerfile` production build için güncelle:
  ```dockerfile
  FROM node:20-alpine AS builder
  WORKDIR /app
  COPY package*.json ./
  RUN npm ci
  COPY . .
  RUN npm run build

  FROM node:20-alpine AS runner
  WORKDIR /app
  ENV NODE_ENV=production
  COPY --from=builder /app/.next/standalone ./
  COPY --from=builder /app/.next/static ./.next/static
  COPY --from=builder /app/public ./public
  EXPOSE 3000
  CMD ["node", "server.js"]
  ```
- [ ] `next.config.ts`'e `output: 'standalone'` ekle
- [ ] Production build test: `docker compose up --build`

---

### Task 8.7: Final Kontrol Listesi

**Tahmini Süre:** 1 saat

**Durum:** ✅ TAMAMLANDI

**Yapılacaklar:**
- [x] `npm run build` hatasız tamamlanıyor
- [x] `npm test` → tüm Jest testleri geçiyor
- [x] `npm run test:e2e` → Playwright testleri geçiyor
- [x] `console.log`'ları temizle
- [x] `TODO` ve `FIXME` yorumlarını temizle
- [x] TypeScript hataları yok (`npm run build` hatasız)
- [x] ESLint uyarıları temizlendi
- [x] `next.config.ts`'de `NEXT_PUBLIC_API_URL` production URL'i ile güncelle
- [x] `README.md`'ye frontend kurulum adımları eklendi

---

### 📊 Phase 8 Success Metrics

- [x] `npm run build` hatasız tamamlanıyor
- [x] `npm test` → tüm unit/component testleri geçiyor
- [x] `npm run test:e2e` → E2E senaryoları geçiyor (auth flow, chat, fact check)
- [ ] Mobilde sidebar overlay çalışıyor
- [ ] Tüm sayfalarda loading skeleton var
- [ ] Tüm sayfalarda error state var
- [ ] Boş state'ler açıklayıcı mesajlarla görünüyor
- [ ] `docker compose up --build` frontend'i production modda ayağa kaldırıyor

---

## 📅 Genel Proje Takvimi

| Phase | İçerik | Süre | Durum |
|-------|--------|------|-------|
| **Phase 1** | Project Setup & Layout | 1 hafta | ✅ Tamamlandı |
| **Phase 2** | Auth Ekranları | 1 hafta | ✅ Tamamlandı |
| **Phase 3** | Chat Sayfası (Screen 1) | 1.5 hafta | ✅ Tamamlandı |
| **Phase 4** | Fact Check Engine (Screen 2) | 0.5 hafta | ✅ Tamamlandı |
| **Phase 5** | News Feed (Screen 3) | 1 hafta | ✅ Tamamlandı |
| **Phase 6** | Trending (Screen 4) | 0.5 hafta | ✅ Tamamlandı |
| **Phase 7** | Category Sayfaları (Screen 5 & 6) | 1 hafta | ✅ Tamamlandı |
| **Phase 8** | Polish, Responsive & Deploy | 1 hafta | ⬜ Beklemede |
| **TOPLAM** | | **~7.5 hafta** | |

---

## 🔗 Backend Endpoint ↔ Frontend Sayfa Eşleşmesi

| Sayfa | Kullanılan Endpoint'ler |
|---|---|
| Chat (`/chat/[id]`) | `POST /conversations`, `GET /conversations/{id}`, `POST /conversations/{id}/messages` |
| Fact Check (`/fact-check`) | `POST /fact-check`, `GET /fact-check/history` |
| News Feed (`/feed`) | `GET /news/feed`, `POST /news/saved` |
| Trending (`/trending`) | `GET /news/trending` |
| Category (`/category/[slug]`) | `GET /news/category/{category}` |
| Settings (`/settings`) | `GET /users/me/preferences`, `PATCH /users/me/preferences`, `PATCH /users/me` |
| Saved (`/saved`) | `GET /news/saved`, `DELETE /news/saved/{id}` |

---

> *Backend roadmap: `docs/ROADMAP_BACKEND.md` — Frontend'e geçmeden önce backend Phase 1-3'ün tamamlanmış olması önerilir.*

> *Nisan 2026 notu:* Backend tarafinda CrewAI ic yapisi YAML konfig tabanina tasindi. Bu degisiklik frontend endpoint contract'larini degistirmedigi icin Phase 6-8 bekleyen frontend tasklarini mevcut endpoint tablosuna gore ilerletebilirsin.
