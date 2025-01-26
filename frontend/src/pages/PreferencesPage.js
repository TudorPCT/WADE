import React, { useEffect, useState } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';

const PreferencesPage = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch('http://127.0.0.1:5000/api/preferences?key=search')
            .then(response => response.json())
            .then(data => setData(data))
            .catch(error => console.error('Error fetching data:', error));
            console.log(data);
    }, []);

    return (
        <div>
            <h1>Preferences</h1>
        </div>
    );
};

export default PreferencesPage;