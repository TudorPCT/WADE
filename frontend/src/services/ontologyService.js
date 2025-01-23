import axios from 'axios';

const API_URL = 'http://localhost:5000/api/ontologies';

export const searchOntologies = (query) =>
    axios.get(`${API_URL}/search`, { params: { query } }).then(res => res.data);
