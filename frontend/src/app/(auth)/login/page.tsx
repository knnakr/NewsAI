"use client"

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect, useMemo, useState } from 'react'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { useLogin } from '@/hooks/useAuth'

function isValidEmail(value: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
}

export default function LoginPage() {
  const router = useRouter()
  const login = useLogin()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [submitted, setSubmitted] = useState(false)

  const emailError = useMemo(() => {
    if (!submitted) return ''
    if (!email.trim()) return 'Email boş olamaz'
    if (!isValidEmail(email)) return 'Geçerli bir email giriniz'
    return ''
  }, [email, submitted])

  const passwordError = useMemo(() => {
    if (!submitted) return ''
    if (!password.trim()) return 'Şifre boş olamaz'
    return ''
  }, [password, submitted])

  const apiError = useMemo(() => {
    if (!login.isError) return ''
    const status = (login.error as { response?: { status?: number } })?.response?.status
    if (status === 423) return 'Hesabınız geçici olarak kilitlendi'
    return 'E-posta veya şifre hatalı'
  }, [login.error, login.isError])

  useEffect(() => {
    if (login.isSuccess) {
      router.push('/chat')
    }
  }, [login.isSuccess, router])

  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setSubmitted(true)

    const hasErrors = !email.trim() || !password.trim() || !isValidEmail(email)
    if (hasErrors) return

    login.mutate({ email: email.trim(), password })
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-navy-900 px-4">
      <section className="w-full max-w-md rounded-2xl border border-navy-600 bg-navy-800 p-6 shadow-lg">
        <div className="mb-6 text-center">
          <h1 className="text-2xl font-bold text-slate-100">News AI</h1>
          <p className="mt-1 text-sm text-slate-400">Hesabınıza giriş yapın</p>
        </div>

        <form className="space-y-4" onSubmit={onSubmit} noValidate>
          <Input
            id="email"
            name="email"
            type="email"
            label="Email"
            placeholder="you@example.com"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            error={emailError}
          />

          <div className="space-y-2">
            <Input
              id="password"
              name="password"
              type={showPassword ? 'text' : 'password'}
              label="Password"
              placeholder="Şifrenizi girin"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              error={passwordError}
            />
            <button
              type="button"
              className="text-xs text-slate-300 hover:text-slate-100"
              onClick={() => setShowPassword((current) => !current)}
            >
              {showPassword ? 'Şifreyi gizle' : 'Şifreyi göster'}
            </button>
          </div>

          {apiError ? <p className="text-sm text-red-400">{apiError}</p> : null}

          <Button type="submit" className="w-full" loading={login.isPending}>
            Giriş Yap
          </Button>
        </form>

        <p className="mt-5 text-center text-sm text-slate-400">
          Hesabın yok mu?{' '}
          <Link href="/register" className="font-medium text-accent-blue hover:underline">
            Kayıt ol
          </Link>
        </p>
      </section>
    </main>
  )
}
