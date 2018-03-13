export const SERVER_URL = process.env.NODE_ENV === 'production' ? 'https://example.com': process.env.NODE_ENV === 'stage' ? 'https://beta.example.com': 'http://127.0.0.1:8000';
export const API_URL = `${SERVER_URL}/api`;

export const COUNT_PER_PAGE = 15;
