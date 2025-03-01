import React, {useEffect, useState} from 'react';
import {useLocation, useNavigate} from 'react-router-dom';
import {DataTable} from 'primereact/datatable';
import {Column} from 'primereact/column';
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

    const handleLinkClick = (e, url) => {
        e.preventDefault();
        const newFragment = url.hash.substring(1);
        if (url.href.includes('/software-ontology')) {
            navigate(`/software-ontology?fragment=${newFragment}`);
        } else {
            window.open(url.href, '_blank', 'noopener,noreferrer');
        }
    };

    const getURL = (string) => {
        try {
            return new URL(string);
        } catch (_) {
            return false;
        }
    };

    const predicateTemplate = (rowData) => {
        return template(rowData.predicate);
    };

    const objectTemplate = (rowData) => {
        return template(rowData.object);
    };

    const template = (link) => {
        const url = getURL(link);
        if (url) {
            if (url.href.includes('/software-ontology')) {
                return (
                    <a href={url.href} onClick={(e) => handleLinkClick(e, url)}>
                        {url.hash.substring(1)}
                    </a>
                );
            }
            return (
                <a href={url.href} target="_blank" rel="noopener noreferrer">
                    {url.hash.substring(1)}
                </a>
            );
        }
        return <span>{link}</span>;
    };

    return (
        <div
            className="ontology-page"
            prefix="schema: http://schema.org/"
            typeof="schema:WebPage"
        >
            <h1
                className="ontology-title"
                property="schema:name"
            >
                Software Ontology - {fragment}
            </h1>

            <section
                property="schema:mainEntity"
                typeof="schema:ItemList"
            >
                <DataTable value={data} showGridlines>
                    <Column
                        field="predicate"
                        header="Predicate"
                        body={predicateTemplate}
                    />
                    <Column
                        field="object"
                        header="Object"
                        body={objectTemplate}
                    />
                </DataTable>
            </section>
        </div>
    );
};

export default SoftwareOntologyPage;
