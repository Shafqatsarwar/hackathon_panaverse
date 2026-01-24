"use client";

import { useState, useEffect, useRef } from "react";

export default function Home() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [input, setInput] = useState("");
  const [status, setStatus] = useState<any>(null);
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Fetch System Status
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/status");
        const data = await res.json();
        setStatus(data);
      } catch (e) {
        console.error("Failed to fetch status", e);
      }
    };
    fetchStatus();
    const interval = setInterval(fetchStatus, 30000); // Poll every 30s
    return () => clearInterval(interval);
  }, []);

  // Initialize WebSocket
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws/chat");

    socket.onopen = () => {
      console.log("Connected to Chat Server");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "typing") {
        setIsTyping(true);
      } else if (data.type === "chunk") {
        setIsTyping(false);
        setMessages((prev) => {
          const lastMsg = prev[prev.length - 1];
          if (lastMsg && lastMsg.role === "assistant") {
            return [...prev.slice(0, -1), { ...lastMsg, content: lastMsg.content + data.content }];
          } else {
            return [...prev, { role: "assistant", content: data.content }];
          }
        });
      } else if (data.type === "complete") {
        setIsTyping(false);
      } else if (data.type === "error") {
        setMessages((prev) => [...prev, { role: "system", content: `Error: ${data.message}` }]);
      }
    };

    socket.onclose = () => console.log("Disconnected");
    setWs(socket);

    return () => socket.close();
  }, []);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const sendMessage = async () => {
    if (!input.trim() || !ws) return;

    const userMsg = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);

    // Optimistic UI for User
    ws.send(JSON.stringify({ message: userMsg, user_id: "web-client" }));
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-gray-100 font-sans">
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 bg-gray-800 border-b border-gray-700 shadow-md">
        <div className="flex items-center gap-3">
          <div className="relative w-12 h-12 overflow-hidden rounded-full border border-gray-600">
            <img
              src="/Logo_Exellence.jpg"
              alt="Excellence Logo"
              className="object-cover w-full h-full"
            />
          </div>
          <div>
            <h1 className="text-lg font-semibold">Panaversity Assistant</h1>
            <p className="text-xs text-gray-400">Powered by Gemini 2.5 & Odoo</p>
          </div>
        </div>
        <div className="flex gap-4 text-xs">
          <StatusBadge label="Odoo" active={status?.main_agent?.odoo_agent?.enabled} />
          <StatusBadge label="Email" active={status?.main_agent?.email_agent?.authenticated} />
          <StatusBadge label="WhatsApp" active={status?.main_agent?.whatsapp_agent?.enabled} />
        </div>
      </header>

      {/* Main Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.length === 0 && (
          <div className="text-center mt-20 text-gray-500">
            <h2 className="text-2xl font-bold mb-2">How can I help you?</h2>
            <p>Ask about emails, leads, or tasks.</p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 whitespace-pre-wrap ${msg.role === "user"
                ? "bg-blue-600 text-white"
                : "bg-gray-800 text-gray-200 border border-gray-700"
                }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-gray-800 rounded-2xl px-4 py-3 border border-gray-700">
              <span className="animate-pulse">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* Input Area */}
      <footer className="p-4 bg-gray-800 border-t border-gray-700">
        <div className="max-w-4xl mx-auto flex gap-2">
          <input
            type="text"
            className="flex-1 bg-gray-900 border border-gray-600 rounded-xl px-4 py-3 focus:outline-none focus:border-blue-500 transition-colors"
            placeholder="Type a message... (e.g. 'Any new leads?')"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button
            onClick={sendMessage}
            disabled={!input.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 rounded-xl font-medium transition-all active:scale-95"
          >
            Send
          </button>
        </div>
      </footer>
    </div>
  );
}

function StatusBadge({ label, active }: { label: string; active: boolean }) {
  return (
    <div className={`flex items-center gap-1.5 px-2 py-1 rounded bg-gray-700/50 border border-gray-600`}>
      <div className={`w-2 h-2 rounded-full ${active ? "bg-green-500" : "bg-red-500"}`} />
      <span>{label}</span>
    </div>
  );
}
