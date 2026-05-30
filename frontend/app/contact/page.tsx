import { ContactForm } from "./ui";

export default function ContactPage() {
  return (
    <main className="main">
      <section className="section" style={{ marginTop: 0 }}>
        <h2>Contact</h2>
        <div className="panel">
          <ContactForm />
        </div>
      </section>
    </main>
  );
}

