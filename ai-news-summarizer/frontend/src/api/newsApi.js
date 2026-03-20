import axios from "axios";

const BASE_URL = "http://localhost:8000";

export async function summarizeNews(topic) {
  const response = await axios.post(`${BASE_URL}/api/summarize`, { topic });
  return response.data; // { summary, articles, session_id }
}

export async function askFollowup(question, sessionId) {
  const response = await axios.post(`${BASE_URL}/api/followup`, {
    question,
    session_id: sessionId,
  });
  return response.data; // { answer }
}
