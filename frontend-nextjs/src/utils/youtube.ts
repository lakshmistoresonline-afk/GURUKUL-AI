/**
 * Gurukul AI YouTube Utilities
 */

/**
 * Extracts the Video ID from various YouTube URL formats.
 */
export function extractVideoId(url: string): string | null {
  if (!url) return null;

  // Standard watch URL: https://www.youtube.com/watch?v=VIDEO_ID
  const watchMatch = url.match(/(?:v=|v\/|embed\/|shorts\/|youtu\.be\/|\/v\/|\/e\/|watch\?v=|\/watch\?feature=player_embedded&v=)([^#&?]*)/);
  if (watchMatch && watchMatch[1]) {
    const id = watchMatch[1];
    // Video IDs are typically 11 characters
    if (id.length === 11) return id;
  }

  return null;
}

/**
 * Normalizes any valid YouTube video URL to a standard watch URL.
 */
export function normalizeVideoUrl(url: string): string | null {
  const videoId = extractVideoId(url);
  if (videoId) {
    return `https://www.youtube.com/watch?v=${videoId}`;
  }
  return null;
}

/**
 * Checks if a URL is a YouTube search results URL.
 */
export function isYouTubeSearchUrl(url: string): boolean {
  if (!url) return false;
  return url.includes('youtube.com/results') || url.includes('search_query=');
}

/**
 * Generates a clean direct video URL from a video ID.
 */
export function getDirectVideoUrl(videoId: string): string {
  return `https://www.youtube.com/watch?v=${videoId}`;
}
