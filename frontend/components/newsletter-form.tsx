"use client";

import { Send } from "lucide-react";
import { FormEvent, useState } from "react";
import { postJson } from "@/lib/api";

export function NewsletterForm() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("Subscribing...");
    try {
      await postJson("/newsletter/subscribe", { email });
      setEmail("");
      setMessage("Subscribed. Check your inbox if email is configured.");
    } catch {
      setMessage("Subscription failed. Check the API logs.");
    }
  }

  return (
    <form className="form-row" onSubmit={submit}>
      <input
        className="input"
        type="email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
        placeholder="you@example.com"
        aria-label="Email address"
        required
      />
      <button className="button secondary" type="submit">
        <Send size={16} />
        Subscribe
      </button>
      {message ? <p className="muted">{message}</p> : null}
    </form>
  );
}

