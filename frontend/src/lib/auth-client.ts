/**
 * Authentication client for backend API.
 * Handles signup, signin, and token management.
 */

import axios from 'axios';

// Use the same base URL as in api.ts
// Always append /api/v1 to the base URL for auth endpoints
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_BASE_URL = BASE_URL.includes('/api/v1') ? BASE_URL : `${BASE_URL}/api/v1`;

// Create an axios instance for auth requests
const authApiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

interface AuthResponse {
  token: string;
  user: {
    id: string;
    email: string;
    email_verified: boolean;
    created_at: string;
    updated_at: string;
  };
}

/**
 * Sign up a new user.
 */
export async function signUp(email: string, password: string): Promise<void> {
  try {
    const response = await authApiClient.post<AuthResponse>('/auth/signup', { email, password });

    // Store token and user info in localStorage
    localStorage.setItem('auth_token', response.data.token);
    localStorage.setItem('user_id', response.data.user.id);
    localStorage.setItem('user_email', response.data.user.email);
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const errorMessage = error.response.data?.detail || 'Signup failed';
      throw new Error(errorMessage);
    }
    throw new Error('Signup failed');
  }
}

/**
 * Sign in an existing user.
 */
export async function signIn(email: string, password: string): Promise<void> {
  try {
    const response = await authApiClient.post<AuthResponse>('/auth/signin', { email, password });

    // Store token and user info in localStorage
    localStorage.setItem('auth_token', response.data.token);
    localStorage.setItem('user_id', response.data.user.id);
    localStorage.setItem('user_email', response.data.user.email);
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const errorMessage = error.response.data?.detail || 'Sign in failed';
      throw new Error(errorMessage);
    }
    throw new Error('Sign in failed');
  }
}

/**
 * Sign out the current user.
 * Revokes the JWT token on the backend.
 */
export async function signOut(): Promise<void> {
  const token = getToken();

  if (token) {
    try {
      // Call logout endpoint to revoke token
      await authApiClient.post('/auth/logout', {}, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
    } catch (error) {
      // Log error but still clear local storage
      console.error('Logout API call failed:', error);
    }
  }

  // Clear local storage
  localStorage.removeItem('auth_token');
  localStorage.removeItem('user_id');
  localStorage.removeItem('user_email');

  // Redirect to home
  if (typeof window !== 'undefined') {
    window.location.href = '/';
  }
}

/**
 * Get the current auth token.
 */
export function getToken(): string | null {
  return localStorage.getItem('auth_token');
}

/**
 * Get the current user ID.
 */
export function getUserId(): string | null {
  return localStorage.getItem('user_id');
}

/**
 * Check if user is authenticated.
 */
export function isAuthenticated(): boolean {
  return !!getToken();
}
