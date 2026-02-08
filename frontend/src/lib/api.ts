/**
 * API client utility for backend communication.
 * Handles JWT token attachment, error handling, and timeouts.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface ChatResponse {
  message: string;
  conversation_id: string;
}

interface ConversationHistory {
  conversation_id: string | null;
  messages: Array<{
    id: string;
    role: "user" | "assistant";
    content: string;
    created_at: string;
  }>;
}

/**
 * Custom error class for API errors.
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Handle API response errors with user-friendly messages.
 */
async function handleResponseError(response: Response): Promise<never> {
  const status = response.status;
  let errorData: { detail?: string; error?: string; message?: string } = {};

  try {
    errorData = await response.json();
  } catch {
    // Response body is not JSON
  }

  const serverMessage = errorData.detail || errorData.error || errorData.message;

  switch (status) {
    case 401:
      throw new ApiError(
        serverMessage || "Session expired. Please sign in again.",
        status,
        "UNAUTHORIZED"
      );
    case 403:
      throw new ApiError(
        serverMessage || "You don't have permission to perform this action.",
        status,
        "FORBIDDEN"
      );
    case 404:
      throw new ApiError(
        serverMessage || "The requested resource was not found.",
        status,
        "NOT_FOUND"
      );
    case 429:
      throw new ApiError(
        serverMessage || "Too many requests. Please try again in a moment.",
        status,
        "RATE_LIMITED"
      );
    case 500:
    case 502:
    case 503:
      throw new ApiError(
        serverMessage || "The server is temporarily unavailable. Please try again later.",
        status,
        "SERVER_ERROR"
      );
    default:
      throw new ApiError(
        serverMessage || `Request failed with status ${status}`,
        status,
        "UNKNOWN"
      );
  }
}

/**
 * Send a chat message to the backend.
 */
export async function sendChatMessage(
  userId: string,
  message: string,
  token: string,
  timeout: number = 30000
): Promise<ChatResponse> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(`${API_URL}/api/${userId}/chat`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
      signal: controller.signal,
    });

    if (!response.ok) {
      await handleResponseError(response);
    }

    return response.json();
  } catch (err) {
    if (err instanceof ApiError) {
      throw err;
    }
    if (err instanceof Error && err.name === "AbortError") {
      throw new ApiError(
        "Request timed out. Please try again.",
        408,
        "TIMEOUT"
      );
    }
    throw new ApiError(
      "Network error. Please check your connection.",
      0,
      "NETWORK_ERROR"
    );
  } finally {
    clearTimeout(timeoutId);
  }
}

/**
 * Get conversation history for a user.
 */
export async function getConversationHistory(
  userId: string,
  token: string,
  limit: number = 50,
  timeout: number = 10000
): Promise<ConversationHistory> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(
      `${API_URL}/api/${userId}/conversations?limit=${limit}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        signal: controller.signal,
      }
    );

    if (!response.ok) {
      await handleResponseError(response);
    }

    return response.json();
  } catch (err) {
    if (err instanceof ApiError) {
      throw err;
    }
    if (err instanceof Error && err.name === "AbortError") {
      throw new ApiError(
        "Request timed out. Please try again.",
        408,
        "TIMEOUT"
      );
    }
    throw new ApiError(
      "Network error. Please check your connection.",
      0,
      "NETWORK_ERROR"
    );
  } finally {
    clearTimeout(timeoutId);
  }
}

/**
 * Health check for the backend.
 */
export async function checkHealth(): Promise<{ status: string; timestamp: string }> {
  const response = await fetch(`${API_URL}/health`);
  if (!response.ok) {
    throw new ApiError("Backend is unavailable", response.status, "HEALTH_CHECK_FAILED");
  }
  return response.json();
}
