import axios from "axios";
import { createClient } from "./supabaseClient";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL, // e.g. https://your-backend.onrender.com
});

// Attach the current Supabase access token to every outgoing request.
api.interceptors.request.use(async (config) => {
  const supabase = createClient();
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (session?.access_token) {
    config.headers.Authorization = `Bearer ${session.access_token}`;
  }
  return config;
});

export default api;
