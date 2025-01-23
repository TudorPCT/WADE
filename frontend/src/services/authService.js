import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const login = (credentials) => axios.post(`${API_URL}/login`, credentials).then(res => res.data);

export const signup = (data) => axios.post(`${API_URL}/signup`, data).then(res => res.data);
