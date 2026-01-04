import { useState, useCallback } from 'react';
import { api } from '../services/api';
import { v4 as uuidv4 } from 'uuid';

export const useChat = () => {
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [conversationId, setConversationId] = useState(null);
    const [error, setError] = useState(null);

    const sendMessage = useCallback(async (text, files = []) => {
        if (!text.trim() && files.length === 0) return;

        // Add user message to UI immediately
        const userMessage = {
            id: uuidv4(),
            role: 'user',
            content: text,
            files: files.map(f => ({ name: f.name, type: f.type, size: f.size })) // Store metadata
        };

        setMessages(prev => [...prev, userMessage]);
        setIsLoading(true);
        setError(null);

        try {
            const response = await api.sendMessage({
                conversationId,
                message: text,
                files
            });

            // Add AI response
            const aiMessage = {
                id: response.message_id || uuidv4(),
                role: 'assistant', // Mapped from 'model' usually, but here consistent UI role
                content: response.reply
            };

            setMessages(prev => [...prev, aiMessage]);

            if (!conversationId && response.conversation_id) {
                setConversationId(response.conversation_id);
            }
        } catch (err) {
            setError("Failed to send message. Please try again.");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    }, [conversationId]);

    return { messages, sendMessage, isLoading, error };
};
