import type { ReactNode } from "react";
import Link from "next/link";
import { ArrowRight, Sparkles, Mail, Shield, Gauge, Layers, Zap, BookOpen, Cloud } from "lucide-react";
import type { Section, SectionCta, Site } from "@/lib/api";

const ICONS: Record<string, typeof Sparkles> = {
  sparkles: Sparkles,
  mail: Mail,
  shield: Shield,
  gauge: Gauge,
  layers: Layers,
  zap: Zap,
  book: BookOpen,
  cloud: Cloud
};

function SectionIcon({ name, color }: { name?: string; color?: string }) {
  const Cmp = (name && ICONS[name]) || Sparkles;
  return <Cmp size={24} strokeWidth={1.8} color={color || "var(--color-primary)"} />;
}

function HeroActions({ cta, secondaryCta }: { cta?: SectionCta; secondaryCta?: SectionCta }) {
  if (!cta?.label && !secondaryCta?.label) return null;
  return (
    <div className="hero-actions">
      {cta?.label && (
        <Link className="button secondary" href={cta.href || "#"}>
          {cta.label} <ArrowRight size={16} />
        </Link>
      )}
      {secondaryCta?.label && (
        <Link className="button ghost" href={secondaryCta.href || "#"}>
          {secondaryCta.label}
        </Link>
      )}
    </div>
  );
}

function SectionHead({ heading, subhead }: { heading?: string; subhead?: string }) {
  if (!heading && !subhead) return null;
  return (
    <div className="section-head">
      {heading && <h2>{heading}</h2>}
      {subhead && <p className="lede">{subhead}</p>}
    </div>
  );
}

function Hero({ section, site }: { section: Section; site: Site }) {
  const c = section.content ?? {};
  const variant = section.variant || "split";
  const headline = c.headline || site.name;
  const copy = (
    <div className="hero-copy">
      {c.badge ? <span className="hero-badge">{c.badge}</span> : <p className="kicker">{c.kicker || site.industry}</p>}
      <h1>
        {headline}
        {c.headlineAccent && (
          <>
            <br />
            <span className="accent-text">{c.headlineAccent}</span>
          </>
        )}
      </h1>
      {c.subhead && <p className="lede">{c.subhead}</p>}
      <HeroActions cta={c.cta} secondaryCta={c.secondaryCta} />
    </div>
  );
  if (variant === "centered") return <section className="hero hero-centered">{copy}</section>;
  if (variant === "fullbleed") return <section className="hero hero-fullbleed">{copy}</section>;
  return (
    <section className="hero hero-split">
      {copy}
      <div className="hero-visual" aria-hidden="true" />
    </section>
  );
}

function Stats({ section }: { section: Section }) {
  const items = section.content?.items ?? [];
  if (!items.length) return null;
  return (
    <section className="stats">
      {items.map((item, index) => (
        <div className="stat" key={index}>
          <span className="stat-value">{item.value}</span>
          <span className="stat-label">{item.label}</span>
        </div>
      ))}
    </section>
  );
}

function Logos({ section }: { section: Section }) {
  const c = section.content ?? {};
  const items = c.items ?? [];
  if (!items.length) return null;
  return (
    <section className="logos">
      {c.heading && <p className="logos-heading">{c.heading}</p>}
      <div className="logos-row">
        {items.map((item, index) => (
          <span className="logo-chip" key={index}>
            {item.label}
          </span>
        ))}
      </div>
    </section>
  );
}

function Features({ section }: { section: Section }) {
  const c = section.content ?? {};
  const items = c.items ?? [];
  const minimal = section.variant === "minimal";
  return (
    <section className="section">
      <SectionHead heading={c.heading} subhead={c.subhead} />
      <div className={minimal ? "feature-grid" : "grid"}>
        {items.map((item, index) => (
          <div className={minimal ? "feature" : "post-card"} key={index}>
            <SectionIcon name={item.icon} />
            <h3>{item.title}</h3>
            <p>{item.body}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function Problem({ section }: { section: Section }) {
  const c = section.content ?? {};
  const items = c.items ?? [];
  return (
    <section className="section">
      <SectionHead heading={c.heading} subhead={c.subhead} />
      <div className="grid">
        {items.map((item, index) => (
          <div className="post-card problem-card" key={index}>
            <SectionIcon name={item.icon} color="var(--color-accent)" />
            <h3>{item.title}</h3>
            <p>{item.body}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function Comparison({ section }: { section: Section }) {
  const c = section.content ?? {};
  const left = c.left ?? {};
  const right = c.right ?? {};
  return (
    <section className="section">
      <SectionHead heading={c.heading} subhead={c.subhead} />
      <div className="compare">
        <div className="compare-col">
          <h3>{left.title}</h3>
          <ul>{(left.items ?? []).map((t, i) => <li key={i}>{t}</li>)}</ul>
        </div>
        <div className="compare-col featured">
          <h3>{right.title}</h3>
          <ul>{(right.items ?? []).map((t, i) => <li key={i}>{t}</li>)}</ul>
        </div>
      </div>
    </section>
  );
}

function Testimonials({ section }: { section: Section }) {
  const c = section.content ?? {};
  const items = c.items ?? [];
  return (
    <section className="section">
      <SectionHead heading={c.heading} subhead={c.subhead} />
      <div className="grid">
        {items.map((item, index) => (
          <figure className="post-card quote-card" key={index}>
            <blockquote>{item.quote}</blockquote>
            <figcaption>
              <strong>{item.author}</strong>
              {item.role && <span>{item.role}</span>}
            </figcaption>
          </figure>
        ))}
      </div>
    </section>
  );
}

function Pricing({ section }: { section: Section }) {
  const c = section.content ?? {};
  const items = c.items ?? [];
  return (
    <section className="section">
      <SectionHead heading={c.heading} subhead={c.subhead} />
      <div className="grid">
        {items.map((item, index) => (
          <div className={`post-card price-card${item.featured ? " featured" : ""}`} key={index}>
            <h3>{item.name}</h3>
            <div className="price">
              <span className="price-value">{item.price}</span>
              {item.period && <span className="price-period">{item.period}</span>}
            </div>
            <ul className="price-features">{(item.features ?? []).map((f, i) => <li key={i}>{f}</li>)}</ul>
            {item.cta?.label && (
              <Link className={item.featured ? "button secondary" : "button ghost"} href={item.cta.href || "#"}>
                {item.cta.label}
              </Link>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}

function Faq({ section }: { section: Section }) {
  const c = section.content ?? {};
  const items = c.items ?? [];
  return (
    <section className="section">
      <SectionHead heading={c.heading} subhead={c.subhead} />
      <div className="faq">
        {items.map((item, index) => (
          <details className="faq-item" key={index}>
            <summary>{item.q}</summary>
            <p>{item.a}</p>
          </details>
        ))}
      </div>
    </section>
  );
}

function Cta({ section }: { section: Section }) {
  const c = section.content ?? {};
  return (
    <section className="cta-banner">
      <div className="cta-copy">
        {c.headline && <h2>{c.headline}</h2>}
        {c.subhead && <p className="lede">{c.subhead}</p>}
      </div>
      {c.cta?.label && (
        <Link className="button secondary" href={c.cta.href || "#"}>
          {c.cta.label} <ArrowRight size={16} />
        </Link>
      )}
    </section>
  );
}

const RENDERERS: Record<string, (s: Section, site: Site) => ReactNode> = {
  hero: (s, site) => <Hero section={s} site={site} />,
  stats: (s) => <Stats section={s} />,
  logos: (s) => <Logos section={s} />,
  features: (s) => <Features section={s} />,
  problem: (s) => <Problem section={s} />,
  comparison: (s) => <Comparison section={s} />,
  testimonials: (s) => <Testimonials section={s} />,
  pricing: (s) => <Pricing section={s} />,
  faq: (s) => <Faq section={s} />,
  cta: (s) => <Cta section={s} />
};

export function SectionRenderer({ sections, site }: { sections: Section[]; site: Site }) {
  return (
    <>
      {sections.map((section, index) => {
        const render = RENDERERS[section.type];
        return render ? <div key={index}>{render(section, site)}</div> : null;
      })}
    </>
  );
}
