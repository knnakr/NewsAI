interface CategoryHeaderProps {
  category: string
}

const CATEGORY_TEXT: Record<string, { title: string; description: string }> = {
  sports: {
    title: 'Sports Central',
    description: 'Latest stories, match analysis, and key moments from global sports.',
  },
  technology: {
    title: 'Technology Horizon',
    description: 'AI, chips, startups, and breakthroughs shaping the future of technology.',
  },
  world: {
    title: 'World News',
    description: 'Top headlines and geopolitical updates from around the world.',
  },
  economy: {
    title: 'Economy Watch',
    description: 'Markets, inflation, and policy developments that move the global economy.',
  },
}

export function CategoryHeader({ category }: CategoryHeaderProps) {
  const content = CATEGORY_TEXT[category] ?? {
    title: `${category.charAt(0).toUpperCase()}${category.slice(1)} News`,
    description: 'Curated articles for this category.',
  }

  return (
    <div>
      <h1 className="mb-2 text-4xl font-bold text-text-primary">{content.title}</h1>
      <p className="text-text-secondary">{content.description}</p>
    </div>
  )
}