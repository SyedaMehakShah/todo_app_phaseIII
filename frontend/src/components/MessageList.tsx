"use client";

import { useEffect, useRef } from "react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

interface MessageListProps {
  messages: Message[];
  isLoading?: boolean;
}

export default function MessageList({
  messages,
  isLoading = false,
}: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="text-center text-gray-500 py-12">
        <p className="text-lg mb-2">Welcome to your AI Todo Assistant!</p>
        <p className="text-sm">
          Try saying things like &quot;Add a task to buy groceries&quot; or
          &quot;Show my tasks&quot;
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {messages.map((message) => (
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
            <div className="whitespace-pre-wrap">{message.content}</div>
          </div>
        </div>
      ))}

      {isLoading && (
        <div className="flex justify-start">
          <div className="bg-gray-800 text-gray-400 rounded-lg px-4 py-2">
            <span className="animate-pulse">Thinking...</span>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}
