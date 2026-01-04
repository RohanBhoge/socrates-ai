import axios from 'axios';

const API_BASE_URL = '/api/chat'; // Vite proxy handles redirection to backend

export const api = {
    // Send text + optional files
    sendMessage: async ({ conversationId, message, files }) => {
        const formData = new FormData();
        if (conversationId) {
            formData.append('conversation_id', conversationId);
        }
        formData.append('message', message);

        if (files && files.length > 0) {
            files.forEach(file => {
                formData.append('files', file);
            });
        }

        try {
            const response = await axios.post(API_BASE_URL, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            return response.data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // Get conversation history
    getHistory: async (conversationId) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/history/${conversationId}`);
            return response.data;
        } catch (error) {
            console.error('History fetch error:', error);
            throw error;
        }
    },

    // Clear memory
    clearMemory: async (conversationId) => {
        try {
            await axios.post(`${API_BASE_URL}/clear/${conversationId}`);
        } catch (error) {
            console.error('Clear memory error', error);
            throw error;
        }
    }
};
