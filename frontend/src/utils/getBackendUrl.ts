/**
 * Get the backend URL based on the current environment
 * Returns empty string for relative URLs to avoid CORS issues and use Nginx proxy
 */
export function getBackendUrl(): string {
  return import.meta.env.VITE_BACKEND_URL || '';
}

// Convenience function to get API URL (alias for backward compatibility)
export function getApiUrl(): string {
  return getBackendUrl();
}

// Export as default for simpler imports
export default getBackendUrl;
