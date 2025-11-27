const viteHost = import.meta.env.VITE_HOST_URL
const viteApi = import.meta.env.VITE_API_V1_STR

export const HOST_URL =
  viteHost ||
  "http://localhost:8000";

export const API_V1_STR =
  viteApi ||
  "/api/v1";

export const API_BASE_URL = HOST_URL + API_V1_STR;