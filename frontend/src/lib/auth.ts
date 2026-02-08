import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { createClient } from "@libsql/client";

/**
 * Better Auth server configuration.
 * This configures the auth handlers for the API routes.
 */

// Create libSQL client for SQLite
const client = createClient({
  url: "file:./dev.db",
});

export const auth = betterAuth({
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
  basePath: "/api/auth",
  secret: process.env.BETTER_AUTH_SECRET,
  database: client,
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
  emailAndPassword: {
    enabled: true,
    autoSignIn: true,
  },
  plugins: [
    jwt(),
  ],
});
