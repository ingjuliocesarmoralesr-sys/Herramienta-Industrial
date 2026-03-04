"use client";

import { saveIdea, Trend } from "@/lib/api";

type Props = {
  items: Trend[];
  onSaved?: () => void;
};

export default function TrendTable({ items, onSaved }: Props) {
  return (
    <div>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>Title</th>
            <th>Source</th>
            <th>Keyword</th>
            <th>Viral score</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={`${item.source}-${item.url}`}>
              <td><a href={item.url} target="_blank">{item.title}</a></td>
              <td>{item.source}</td>
              <td>{item.keyword}</td>
              <td>{item.viral_score}</td>
              <td>
                <button
                  onClick={async () => {
                    await saveIdea({
                      title: item.title,
                      source: item.source,
                      keyword: item.keyword,
                      url: item.url,
                      viral_score: item.viral_score
                    });
                    onSaved?.();
                  }}
                >
                  Save idea
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
