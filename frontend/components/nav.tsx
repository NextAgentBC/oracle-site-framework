"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { t, langLabel, type Messages } from "@/lib/i18n";

type NavPage = { slug: string; navLabel: string };

export function SiteNav({
  siteName,
  pages = [],
  locale,
  locales,
  messages
}: {
  siteName: string;
  pages?: NavPage[];
  locale: string;
  locales: string[];
  messages: Messages;
}) {
  const [open, setOpen] = useState(false);
  const close = () => setOpen(false);
  const pathname = usePathname() || `/${locale}`;
  // The path with the current locale prefix stripped, so the language toggle
  // can rebuild the same page under another locale.
  const rest = pathname.replace(new RegExp(`^/${locale}(?=/|$)`), "");

  const staticLinks = [
    { href: `/${locale}/blog`, label: t(messages, "nav.blog") },
    { href: `/${locale}/contact`, label: t(messages, "nav.contact") }
  ];

  return (
    <header className="topbar">
      <Link className="brand" href={`/${locale}`} onClick={close}>
        <span className="mark" />
        <span>{siteName}</span>
      </Link>

      <button
        type="button"
        className="nav-toggle"
        aria-label={t(messages, "nav.menu")}
        aria-expanded={open}
        aria-controls="primary-nav"
        onClick={() => setOpen((value) => !value)}
      >
        <span className="nav-toggle-bar" />
        <span className="nav-toggle-bar" />
        <span className="nav-toggle-bar" />
      </button>

      <nav id="primary-nav" className={open ? "nav is-open" : "nav"} aria-label="Main navigation">
        {pages.map((page) => (
          <Link key={page.slug} href={`/${locale}/${page.slug}`} onClick={close}>
            {page.navLabel}
          </Link>
        ))}
        {staticLinks.map((link) => (
          <Link key={link.href} href={link.href} onClick={close}>
            {link.label}
          </Link>
        ))}
        {locales.length > 1 && (
          <span className="nav-langs" role="group" aria-label="Language">
            {locales.map((l) => (
              <Link
                key={l}
                href={`/${l}${rest}`}
                className={`nav-lang${l === locale ? " is-active" : ""}`}
                onClick={close}
                hrefLang={l}
              >
                {langLabel(l)}
              </Link>
            ))}
          </span>
        )}
      </nav>
    </header>
  );
}
