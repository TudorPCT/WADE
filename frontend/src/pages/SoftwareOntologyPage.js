import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import './SoftwareOntologyPage.css'; // Import the CSS file

const SoftwareOntologyPage = () => {
    const [data, setData] = useState([]);
    const location = useLocation();
    const params = new URLSearchParams(location.search);
    const fragment = params.get('fragment');

    useEffect(() => {
        if (fragment) {
            fetchData(fragment);
        }
    }, [fragment]);

    const fetchData = async (fragment) => {
        try {
            console.log('Fetching data for:', fragment);
            const response = await fetch(`http://127.0.0.1:5000/software-ontology?fragment=${fragment}`);
            const json = await response.json();
            setData(json);  // Adjust based on your API response
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    return (
        <div className="ontology-page">
            <h1 className="ontology-title">Software Ontology - {fragment}</h1>
            <DataTable value={data} showGridlines tableStyle={{ minWidth: '50rem' }}>
                <Column field="predicate" header="Predicate"></Column>
                <Column field="object" header="Object"></Column>
            </DataTable>
        </div>
    );
};

export default SoftwareOntologyPage;
