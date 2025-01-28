import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import './SoftwareOntologyPage.css'; // Import the CSS file

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

const SoftwareOntologyPage = () => {
    const [data, setData] = useState([]);
    const location = useLocation();
    const navigate = useNavigate();
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
            const response = await fetch(`${API_URL}/software-ontology?fragment=${fragment}`);
            const json = await response.json();
            setData(json);  // Adjust based on your API response
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const handleLinkClick = (e, link) => {
        e.preventDefault();
        const url = new URL(link);
        const newFragment = url.hash.substring(1);
        if (link.includes('/software-ontology')) {
            navigate(`/software-ontology?fragment=${newFragment}`);
        } else {
            window.open(link, '_blank', 'noopener,noreferrer');
        }
    };

    const isValidURL = (string) => {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    };

    const objectTemplate = (rowData) => {
        const link = rowData.object;
        if (isValidURL(link)) {
            if (link.includes('/software-ontology')) {
                return <a href={link} onClick={(e) => handleLinkClick(e, link)}>{link}</a>;
            }
            return <a href={link} target="_blank" rel="noopener noreferrer">{link}</a>;
        }
        return <span>{link}</span>;
    };

    return (
        <div className="ontology-page">
            <h1 className="ontology-title">Software Ontology - {fragment}</h1>
            <DataTable value={data} showGridlines>
                <Column field="predicate" header="Predicate" body={objectTemplate}></Column>
                <Column field="object" header="Object" body={objectTemplate}></Column>
            </DataTable>
        </div>
    );
};

export default SoftwareOntologyPage;
