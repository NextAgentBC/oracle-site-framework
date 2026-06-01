"use client";

import { FormEvent, useState } from "react";
import { Send } from "lucide-react";
import { postJson } from "@/lib/api";

type Labels = {
  emailPlaceholder?: string;
  messagePlaceholder?: string;
  send?: string;
  sending?: string;
  sent?: string;
  failed?: string;
};

export function ContactForm({ labels = {} }: { labels?: Labels }) {
  const l = {
    emailPlaceholder: "you@example.com",
    messagePlaceholder: "Message",
    send: "Send",
    sending: "Sending...",
    sent: "Message sent.",
    failed: "Message failed. Check API configuration.",
    ...labels
  };
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus(l.sending);
    try {
      await postJson("/contact", { email, message });
      setEmail("");
      setMessage("");
      setStatus(l.sent);
    } catch {
      setStatus(l.failed);
    }
  }

  return (
    <form className="stack" onSubmit={submit}>
      <input className="input" type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder={l.emailPlaceholder} required />
      <textarea className="textarea" value={message} onChange={(event) => setMessage(event.target.value)} placeholder={l.messagePlaceholder} required />
      <button className="button" type="submit">
        <Send size={16} />
        {l.send}
      </button>
      {status ? <p className="muted">{status}</p> : null}
    </form>
  );
}
