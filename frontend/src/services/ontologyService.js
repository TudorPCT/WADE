import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

export const searchOntologies = (query) =>
    axios.get(`${API_URL}/api/search`, { params: { query } }).then(res => res.data);
