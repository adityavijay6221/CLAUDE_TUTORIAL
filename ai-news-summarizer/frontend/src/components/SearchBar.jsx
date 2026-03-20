import { useState } from "react";

export default function SearchBar({ onSearch, loading }) {
  const [topic, setTopic] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (topic.trim()) {
      onSearch(topic.trim());
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 w-full max-w-2xl">
      <input
        type="text"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Enter a news topic (e.g. AI, climate change, elections...)"
        disabled={loading}
        className="flex-1 px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800 disabled:bg-gray-100"
      />
      <button
        type="submit"
        disabled={loading || !topic.trim()}
        className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? "Searching..." : "Search"}
      </button>
    </form>
  );
}
