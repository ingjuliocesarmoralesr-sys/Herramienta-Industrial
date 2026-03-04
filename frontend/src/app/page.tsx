"use client";

import { useEffect, useState } from "react";

import TrendTable from "@/components/TrendTable";
import { exportCsvUrl, fetchDashboard, fetchIdeas, fetchSearch, SavedIdea, Trend } from "@/lib/api";

export default function HomePage() {
  const [keyword, setKeyword] = useState("ai");
  const [searchResults, setSearchResults] = useState<Trend[]>([]);
  const [dashboard, setDashboard] = useState<Trend[]>([]);
  const [ideas, setIdeas] = useState<SavedIdea[]>([]);
  const [loading, setLoading] = useState(false);

  async function loadDashboard() {
    const [dash, saved] = await Promise.all([fetchDashboard(), fetchIdeas()]);
    setDashboard(dash);
    setIdeas(saved);
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  return (
    <main style={{ fontFamily: "Arial, sans-serif", margin: "0 auto", maxWidth: 1100, padding: 20 }}>
      <h1>ViralTrendFinder</h1>
      <p>Find trending content from Reddit API, YouTube Data API, and Google News RSS feeds.</p>

      <section style={{ marginBottom: 24 }}>
        <h2>1) Search keywords</h2>
        <form
          onSubmit={async (event) => {
            event.preventDefault();
            setLoading(true);
            try {
              setSearchResults(await fetchSearch(keyword));
            } finally {
              setLoading(false);
            }
          }}
        >
          <input value={keyword} onChange={(e) => setKeyword(e.target.value)} placeholder="Search keyword" />
          <button type="submit" disabled={loading}>{loading ? "Searching..." : "Search"}</button>
        </form>
        {searchResults.length > 0 && <TrendTable items={searchResults.slice(0, 15)} onSaved={loadDashboard} />}
      </section>

      <section style={{ marginBottom: 24 }}>
        <h2>2) Trending dashboard + 3) Viral score ranking</h2>
        <TrendTable items={dashboard.slice(0, 15)} onSaved={loadDashboard} />
      </section>

      <section style={{ marginBottom: 24 }}>
        <h2>4) Save ideas + 5) Export CSV</h2>
        <a href={exportCsvUrl()} target="_blank">Export saved ideas as CSV</a>
        <ul>
          {ideas.map((idea) => (
            <li key={idea.id}>
              [{idea.source}] {idea.title} (score: {idea.viral_score})
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>6) Daily alerts</h2>
        <p>
          Daily alerts are scheduled by the backend scheduler (APScheduler cron) at 09:00 server time.
          Plug in email/Slack delivery in <code>backend/app/alerts.py</code>.
        </p>
      </section>

      <p><strong>Policy:</strong> No Facebook/Instagram scraping. Uses only public APIs and RSS.</p>
    </main>
  );
}
