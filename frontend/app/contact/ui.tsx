"use client";

import { FormEvent, useState } from "react";
import { Send } from "lucide-react";
import { postJson } from "@/lib/api";

export function ContactForm() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus("Sending...");
    try {
      await postJson("/contact", { email, message });
      setEmail("");
      setMessage("");
      setStatus("Message sent.");
    } catch {
      setStatus("Message failed. Check API configuration.");
    }
  }

  return (
    <form className="stack" onSubmit={submit}>
      <input className="input" type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@example.com" required />
      <textarea className="textarea" value={message} onChange={(event) => setMessage(event.target.value)} placeholder="Message" required />
      <button className="button" type="submit">
        <Send size={16} />
        Send
      </button>
      {status ? <p className="muted">{status}</p> : null}
    </form>
  );
}

