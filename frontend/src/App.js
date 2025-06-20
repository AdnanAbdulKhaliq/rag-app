import React, { useState, useRef, useEffect } from "react";
import { Bot, User, Send, Loader, FileText } from "lucide-react";
import "./App.css";

// --- Main App Component ---
export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const sessionId = useRef(Date.now().toString()); // Generate a unique session ID

  // Function to scroll to the latest message
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Set an initial greeting message from the bot
  useEffect(() => {
    setMessages([
      {
        text: "Hello! I'm an AI assistant. How can I help you with the Leave Policy document today?",
        isUser: false,
      },
    ]);
  }, []);

  // --- Handle message submission ---
  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { text: input, isUser: true };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: input,
          session_id: sessionId.current,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(
          `HTTP error! status: ${response.status}, message: ${errorText}`
        );
      }

      const data = await response.json();
      const botMessage = { text: data.answer, isUser: false };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Failed to fetch from backend:", error);
      const errorMessage = {
        text: "Sorry, I'm having trouble connecting to my brain right now. Please try again later.",
        isUser: false,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // --- Render the component ---
  return (
    <div className="chat-container">
      {/* Header */}
      <header className="chat-header">
        <FileText className="header-icon" />
        <h1 className="header-title">Leave Policy RAG Agent</h1>
      </header>

      {/* Chat Messages */}
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message-wrapper ${
              msg.isUser ? "user-message-wrapper" : "bot-message-wrapper"
            }`}
          >
            {!msg.isUser && (
              <div className="avatar bot-avatar">
                <Bot className="avatar-icon" />
              </div>
            )}
            <div
              className={`message-bubble ${
                msg.isUser ? "user-message-bubble" : "bot-message-bubble"
              }`}
            >
              <p>{msg.text}</p>
            </div>
            {msg.isUser && (
              <div className="avatar user-avatar">
                <User className="avatar-icon" />
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message-wrapper bot-message-wrapper">
            <div className="avatar bot-avatar">
              <Bot className="avatar-icon" />
            </div>
            <div className="message-bubble bot-message-bubble loading-bubble">
              <Loader className="loader-icon" />
              <p>Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <footer className="chat-footer">
        <form onSubmit={handleSendMessage} className="message-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about the leave policy..."
            className="message-input"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="send-button"
            disabled={isLoading || !input.trim()}
          >
            <Send className="send-icon" />
          </button>
        </form>
      </footer>
    </div>
  );
}
