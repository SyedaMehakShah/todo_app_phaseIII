"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import ProtectedRoute from "../../components/ProtectedRoute";
import { sendChatMessage, getConversationHistory } from "../../lib/api";
import { getToken, getUserId, isAuthenticated } from "../../lib/auth-client";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

interface User {
  id: string;
  email: string;
  name?: string;
}

export default function ChatPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch user session and token on mount
  useEffect(() => {
    const fetchSession = () => {
      try {
        if (isAuthenticated()) {
          const userId = getUserId();
          const userEmail = localStorage.getItem('user_email');
          const jwtToken = getToken();

          if (userId && userEmail && jwtToken) {
            setUser({ id: userId, email: userEmail });
            setToken(jwtToken);
          }
        }
      } catch (err) {
        console.error("Failed to fetch session:", err);
        setError("Failed to load session. Please sign in again.");
      }
    };

    fetchSession();
  }, []);

  // Load conversation history when user and token are available
  useEffect(() => {
    const loadHistory = async () => {
      if (!user?.id || !token) {
        setIsLoadingHistory(false);
        return;
      }

      try {
        const history = await getConversationHistory(user.id, token);
        if (history.messages && history.messages.length > 0) {
          setMessages(
            history.messages.map((msg) => ({
              id: msg.id,
              role: msg.role as "user" | "assistant",
              content: msg.content,
            }))
          );
        }
      } catch (err) {
        console.error("Failed to load history:", err);
        // Don't show error for empty history
      } finally {
        setIsLoadingHistory(false);
      }
    };

    loadHistory();
  }, [user?.id, token]);

  const handleSignOut = async () => {
    try {
      await fetch("/api/auth/sign-out", { method: "POST" });
      router.push("/login");
    } catch (err) {
      console.error("Sign out failed:", err);
    }
  };

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      if (!input.trim() || isLoading || !user || !token) return;

      const userMessage: Message = {
        id: Date.now().toString(),
        role: "user",
        content: input.trim(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setInput("");
      setIsLoading(true);
      setError(null);

      try {
        const response = await sendChatMessage(user.id, userMessage.content, token);

        const assistantMessage: Message = {
          id: Date.now().toString() + "-assistant",
          role: "assistant",
          content: response.message,
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        console.error("Chat error:", err);
        const errorMsg = err instanceof Error ? err.message : "Failed to send message";
        setError(errorMsg);

        const errorMessage: Message = {
          id: Date.now().toString() + "-error",
          role: "assistant",
          content: "Sorry, something went wrong. Please try again.",
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    },
    [input, isLoading, user, token]
  );

  return (
    <ProtectedRoute>
      <div className="min-h-screen flex flex-col bg-gradient-to-br from-[#0A0A0A] to-[#1A1A1A]">
        {/* Header */}
        <header className="border-b border-gray-800 p-4">
          <div className="max-w-4xl mx-auto flex justify-between items-center">
            <h1 className="text-xl font-bold gradient-text">AI Todo Assistant</h1>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-400">{user?.email}</span>
              <button
                onClick={handleSignOut}
                className="text-sm text-gray-400 hover:text-white transition-colors"
              >
                Sign Out
              </button>
            </div>
          </div>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4">
          <div className="max-w-4xl mx-auto space-y-4">
            {isLoadingHistory ? (
              <div className="text-center text-gray-500 py-12">
                <div className="animate-pulse">Loading conversation history...</div>
              </div>
            ) : messages.length === 0 ? (
              <div className="text-center text-gray-500 py-12">
                <p className="text-lg mb-2">Welcome to your AI Todo Assistant!</p>
                <p className="text-sm">
                  Try saying things like &quot;Add a task to buy groceries&quot; or
                  &quot;Show my tasks&quot;
                </p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${
                    message.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-2 ${
                      message.role === "user"
                        ? "bg-gradient-to-r from-[#FF6B6B] to-[#4ECDC4] text-white"
                        : "bg-gray-800 text-gray-200"
                    }`}
                  >
                    {message.content}
                  </div>
                </div>
              ))
            )}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-800 text-gray-400 rounded-lg px-4 py-2">
                  <span className="animate-pulse">Thinking...</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Error display */}
        {error && (
          <div className="px-4 py-2 bg-red-900/50 text-red-200 text-sm text-center">
            {error}
          </div>
        )}

        {/* Input */}
        <div className="border-t border-gray-800 p-4">
          <form onSubmit={handleSubmit} className="max-w-4xl mx-auto flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a message... (e.g., 'Add task: buy milk')"
              className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#FF6B6B]"
              disabled={isLoading || !token}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim() || !token}
              className="bg-gradient-to-r from-[#FF6B6B] to-[#4ECDC4] text-white px-6 py-2 rounded-lg font-medium hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </ProtectedRoute>
  );
}
