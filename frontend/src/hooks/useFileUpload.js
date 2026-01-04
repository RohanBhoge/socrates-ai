import { useState, useCallback } from 'react';

export const useFileUpload = (maxFiles = 3, maxSizeMB = 10) => {
    const [files, setFiles] = useState([]);
    const [fileError, setFileError] = useState(null);

    const onDrop = useCallback((acceptedFiles) => {
        setFileError(null);
        const validFiles = acceptedFiles.filter(file => {
            if (file.size > maxSizeMB * 1024 * 1024) {
                setFileError(`File ${file.name} is too large (Max ${maxSizeMB}MB)`);
                return false;
            }
            return true;
        });

        setFiles(prev => {
            const newFiles = [...prev, ...validFiles];
            if (newFiles.length > maxFiles) {
                setFileError(`Maximum ${maxFiles} files allowed`);
                return prev;
            }
            return newFiles;
        });
    }, [maxFiles, maxSizeMB]);

    const removeFile = useCallback((fileToRemove) => {
        setFiles(prev => prev.filter(f => f !== fileToRemove));
    }, []);

    const clearFiles = useCallback(() => {
        setFiles([]);
    }, []);

    return { files, onDrop, removeFile, clearFiles, fileError };
};
