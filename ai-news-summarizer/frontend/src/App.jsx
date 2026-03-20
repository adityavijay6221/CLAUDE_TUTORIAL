import { useState } from "react";
import SearchBar from "./components/SearchBar";
import NewsSummary from "./components/NewsSummary";
import ChatBox from "./components/ChatBox";
import { summarizeNews, askFollowup } from "./api/newsApi";

export default function App() {
  const [summary, setSummary] = useState(null);
  const [articles, setArticles] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [searchLoading, setSearchLoading] = useState(false);
  const [qaLoading, setQaLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSearch(topic) {
    setSearchLoading(true);
    setError(null);
    setSummary(null);
    setArticles([]);
    setSessionId(null);

    try {
      const data = await summarizeNews(topic);
      setSummary(data.summary);
      setArticles(data.articles);
      setSessionId(data.session_id);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to fetch news. Please try again.");
    } finally {
      setSearchLoading(false);
    }
  }

  async function handleAsk(question) {
    if (!sessionId) return null;
    setQaLoading(true);
    try {
      const data = await askFollowup(question, sessionId);
      return data.answer;
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to get answer. Please try again.");
      return null;
    } finally {
      setQaLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-5">
          <h1 className="text-3xl font-bold text-blue-700">AI News Summarizer</h1>
          <p className="text-gray-500 mt-1">Search any topic and get an AI-powered news summary</p>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8 flex flex-col items-center gap-8">
        {/* Search */}
        <SearchBar onSearch={handleSearch} loading={searchLoading} />

        {/* Error */}
        {error && (
          <div className="w-full max-w-2xl bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {/* Loading Skeleton */}
        {searchLoading && (
          <div className="w-full max-w-3xl bg-white rounded-xl shadow-md p-6 animate-pulse">
            <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
            <div className="space-y-2">
              <div className="h-4 bg-gray-200 rounded w-full"></div>
              <div className="h-4 bg-gray-200 rounded w-5/6"></div>
              <div className="h-4 bg-gray-200 rounded w-4/6"></div>
            </div>
          </div>
        )}

        {/* Results */}
        {summary && !searchLoading && (
          <>
            <NewsSummary summary={summary} articles={articles} />
            <ChatBox onAsk={handleAsk} loading={qaLoading} />
          </>
        )}
      </main>
    </div>
  );
}
