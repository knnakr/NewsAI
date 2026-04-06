"use client";

import { FormEvent, useState } from "react";
import { toast } from "sonner";

import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { api } from "@/lib/api";
import { useAuthStore } from "@/stores/authStore";

type AITone = "Neutral" | "Formal" | "Casual";
type Language = "TR" | "EN";

const AVAILABLE_CATEGORIES = ["world", "economy", "sports", "technology"];

export default function SettingsPage() {
	const user = useAuthStore((state) => state.user);
	const setUser = useAuthStore((state) => state.setUser);

	const [displayName, setDisplayName] = useState(user?.display_name ?? "");
	const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
	const [language, setLanguage] = useState<Language>("TR");
	const [aiTone, setAiTone] = useState<AITone>("Neutral");
	const [emailDigestEnabled, setEmailDigestEnabled] = useState(false);
	const [isSaving, setIsSaving] = useState(false);

	const toggleCategory = (category: string) => {
		setSelectedCategories((prev) =>
			prev.includes(category) ? prev.filter((item) => item !== category) : [...prev, category],
		);
	};

	const handleSave = async (event: FormEvent<HTMLFormElement>) => {
		event.preventDefault();

		setIsSaving(true);
		const normalizedDisplayName = displayName.trim() || user?.display_name || "User";

		try {
			await api.patch("/users/me", {
				display_name: normalizedDisplayName,
			});

			await api.patch("/users/me/preferences", {
				categories: selectedCategories,
				language,
				ai_tone: aiTone,
				email_digest: emailDigestEnabled,
			});

			if (user) {
				setUser({
					...user,
					display_name: normalizedDisplayName,
				});
			}

			toast.success("Ayarlar kaydedildi.");
		} catch {
			toast.error("Ayarlar kaydedilirken bir hata oluştu.");
		} finally {
			setIsSaving(false);
		}
	};

	return (
		<div className="min-h-full bg-navy-900 px-4 py-6 md:px-8">
			<div className="mx-auto max-w-5xl space-y-6">
				<div>
					<h1 className="text-2xl font-semibold text-slate-100">Settings</h1>
					<p className="mt-1 text-sm text-slate-400">Profil bilgilerini ve AI tercihlerini yonet.</p>
				</div>

				<form onSubmit={handleSave} className="space-y-6">
					<section className="rounded-xl border border-navy-600 bg-navy-800 p-5">
						<h2 className="text-lg font-medium text-slate-100">Profil</h2>
						<p className="mt-1 text-sm text-slate-400">Gorunen adini guncelleyebilirsin.</p>
						<div className="mt-4 max-w-md">
							<Input
								label="Display Name"
								name="display_name"
								value={displayName}
								onChange={(event) => setDisplayName(event.target.value)}
							/>
						</div>
					</section>

					<section className="rounded-xl border border-navy-600 bg-navy-800 p-5">
						<h2 className="text-lg font-medium text-slate-100">Tercihler</h2>
						<p className="mt-1 text-sm text-slate-400">Hangi haberleri ve nasil bir AI tonunu tercih ettigini sec.</p>

						<div className="mt-5 space-y-5">
							<div>
								<p className="mb-2 text-sm font-medium text-slate-200">Kategori Secimi</p>
								<div className="flex flex-wrap gap-2">
									{AVAILABLE_CATEGORIES.map((category) => {
										const isSelected = selectedCategories.includes(category);
										return (
											<button
												key={category}
												type="button"
												onClick={() => toggleCategory(category)}
												aria-pressed={isSelected}
												className={`rounded-full border px-3 py-1.5 text-sm capitalize transition-colors ${
													isSelected
														? "border-accent-blue bg-accent-blue/20 text-accent-blue"
														: "border-navy-500 bg-navy-700 text-slate-200 hover:border-navy-400"
												}`}
											>
												{category}
											</button>
										);
									})}
								</div>
							</div>

							<div className="grid gap-4 md:grid-cols-2">
								<div>
									<label htmlFor="language" className="mb-1 block text-sm font-medium text-slate-200">
										Language
									</label>
									<select
										id="language"
										name="language"
										value={language}
										onChange={(event) => setLanguage(event.target.value as Language)}
										className="h-10 w-full rounded-lg border border-navy-600 bg-navy-700 px-3 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-accent-blue"
									>
										<option value="TR">TR</option>
										<option value="EN">EN</option>
									</select>
								</div>

								<div>
									<label htmlFor="ai-tone" className="mb-1 block text-sm font-medium text-slate-200">
										AI Tone
									</label>
									<select
										id="ai-tone"
										name="ai_tone"
										value={aiTone}
										onChange={(event) => setAiTone(event.target.value as AITone)}
										className="h-10 w-full rounded-lg border border-navy-600 bg-navy-700 px-3 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-accent-blue"
									>
										<option value="Neutral">Neutral</option>
										<option value="Formal">Formal</option>
										<option value="Casual">Casual</option>
									</select>
								</div>
							</div>

							<div className="flex items-center justify-between rounded-lg border border-navy-600 bg-navy-700 px-4 py-3">
								<div>
									<p className="text-sm font-medium text-slate-100">Email Digest</p>
									<p className="text-xs text-slate-400">Gunluk haber ozetlerini e-posta ile al.</p>
								</div>
								<label className="inline-flex items-center gap-2 text-sm text-slate-200">
									<input
										type="checkbox"
										checked={emailDigestEnabled}
										onChange={(event) => setEmailDigestEnabled(event.target.checked)}
										className="h-4 w-4 rounded border-navy-500 bg-navy-800 text-accent-blue focus:ring-accent-blue"
									/>
									Açık
								</label>
							</div>
						</div>
					</section>

					<section className="rounded-xl border border-red-500/40 bg-red-950/20 p-5">
						<h2 className="text-lg font-medium text-red-300">Danger Zone</h2>
						<p className="mt-1 text-sm text-red-200/80">Hesabini kalici olarak silmek geri alinamaz.</p>
						<Button type="button" variant="danger" className="mt-4">
							Hesabi Sil
						</Button>
					</section>

					<div className="flex justify-end">
						<Button type="submit" loading={isSaving}>
							Degisiklikleri Kaydet
						</Button>
					</div>
				</form>
			</div>
		</div>
	);
}
