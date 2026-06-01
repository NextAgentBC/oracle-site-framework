import type { Metadata } from "next";
import Link from "next/link";
import { ContactForm } from "./ui";
import { alternatesFor, loadMessages, normalizeLocale, t } from "@/lib/i18n";

export async function generateMetadata({ params }: { params: Promise<{ locale: string }> }): Promise<Metadata> {
  const { locale: raw } = await params;
  const locale = normalizeLocale(raw);
  const messages = await loadMessages(locale);
  return {
    title: t(messages, "meta.contact"),
    description: t(messages, "contact.lede"),
    alternates: alternatesFor(locale, "/contact")
  };
}

export default async function ContactPage({ params }: { params: Promise<{ locale: string }> }) {
  const { locale: raw } = await params;
  const locale = normalizeLocale(raw);
  const messages = await loadMessages(locale);

  return (
    <main className="main">
      <header className="page-header">
        <p className="kicker">{t(messages, "contact.kicker")}</p>
        <h1>{t(messages, "contact.title")}</h1>
        <p className="lede">{t(messages, "contact.lede")}</p>
      </header>
      <div className="contact-layout">
        <div className="panel">
          <ContactForm
            labels={{
              emailPlaceholder: t(messages, "contactForm.emailPlaceholder"),
              messagePlaceholder: t(messages, "contactForm.messagePlaceholder"),
              send: t(messages, "contactForm.send"),
              sending: t(messages, "contactForm.sending"),
              sent: t(messages, "contactForm.sent"),
              failed: t(messages, "contactForm.failed")
            }}
          />
        </div>
        <aside className="contact-aside">
          <div className="contact-point">
            <h3>{t(messages, "contact.responseTitle")}</h3>
            <p className="muted">{t(messages, "contact.responseBody")}</p>
          </div>
          <div className="contact-point">
            <h3>{t(messages, "contact.newsletterTitle")}</h3>
            <p className="muted">{t(messages, "contact.newsletterBody")}</p>
          </div>
          <div className="contact-point">
            <h3>{t(messages, "contact.blogTitle")}</h3>
            <p className="muted">
              <Link href={`/${locale}/blog`}>{t(messages, "contact.blogBody")}</Link>
            </p>
          </div>
        </aside>
      </div>
    </main>
  );
}
