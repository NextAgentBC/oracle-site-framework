"use client";

import { Send } from "lucide-react";
import { FormEvent, useState } from "react";
import { postJson } from "@/lib/api";

type Labels = {
  placeholder?: string;
  button?: string;
  subscribing?: string;
  subscribed?: string;
  failed?: string;
  emailAria?: string;
};

export function NewsletterForm({ labels = {} }: { labels?: Labels }) {
  const l = {
    placeholder: "you@example.com",
    button: "Subscribe",
    subscribing: "Subscribing...",
    subscribed: "Subscribed. Check your inbox if email is configured.",
    failed: "Subscription failed. Check the API logs.",
    emailAria: "Email address",
    ...labels
  };
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage(l.subscribing);
    try {
      await postJson("/newsletter/subscribe", { email });
      setEmail("");
      setMessage(l.subscribed);
    } catch {
      setMessage(l.failed);
    }
  }

  return (
    <form className="form-row" onSubmit={submit}>
      <input
        className="input"
        type="email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
        placeholder={l.placeholder}
        aria-label={l.emailAria}
        required
      />
      <button className="button secondary" type="submit">
        <Send size={16} />
        {l.button}
      </button>
      {message ? <p className="muted">{message}</p> : null}
    </form>
  );
}
