import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Bot, User } from 'lucide-react';

export const MessageBubble = ({ message }) => {
    const isAssistant = message.role === 'assistant';

    return (
        <div className={`message-bubble ${message.role}`}>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                <div className={`avatar ${message.role}`} style={{
                    marginTop: '4px',
                    color: isAssistant ? '#2563eb' : '#64748b'
                }}>
                    {isAssistant ? <Bot size={24} /> : <User size={24} />}
                </div>

                <div className="content" style={{ flex: 1 }}>
                    {/* Display uploaded files metadata if any (for user) */}
                    {message.files && message.files.length > 0 && (
                        <div className="message-files" style={{ marginBottom: '0.5rem' }}>
                            {message.files.map((file, idx) => (
                                <div key={idx} className="file-badge" style={{
                                    fontSize: '0.8rem',
                                    background: 'rgba(0,0,0,0.05)',
                                    padding: '2px 8px',
                                    borderRadius: '12px',
                                    display: 'inline-block',
                                    marginRight: '8px'
                                }}>
                                    📎 {file.name}
                                </div>
                            ))}
                        </div>
                    )}

                    <div className="markdown-content">
                        <ReactMarkdown>
                            {message.content}
                        </ReactMarkdown>
                    </div>
                </div>
            </div>
        </div>
    );
};
