import Link from 'next/link'

import { Button } from '@/components/ui/Button'

export default function NotFoundPage() {
  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4 py-12">
      <div className="w-full max-w-lg rounded-xl border border-navy-700 bg-navy-800 p-8 text-center">
        <p className="text-sm font-semibold uppercase tracking-wide text-accent-blue">404</p>
        <h1 className="mt-3 text-3xl font-bold text-text-primary">Sayfa bulunamadi</h1>
        <p className="mt-3 text-text-secondary">Aradiginiz sayfa mevcut degil ya da tasinmis olabilir.</p>
        <div className="mt-6 flex justify-center">
          <Link href="/chat">
            <Button type="button" variant="secondary">
              Sohbete don
            </Button>
          </Link>
        </div>
      </div>
    </div>
  )
}
