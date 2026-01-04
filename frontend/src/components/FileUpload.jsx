import React from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, FileText, Image as ImageIcon } from 'lucide-react';

export const FileUpload = ({ onDrop, files, onRemove }) => {
    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/*': ['.jpeg', '.png', '.jpg', '.webp'],
            'application/pdf': ['.pdf']
        },
        maxFiles: 3,
        maxSize: 10485760 // 10MB
    });

    return (
        <div className="file-upload-container">
            <div {...getRootProps()} className={`file-upload-zone ${isDragActive ? 'active' : ''}`}>
                <input {...getInputProps()} />
                <Upload size={18} style={{ marginRight: '8px' }} />
                {isDragActive ? (
                    <span>Drop files here...</span>
                ) : (
                    <span>Drag & drop images/PDFs, or click to select</span>
                )}
            </div>

            {files.length > 0 && (
                <div className="file-preview-list">
                    {files.map((file, index) => (
                        <div key={index} className="file-preview-item">
                            {file.type.includes('pdf') ? <FileText size={14} /> : <ImageIcon size={14} />}
                            <span style={{ maxWidth: '150px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                                {file.name}
                            </span>
                            <button
                                className="remove-file"
                                onClick={(e) => { e.stopPropagation(); onRemove(file); }}
                            >
                                <X size={14} />
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};
