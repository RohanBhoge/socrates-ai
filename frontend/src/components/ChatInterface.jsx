import React, { useState, useRef, useEffect } from 'react';
import { Send, UploadCloud } from 'lucide-react';
import { useChat } from '../hooks/useChat';
import { useFileUpload } from '../hooks/useFileUpload';
import { MessageBubble } from './MessageBubble';
import { TypingIndicator } from './TypingIndicator';
import { FileUpload } from './FileUpload';
import '../styles/ChatInterface.css';

export const ChatInterface = () => {
    const { messages, sendMessage, isLoading, error } = useChat();
    const { files, onDrop, removeFile, clearFiles, fileError } = useFileUpload();
    const [inputValue, setInputValue] = useState("");
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isLoading]);

    const handleSend = async (e) => {
        e.preventDefault();
        if ((!inputValue.trim() && files.length === 0) || isLoading) return;

        // Pass current state to hook
        await sendMessage(inputValue, files);

        // Reset local state
        setInputValue("");
        clearFiles();
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend(e);
        }
    };

    return (
        <div className="chat-container">
            <header className="chat-header">
                <div style={{ background: '#2563eb', padding: '8px', borderRadius: '8px', color: 'white' }}>
                    <UploadCloud size={24} />
                </div>
                <h1>SocratesAI Learning Companion</h1>
            </header>

            <div className="messages-area">
                {messages.length === 0 && (
                    <div style={{ textAlign: 'center', color: '#64748b', marginTop: '2rem' }}>
                        <h3>Welcome! 👋</h3>
                        <p>I help you understand concepts through questioning.</p>
                        <p>Ask me about Math, Physics, or any topic you're stuck on.</p>
                    </div>
                )}

                {messages.map((msg) => (
                    <MessageBubble key={msg.id || Math.random()} message={msg} />
                ))}

                {isLoading && (
                    <div className="message-bubble assistant">
                        <TypingIndicator />
                    </div>
                )}

                {error && <div className="error-banner">{error}</div>}

                <div ref={messagesEndRef} />
            </div>

            <div className="input-area">
                {fileError && <div className="error-banner">{fileError}</div>}

                <form className="input-form" onSubmit={handleSend}>
                    {/* <FileUpload onDrop={onDrop} files={files} onRemove={removeFile} /> */}

                    <div className="input-controls">
                        <textarea
                            className="chat-input"
                            placeholder="Type a message or explanation..."
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyDown={handleKeyDown}
                            disabled={isLoading}
                        />
                        <button
                            type="submit"
                            className="send-button"
                            disabled={isLoading || (!inputValue.trim() && files.length === 0)}
                        >
                            <Send size={20} />
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};
