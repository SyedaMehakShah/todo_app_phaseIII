"use client";

import { useState, useEffect, useCallback } from "react";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";
import { sendChatMessage, getConversationHistory } from "../lib/api";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

interface ChatProps {
  userId: string;
  token: string;
}

export default function Chat({ userId, token }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load conversation history on mount
  useEffect(() => {
    const loadHistory = async () => {
      try {
        const history = await getConversationHistory(userId, token);
        if (history.messages) {
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
      }
    };

    if (userId && token) {
      loadHistory();
    }
  }, [userId, token]);

  const handleSend = useCallback(
    async (message: string) => {
      if (!userId || !token) return;

      // Add user message optimistically
      const userMessage: Message = {
        id: Date.now().toString(),
        role: "user",
        content: message,
      };
      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);
      setError(null);

      try {
        const response = await sendChatMessage(userId, message, token);

        // Add assistant response
        const assistantMessage: Message = {
          id: Date.now().toString() + "-assistant",
          role: "assistant",
          content: response.message,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to send message");

        // Add error message
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
    [userId, token]
  );

  return (
    <div className="flex flex-col h-full">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-4xl mx-auto">
          <MessageList messages={messages} isLoading={isLoading} />
        </div>
      </div>

      {/* Error display */}
      {error && (
        <div className="px-4 py-2 bg-red-900/50 text-red-200 text-sm text-center">
          {error}
        </div>
      )}

      {/* Input area */}
      <div className="border-t border-gray-800 p-4">
        <div className="max-w-4xl mx-auto">
          <MessageInput onSend={handleSend} disabled={isLoading} />
        </div>
      </div>
    </div>
  );
}
