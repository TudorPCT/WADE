import React, { useEffect, useState } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

const PreferencesPage = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        axios.get(`${API_URL}/api/preferences?key=search`)
            .then(response => setData(response.data))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <div>
            <h1>Preferences</h1>
            <DataTable value={data}>
                <Column field="id" header="ID" />
                <Column field="name" header="Name" />
                <Column field="value" header="Value" />
            </DataTable>
        </div>
    );
};

export default PreferencesPage;