import axios from 'axios';

const API_URL = 'http://localhost:5000/api/preferences';

export const getPreferences = () => axios.get(API_URL).then(res => res.data);

export const updatePreferences = (data) => axios.put(API_URL, data).then(res => res.data);
