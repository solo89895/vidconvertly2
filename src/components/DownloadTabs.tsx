import React, { useState } from 'react';
import { Download, Music, Video, File, Loader2 } from 'lucide-react';

interface DownloadTabsProps {
  formats: Array<{
    format_id: string;
    height: number;
    ext: string;
    filesize: number;
    format_note: string;
    vcodec: string;
    acodec: string;
  }>;
  onDownload: (formatId: string) => void;
  isLoading: boolean;
}

export const DownloadTabs: React.FC<DownloadTabsProps> = ({
  formats,
  onDownload,
  isLoading
}) => {
  const [activeTab, setActiveTab] = useState<'audio' | 'video' | 'other'>('video');
  const [downloadingFormat, setDownloadingFormat] = useState<string | null>(null);

  const videoFormats = formats.filter(f => f.vcodec !== 'none');
  const audioFormats = formats.filter(f => f.acodec !== 'none' && f.vcodec === 'none');
  const otherFormats = formats.filter(f => f.vcodec === 'none' && f.acodec === 'none');

  const formatFileSize = (bytes: number) => {
    if (!bytes) return 'N/A';
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sizes[i]}`;
  };

  const handleDownload = async (formatId: string) => {
    setDownloadingFormat(formatId);
    try {
      await onDownload(formatId);
    } finally {
      setDownloadingFormat(null);
    }
  };

  const renderDownloadButton = (formatId: string) => {
    const isDownloading = downloadingFormat === formatId;
    return (
      <button
        onClick={() => handleDownload(formatId)}
        disabled={isLoading || isDownloading}
        className="flex items-center px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {isDownloading ? (
          <>
            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            Downloading...
          </>
        ) : (
          <>
            <Download className="w-4 h-4 mr-2" />
            Download
          </>
        )}
      </button>
    );
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'video':
        return (
          <div className="space-y-4">
            {videoFormats.map((format) => (
              <div
                key={format.format_id}
                className="flex items-center justify-between p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex items-center space-x-4">
                  <Video className="w-6 h-6 text-red-500" />
                  <div>
                    <div className="font-medium">{format.height}p</div>
                    <div className="text-sm text-gray-500">
                      {formatFileSize(format.filesize)} • {format.ext.toUpperCase()}
                    </div>
                  </div>
                </div>
                {renderDownloadButton(format.format_id)}
              </div>
            ))}
          </div>
        );
      case 'audio':
        return (
          <div className="space-y-4">
            {audioFormats.map((format) => (
              <div
                key={format.format_id}
                className="flex items-center justify-between p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex items-center space-x-4">
                  <Music className="w-6 h-6 text-blue-500" />
                  <div>
                    <div className="font-medium">Audio Only</div>
                    <div className="text-sm text-gray-500">
                      {formatFileSize(format.filesize)} • {format.ext.toUpperCase()}
                    </div>
                  </div>
                </div>
                {renderDownloadButton(format.format_id)}
              </div>
            ))}
          </div>
        );
      case 'other':
        return (
          <div className="space-y-4">
            {otherFormats.map((format) => (
              <div
                key={format.format_id}
                className="flex items-center justify-between p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex items-center space-x-4">
                  <File className="w-6 h-6 text-gray-500" />
                  <div>
                    <div className="font-medium">{format.format_note || 'Other Format'}</div>
                    <div className="text-sm text-gray-500">
                      {formatFileSize(format.filesize)} • {format.ext.toUpperCase()}
                    </div>
                  </div>
                </div>
                {renderDownloadButton(format.format_id)}
              </div>
            ))}
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      <div className="flex space-x-4 mb-6">
        <button
          onClick={() => setActiveTab('video')}
          className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
            activeTab === 'video'
              ? 'bg-red-500 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          <Video className="w-5 h-5 mr-2" />
          Video
        </button>
        <button
          onClick={() => setActiveTab('audio')}
          className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
            activeTab === 'audio'
              ? 'bg-red-500 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          <Music className="w-5 h-5 mr-2" />
          Audio
        </button>
        <button
          onClick={() => setActiveTab('other')}
          className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
            activeTab === 'other'
              ? 'bg-red-500 text-white'
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          <File className="w-5 h-5 mr-2" />
          Other
        </button>
      </div>
      {renderTabContent()}
    </div>
  );
}; 