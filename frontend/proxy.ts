import { NextRequest, NextResponse } from "next/server";

const LOCALES = (process.env.NEXT_PUBLIC_SITE_LOCALES || "en,zh")
  .split(",")
  .map((s) => s.trim())
  .filter(Boolean);
const DEFAULT_LOCALE = process.env.NEXT_PUBLIC_DEFAULT_LOCALE || LOCALES[0] || "en";

function hasLocalePrefix(pathname: string): boolean {
  return LOCALES.some((l) => pathname === `/${l}` || pathname.startsWith(`/${l}/`));
}

function detectLocale(req: NextRequest): string {
  const cookie = req.cookies.get("locale")?.value;
  if (cookie && LOCALES.includes(cookie)) return cookie;
  const accept = req.headers.get("accept-language") || "";
  for (const part of accept.split(",")) {
    const code = part.split(";")[0].trim().toLowerCase();
    const base = code.split("-")[0];
    const hit = LOCALES.find((l) => l === code || l === base);
    if (hit) return hit;
  }
  return DEFAULT_LOCALE;
}

export function proxy(req: NextRequest) {
  const { pathname } = req.nextUrl;
  // Already localized: remember it so bare links (e.g. a block's "/contact")
  // resolve back to the same language on the next request.
  if (hasLocalePrefix(pathname)) {
    const res = NextResponse.next();
    res.cookies.set("locale", pathname.split("/")[1], { path: "/", sameSite: "lax" });
    return res;
  }
  const locale = detectLocale(req);
  const url = req.nextUrl.clone();
  url.pathname = `/${locale}${pathname === "/" ? "" : pathname}`;
  const res = NextResponse.redirect(url);
  res.cookies.set("locale", locale, { path: "/", sameSite: "lax" });
  return res;
}

export const config = {
  // Skip API, Next internals, and any file with an extension (sitemap.xml,
  // robots.txt, favicon, static assets all pass through untouched).
  matcher: ["/((?!api|_next|.*\\..*).*)"]
};
