import type { Metadata } from "next";
import Link from "next/link";
import { Inter, Space_Grotesk, Spectral } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "./providers";
import { getDesign, getSite, getPages } from "@/lib/api";
import { designCssVariables } from "@/lib/design";
import { SiteNav } from "@/components/nav";
import type { DesignProfile } from "@/lib/api";

// Content (pages, blog, nav) is DB-driven and must reflect changes immediately,
// so render dynamically per request instead of statically prerendering at build.
// This also keeps the build from prerendering routes that fetch the API.
export const dynamic = "force-dynamic";

// A small font palette loaded once; templates pick which face to use through
// their typography tokens (e.g. heading: "var(--font-display), serif").
const inter = Inter({ subsets: ["latin"], variable: "--font-sans", display: "swap" });
const grotesk = Space_Grotesk({ subsets: ["latin"], variable: "--font-grotesk", display: "swap", weight: ["400", "500", "600", "700"] });
const serif = Spectral({ subsets: ["latin"], variable: "--font-display", display: "swap", weight: ["400", "500", "600", "700"] });
const fontVars = `${inter.variable} ${grotesk.variable} ${serif.variable}`;

// Derive the two adaptive axes the stylesheet reads, straight from the active
// design profile — no extra API fields needed.
function hexLuminance(hex?: string): number | null {
  if (!hex) return null;
  let h = hex.trim().replace("#", "");
  if (h.length === 3) h = h.split("").map((c) => c + c).join("");
  if (h.length !== 6) return null;
  const r = parseInt(h.slice(0, 2), 16) / 255;
  const g = parseInt(h.slice(2, 4), 16) / 255;
  const b = parseInt(h.slice(4, 6), 16) / 255;
  if ([r, g, b].some((v) => Number.isNaN(v))) return null;
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
function deriveMode(design: DesignProfile): "light" | "dark" {
  const lum = hexLuminance(design.tokens?.colors?.paper);
  return lum !== null && lum < 0.4 ? "dark" : "light";
}
function deriveThemeFamily(design: DesignProfile): string {
  const src = design.source || "";
  const prefix = "style-preset:";
  if (src.startsWith(prefix)) return src.slice(prefix.length);
  return (design.industry || "default").toLowerCase();
}

export async function generateMetadata(): Promise<Metadata> {
  const site = await getSite();
  const article = /^[aeiou]/i.test(site.industry) ? "an" : "a";
  return {
    title: {
      default: site.name,
      template: `%s | ${site.name}`
    },
    description: `${article[0].toUpperCase()}${article.slice(1)} ${site.industry} website framework with daily blogs, newsletter, Google login, SEO, and GEO.`,
    metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || site.url),
    openGraph: {
      title: site.name,
      description: `Daily ${site.industry} insights for ${site.audience}.`,
      url: site.url,
      siteName: site.name,
      type: "website"
    }
  };
}

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const [site, design, pages] = await Promise.all([getSite(), getDesign(), getPages()]);
  const navPages = pages.filter((page) => page.showInNav).map((page) => ({ slug: page.slug, navLabel: page.navLabel }));
  return (
    <html lang="en" data-mode={deriveMode(design)} data-theme={deriveThemeFamily(design)} className={fontVars}>
      <body style={designCssVariables(design)}>
        <AuthProvider>
          <div className="shell">
            <SiteNav siteName={site.name} pages={navPages} />
            {children}
            <footer className="footer">
              <div className="footer-grid">
                <div className="footer-brand">
                  <span className="footer-brand-row">
                    <span className="mark" />
                    <strong>{site.name}</strong>
                  </span>
                  <p className="muted">
                    {site.industry} site built on the Oracle Site framework — Next.js, Flask, Cloudflare.
                  </p>
                </div>
                <nav className="footer-col" aria-label="Pages">
                  <h4>Pages</h4>
                  {navPages.map((page) => (
                    <Link href={`/${page.slug}`} key={page.slug}>
                      {page.navLabel}
                    </Link>
                  ))}
                </nav>
                <nav className="footer-col" aria-label="More">
                  <h4>More</h4>
                  <Link href="/blog">Blog</Link>
                  <Link href="/contact">Contact</Link>
                </nav>
              </div>
              <div className="footer-bottom">© {new Date().getFullYear()} {site.name}</div>
            </footer>
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
