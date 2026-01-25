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
          flex flex-col bg-opacity-90 backdrop-blur-md bg-gray-900 border border-white/10 shadow-2xl overflow-hidden
          ${isMobile ? "w-full h-[80vh] rounded-t-2xl" : "w-[400px] h-[500px] rounded-2xl mb-4"}
          transition-all duration-300 ease-in-out
        `}>
                    {/* Header */}
                    <div className="flex items-center justify-between p-4 bg-gradient-to-r from-indigo-600/80 to-purple-600/80 backdrop-blur-lg border-b border-white/10">
                        <h3 className="font-bold text-white text-sm tracking-wide">Panaversity AI</h3>
                        <button
                            onClick={() => setIsOpen(false)}
                            className="text-white/80 hover:text-white transition-colors p-1 rounded-full hover:bg-white/10"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                        </button>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-4 scroll-smooth">
                        {messages.length === 0 && (
                            <div className="text-center text-gray-400 mt-10 text-sm">
                                <p>Hello! I'm your student assistant.</p>
                                <p className="text-xs mt-2">Ask me about your schedule, emails, or generic questions!</p>
                            </div>
                        )}
                        {messages.map((msg, i) => (
                            <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                                <div className={`
                  max-w-[85%] px-3 py-2 rounded-xl text-sm whitespace-pre-wrap shadow-sm
                  ${msg.role === "user"
                                        ? "bg-indigo-600 text-white rounded-br-none"
                                        : "bg-gray-800/80 border border-white/10 text-gray-200 rounded-bl-none"}
                `}>
                                    {msg.content}
                                </div>
                            </div>
                        ))}
                        {isTyping && (
                            <div className="flex justify-start">
                                <div className="bg-gray-800/80 border border-white/10 rounded-xl rounded-bl-none px-3 py-2 text-xs text-gray-400 animate-pulse">
                                    Thinking...
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input */}
                    <div className="p-3 bg-gray-900/90 border-t border-white/10">
                        <div className="relative flex items-center">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={handleKeyDown}
                                placeholder="Type your question..."
                                className="w-full bg-gray-800/50 text-white placeholder-gray-500 rounded-full py-2 pl-4 pr-10 text-sm border border-white/10 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
                            />
                            <button
                                onClick={sendMessage}
                                disabled={!input.trim()}
                                className="absolute right-1 p-1.5 bg-indigo-600 rounded-full text-white disabled:opacity-50 disabled:bg-gray-700 hover:bg-indigo-500 transition-all"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Toggle Button */}
            {!isOpen && (
                <button
                    onClick={() => setIsOpen(true)}
                    className="group flex items-center justify-center w-14 h-14 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full shadow-lg shadow-indigo-500/30 hover:scale-110 hover:shadow-indigo-500/50 transition-all duration-300 transform active:scale-95"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="white" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="absolute transition-all duration-300 group-hover:opacity-0 scale-100 group-hover:scale-75">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="absolute transition-all duration-300 opacity-0 group-hover:opacity-100 scale-75 group-hover:scale-100">
                        <line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                </button>
            )}
        </div>
    );
}
