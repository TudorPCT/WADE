import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

export const getPreferences = () => axios.get(API_URL/api/preferences).then(res => res.data);

export const updatePreferences = (data) => axios.put(API_URL/api/preferences, data).then(res => res.data);
