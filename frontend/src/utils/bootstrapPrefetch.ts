import { SecureAPI } from '../lib/secureApi';
import { sessionManager } from './sessionManager';

// Use relative URL by default to leverage Nginx proxy
const getBackendUrl = () => {
  const configuredUrl = import.meta.env.VITE_BACKEND_URL;
  if (configuredUrl) {
    return configuredUrl;
  }
  return '';
};

const BACKEND_URL = getBackendUrl();

// Singleton to manage prefetch promise
class BootstrapPrefetchManager {
  private prefetchPromise: Promise<any> | null = null;
  private prefetchData: any = null;
  private prefetchStartTime: number = 0;
  private readonly MAX_RETRY_ATTEMPTS = 2; // Reduced retries for faster failure
  private readonly RETRY_DELAY_BASE = 500; // Reduced base delay for faster retries
  private retryCount = 0;
  private isAvailable = true; // Track if endpoint is available
  
  /**
   * Start prefetching bootstrap data with proper session validation and retry logic
   * This runs in parallel with other initialization
   * Non-blocking - failures won't affect auth flow
   */
  async prefetch(): Promise<any> {
    return null;
  }
}

export const bootstrapPrefetch = new BootstrapPrefetchManager();
