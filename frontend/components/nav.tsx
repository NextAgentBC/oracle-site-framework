"use client";

import { useState } from "react";
import Link from "next/link";

type NavPage = { slug: string; navLabel: string };

const STATIC_LINKS = [
  { href: "/blog", label: "Blog" },
  { href: "/contact", label: "Contact" }
];

export function SiteNav({ siteName, pages = [] }: { siteName: string; pages?: NavPage[] }) {
  const [open, setOpen] = useState(false);
  const close = () => setOpen(false);

  return (
    <header className="topbar">
      <Link className="brand" href="/" onClick={close}>
        <span className="mark" />
        <span>{siteName}</span>
      </Link>

      <button
        type="button"
        className="nav-toggle"
        aria-label="Toggle navigation menu"
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
          <Link key={page.slug} href={`/${page.slug}`} onClick={close}>
            {page.navLabel}
          </Link>
        ))}
        {STATIC_LINKS.map((link) => (
          <Link key={link.href} href={link.href} onClick={close}>
            {link.label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
