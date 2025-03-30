import axios from 'axios';

const API_BASE_URL = 'http://192.168.8.104:8000';

export interface VideoFormat {
  format_id: string;
  height: number;
  ext: string;
  filesize: number;
  format_note: string;
  vcodec: string;
  acodec: string;
}

export interface VideoInfo {
  title: string;
  duration: number;
  formats: VideoFormat[];
}

export const API_ENDPOINTS = {
    convert: `${API_BASE_URL}/api/convert`,
    download: `${API_BASE_URL}/api/download`
};

export const validateUrl = (url: string, platform: string): boolean => {
    const patterns = {
        youtube: /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$/,
        facebook: /^(https?:\/\/)?(www\.)?facebook\.com\/.+$/,
        instagram: /^(https?:\/\/)?(www\.)?instagram\.com\/.+$/,
        tiktok: /^(https?:\/\/)?(www\.)?tiktok\.com\/.+$/,
        pinterest: /^(https?:\/\/)?(www\.)?pinterest\.com\/.+$/
    };

    return patterns[platform as keyof typeof patterns]?.test(url) || false;
};

export const getVideoInfo = async (url: string): Promise<VideoInfo> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/info?url=${encodeURIComponent(url)}`);
    if (!response.ok) {
      throw new Error('Failed to fetch video info');
    }
    return response.json();
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to get video information');
    }
    throw error;
  }
};

interface DownloadOptions {
  fileName?: string;
  compress?: boolean;
  quality?: number;
}

export const downloadVideo = async (params: any) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/download`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params)
    });

    if (!response.ok) {
      throw new Error('Failed to download video');
    }

    return response;
  } catch (error) {
    console.error('Download error:', error);
    throw error;
  }
}; 