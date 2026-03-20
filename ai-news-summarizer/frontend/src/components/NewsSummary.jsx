export default function NewsSummary({ summary, articles }) {
  return (
    <div className="w-full max-w-3xl space-y-6">
      {/* Summary Section */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-3">News Summary</h2>
        <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{summary}</p>
      </div>

      {/* Sources Section */}
      {articles && articles.length > 0 && (
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-3">Sources</h2>
          <ul className="space-y-3">
            {articles.map((article, i) => (
              <li key={i} className="border-b border-gray-100 pb-3 last:border-0 last:pb-0">
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline font-medium"
                >
                  {article.title || article.url}
                </a>
                {article.published_date && (
                  <span className="ml-2 text-xs text-gray-400">{article.published_date}</span>
                )}
                {article.content && (
                  <p className="text-gray-500 text-sm mt-1 line-clamp-2">{article.content}</p>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
