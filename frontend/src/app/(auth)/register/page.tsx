"use client"

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useEffect, useMemo, useState } from 'react'
import { toast } from 'sonner'

import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { useRegister } from '@/hooks/useAuth'

function isValidEmail(value: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
}

export default function RegisterPage() {
  const router = useRouter()
  const register = useRegister()

  const [displayName, setDisplayName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const [touched, setTouched] = useState({
    displayName: false,
    email: false,
    password: false,
  })

  const showDisplayNameError = submitted || touched.displayName
  const showEmailError = submitted || touched.email
  const showPasswordError = submitted || touched.password

  const displayNameError = useMemo(() => {
    if (!showDisplayNameError) return ''
    if (!displayName.trim()) return 'Display name boş olamaz'
    if (displayName.trim().length < 2) return 'Display name en az 2 karakter olmalı'
    return ''
  }, [displayName, showDisplayNameError])

  const emailError = useMemo(() => {
    if (!showEmailError) return ''
    if (!email.trim()) return 'Email boş olamaz'
    if (!isValidEmail(email)) return 'Geçerli bir email giriniz'
    return ''
  }, [email, showEmailError])

  const passwordError = useMemo(() => {
    if (!showPasswordError) return ''
    if (!password.trim()) return 'Şifre boş olamaz'
    if (password.length < 8) return 'Şifre en az 8 karakter olmalı'
    return ''
  }, [password, showPasswordError])

  const apiError = useMemo(() => {
    if (!register.isError) return ''
    const status = (register.error as { response?: { status?: number } })?.response?.status
    if (status === 409) return 'Bu email zaten kullanılıyor'
    return 'Kayıt işlemi başarısız oldu'
  }, [register.error, register.isError])

  useEffect(() => {
    if (register.isSuccess) {
      toast.success('Hoş geldin! Giriş yapabilirsin.')
      router.push('/login')
    }
  }, [register.isSuccess, router])

  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setSubmitted(true)

    const hasErrors =
      !displayName.trim() ||
      displayName.trim().length < 2 ||
      !email.trim() ||
      !isValidEmail(email) ||
      !password.trim() ||
      password.length < 8

    if (hasErrors) return

    register.mutate({
      display_name: displayName.trim(),
      email: email.trim(),
      password,
    })
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-navy-900 px-4">
      <section className="w-full max-w-md rounded-2xl border border-navy-600 bg-navy-800 p-6 shadow-lg">
        <div className="mb-6 text-center">
          <h1 className="text-2xl font-bold text-slate-100">News AI</h1>
          <p className="mt-1 text-sm text-slate-400">Yeni hesap oluşturun</p>
        </div>

        <form className="space-y-4" onSubmit={onSubmit} noValidate>
          <Input
            id="display-name"
            name="display_name"
            type="text"
            label="Display Name"
            placeholder="Adınızı girin"
            value={displayName}
            onChange={(event) => setDisplayName(event.target.value)}
            onBlur={() => setTouched((current) => ({ ...current, displayName: true }))}
            error={displayNameError}
          />

          <Input
            id="email"
            name="email"
            type="email"
            label="Email"
            placeholder="you@example.com"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            onBlur={() => setTouched((current) => ({ ...current, email: true }))}
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
              onBlur={() => setTouched((current) => ({ ...current, password: true }))}
              error={passwordError}
            />
            <div className="flex items-center justify-between">
              <p className="text-xs text-slate-400">En az 8 karakter ({password.length}/8)</p>
              <button
                type="button"
                className="text-xs text-slate-300 hover:text-slate-100"
                onClick={() => setShowPassword((current) => !current)}
              >
                {showPassword ? 'Şifreyi gizle' : 'Şifreyi göster'}
              </button>
            </div>
          </div>

          {apiError ? <p className="text-sm text-red-400">{apiError}</p> : null}

          <Button type="submit" className="w-full" loading={register.isPending}>
            Kayıt Ol
          </Button>
        </form>

        <p className="mt-5 text-center text-sm text-slate-400">
          Zaten hesabın var mı?{' '}
          <Link href="/login" className="font-medium text-accent-blue hover:underline">
            Giriş yap
          </Link>
        </p>
      </section>
    </main>
  )
}
