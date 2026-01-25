"use client";

import { useState, useEffect, useRef } from "react";

export default function ChatWidget() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
    const [input, setInput] = useState("");
    const [ws, setWs] = useState<WebSocket | null>(null);
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const [isMobile, setIsMobile] = useState(false);

    // Mobile detection
    useEffect(() => {
        const handleResize = () => setIsMobile(window.innerWidth < 768);
        handleResize();
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    // Initialize WebSocket when widget opens
    useEffect(() => {
        if (!isOpen) return;

        if (!ws || ws.readyState === WebSocket.CLOSED) {
            const socket = new WebSocket("ws://localhost:8000/ws/chat");

            socket.onopen = () => console.log("ChatWidget: Connected");

            socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.type === "typing") setIsTyping(true);
                else if (data.type === "chunk") {
                    setIsTyping(false);
                    setMessages((prev) => {
                        const lastMsg = prev[prev.length - 1];
                        if (lastMsg && lastMsg.role === "assistant") {
                            return [...prev.slice(0, -1), { ...lastMsg, content: lastMsg.content + data.content }];
                        } else {
                            return [...prev, { role: "assistant", content: data.content }];
                        }
                    });
                } else if (data.type === "complete") setIsTyping(false);
                else if (data.type === "error") {
                    setMessages((prev) => [...prev, { role: "system", content: `Error: ${data.message}` }]);
                }
            };

            socket.onclose = () => console.log("ChatWidget: Disconnected");
            setWs(socket);
        }

        return () => {
            // Optional: don't close immediately to keep history if they toggle
        };
    }, [isOpen]);

    // Auto-scroll
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isTyping, isOpen]);

    const sendMessage = async () => {
        if (!input.trim() || !ws) return;
        const userMsg = input;
        setInput("");
        setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
        ws.send(JSON.stringify({ message: userMsg, user_id: "widget-client" }));
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className={`fixed z-50 flex flex-col items-end ${isMobile ? "bottom-0 right-0 left-0" : "bottom-6 right-6"}`}>

            {/* Chat Window */}
            {isOpen && (
                <div className={`
          flex flex-col bg-zinc-900/90 backdrop-blur-2xl border border-white/20 shadow-[0_0_40px_rgba(37,99,235,0.2)] overflow-hidden
          ${isMobile ? "w-full h-[80vh] rounded-t-3xl" : "w-[400px] h-[550px] rounded-3xl mb-6"}
          transition-all duration-300 ease-in-out animate-in slide-in-from-bottom-5 fade-in-0
        `}>
                    {/* Header */}
                    <div className="flex items-center justify-between p-4 bg-gradient-to-r from-[var(--neon-blue)] via-[var(--neon-purple)] to-[var(--neon-pink)] border-b border-white/10">
                        <div className="flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full bg-white animate-pulse"></div>
                            <h3 className="font-bold text-white text-base tracking-wide shadow-sm">Panaversity AI</h3>
                        </div>
                        <button
                            onClick={() => setIsOpen(false)}
                            className="text-white/80 hover:text-white hover:bg-white/20 transition-all p-1.5 rounded-full"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                        </button>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-4 scroll-smooth custom-scrollbar">
                        {messages.length === 0 && (
                            <div className="flex flex-col items-center justify-center h-full text-center text-gray-400 p-6 space-y-4">
                                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center border border-white/10 shadow-inner">
                                    <span className="text-3xl">👋</span>
                                </div>
                                <div>
                                    <p className="text-white font-medium text-lg">Hello! I'm your assistant.</p>
                                    <p className="text-sm text-gray-400 mt-1">Ask about your schedule, emails, or updates!</p>
                                </div>
                            </div>
                        )}
                        {messages.map((msg, i) => (
                            <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                                <div className={`
                  max-w-[85%] px-4 py-3 rounded-2xl text-sm whitespace-pre-wrap shadow-md leading-relaxed
                  ${msg.role === "user"
                                        ? "bg-gradient-to-br from-[var(--neon-blue)] to-[var(--neon-purple)] text-white rounded-br-none border border-white/10"
                                        : "bg-white/10 border border-white/10 text-gray-100 rounded-bl-none backdrop-blur-md"}
                `}>
                                    {msg.content}
                                </div>
                            </div>
                        ))}
                        {isTyping && (
                            <div className="flex justify-start">
                                <div className="bg-white/5 border border-white/10 rounded-2xl rounded-bl-none px-4 py-2 text-xs text-gray-400 flex items-center gap-1">
                                    <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></span>
                                    <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></span>
                                    <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></span>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input */}
                    <div className="p-4 bg-zinc-900/95 border-t border-white/10 backdrop-blur-xl">
                        <div className="relative flex items-center group">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={handleKeyDown}
                                placeholder="Type your message..."
                                className="w-full bg-black/40 text-white placeholder-gray-500 rounded-full py-3 pl-5 pr-12 text-sm border border-white/10 focus:outline-none focus:border-[var(--neon-purple)] focus:ring-1 focus:ring-[var(--neon-purple)] transition-all"
                            />
                            <button
                                onClick={sendMessage}
                                disabled={!input.trim()}
                                className="absolute right-1.5 p-2 bg-gradient-to-r from-[var(--neon-blue)] to-[var(--neon-purple)] rounded-full text-white disabled:opacity-50 disabled:grayscale transition-all hover:scale-105 active:scale-95 shadow-lg shadow-purple-500/20"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Radiant Toggle Button */}
            {!isOpen && (
                <button
                    onClick={() => setIsOpen(true)}
                    className="group relative flex items-center justify-center w-16 h-16 rounded-full transform hover:scale-110 transition-all duration-300 active:scale-95"
                >
                    {/* Pulsing glow background */}
                    <div className="absolute inset-0 rounded-full bg-gradient-to-r from-[var(--neon-pink)] to-[var(--neon-purple)] animate-pulse opacity-75 blur-md group-hover:opacity-100 group-hover:blur-lg transition-all"></div>

                    {/* Main button */}
                    <div className="relative flex items-center justify-center w-full h-full bg-gradient-to-r from-[var(--neon-pink)] via-[var(--neon-purple)] to-[var(--neon-blue)] rounded-full shadow-2xl border border-white/20">
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="white" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="absolute transition-all duration-300 group-hover:opacity-0 scale-100 group-hover:scale-75 drop-shadow-md">
                            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                        </svg>
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="absolute transition-all duration-300 opacity-0 group-hover:opacity-100 scale-75 group-hover:scale-100 drop-shadow-md">
                            <line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line>
                        </svg>
                    </div>
                </button>
            )}
        </div>
    );
}
