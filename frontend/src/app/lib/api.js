const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

async function request(path, options = {}) {
  const token = localStorage.getItem("token");
  const headers = { "Content-Type": "application/json", ...options.headers };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw { status: res.status, ...body };
  }

  return res.json();
}

export const api = {
  login: (username, password) =>
    request("/api/users/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),

  register: (username, password) =>
    request("/api/users/register", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),

  getPosts: (page = 0, size = 10) =>
    request(`/api/posts?page=${page}&size=${size}`),

  createPost: (content) =>
    request("/api/posts", {
      method: "POST",
      body: JSON.stringify({ content }),
    }),

  likePost: (postId) =>
    request(`/api/posts/${postId}/like`, { method: "POST" }),

  dislikePost: (postId) =>
    request(`/api/posts/${postId}/dislike`, { method: "POST" }),

  getComments: (postId) => request(`/api/posts/${postId}/comments`),

  addComment: (postId, content) =>
    request(`/api/posts/${postId}/comment`, {
      method: "POST",
      body: JSON.stringify({ content }),
    }),

  getUser: (id) => request(`/api/users/${id}`),

  getUserPosts: (id, page = 0, size = 10) =>
    request(`/api/users/${id}/posts?page=${page}&size=${size}`),
};
