/**
 * Reusable authentication form component.
 * Used for both login and signup pages.
 */
'use client';

import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import { signIn, signUp } from '../lib/auth-client';
import { isValidEmail, isValidPassword, sanitizeInput } from '../lib/utils';
import { useToast } from './ToastProvider';

interface AuthFormProps {
  mode: 'login' | 'signup';
}

export default function AuthForm({ mode }: AuthFormProps) {
  const router = useRouter();
  const { showToast } = useToast();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const isLogin = mode === 'login';
  const title = isLogin ? 'Sign In' : 'Sign Up';
  const buttonText = isLogin ? 'Sign In' : 'Create Account';
  const switchText = isLogin ? "Don't have an account?" : 'Already have an account?';
  const switchLink = isLogin ? '/signup' : '/login';
  const switchLinkText = isLogin ? 'Sign Up' : 'Sign In';

  const validateForm = (): boolean => {
    if (!email || !password) {
      setError('Email and password are required');
      return false;
    }

    if (!isValidEmail(email)) {
      setError('Please enter a valid email address');
      return false;
    }

    if (!isValidPassword(password)) {
      setError('Password must be at least 8 characters');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const cleanEmail = sanitizeInput(email);

      if (isLogin) {
        await signIn(cleanEmail, password);
      } else {
        await signUp(cleanEmail, password);
      }

      // Show success notification
      const action = isLogin ? 'signed in' : 'signed up';
      showToast(`Successfully ${action}`, 'success');

      // Redirect to chat on success
      router.push('/chat');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMessage);

      // Show error notification
      showToast(errorMessage, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card p-8 rounded-2xl w-full max-w-sm mx-auto">
      <div className="text-center">
        <h2 className="mt-2 text-center text-2xl sm:text-3xl font-extrabold gradient-text">
          {title}
        </h2>
        <p className="mt-2 text-center text-sm text-gray-400">
          {switchText}{' '}
          <a
            href={switchLink}
            className="font-medium text-[#FF6B6B] hover:text-[#FF8E8E]"
          >
            {switchLinkText}
          </a>
        </p>
      </div>

      <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
        {error && (
          <div className="rounded-md bg-red-500/20 p-4 border border-red-500/50">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-300">{error}</h3>
              </div>
            </div>
          </div>
        )}

        <div className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
              Email address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 placeholder-gray-500 text-white focus:outline-none focus:ring-2 focus:ring-[#FF6B6B] focus:border-transparent text-base"
              placeholder="Email address"
              disabled={loading}
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete={isLogin ? 'current-password' : 'new-password'}
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 placeholder-gray-500 text-white focus:outline-none focus:ring-2 focus:ring-[#FF6B6B] focus:border-transparent text-base"
              placeholder="Password (min 8 characters)"
              disabled={loading}
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            disabled={loading}
            className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-base font-medium rounded-lg text-white bg-gradient-to-r from-[#FF6B6B] to-[#4ECDC4] hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#FF6B6B] disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Processing...' : buttonText}
          </button>
        </div>
      </form>
    </div>
  );
}
