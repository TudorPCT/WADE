import React, { useState } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { useAuth } from "../core/AuthProvider";
import { useNavigate } from 'react-router-dom';
import './SearchPage.css';

const SearchPage = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const authService = useAuth();
    const isAuthenticated = authService.isAuthenticated();
    const navigate = useNavigate();

    const handleInputChange = (event) => {
        setQuery(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch('http://127.0.0.1:5000/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_input: query }),
            });
            const data = await response.json();
            setResults(data.results.bindings);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleSaveSearch = () => {
        console.log('Search saved:', query);
    };

    const renderButton = (rowData) => {
        let fragment = '';
        if (rowData && rowData.indiv && rowData.indiv.value) {
            try {
                const fullUri = rowData.indiv.value;
                fragment = fullUri.split('#')[1] || '';
            } catch (e) {
                console.error('Error extracting fragment:', e);
            }
        } else {
            console.error('indiv.value not found in rowData');
        }

        const handleNavigation = () => {
            const url = `/software-ontology?fragment=${fragment}`;
            navigate(url);
        };

        return (
            <button onClick={handleNavigation}>
                Open Fragment
            </button>
        );
    };

    return (
        <div className="search-page">
            <h1 className="search-page-title">Search Page</h1>
            <form className="search-form" onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={query}
                    onChange={handleInputChange}
                    placeholder="Enter your search query"
                    className="search-input"
                />
                <button type="submit" className="search-button">Search</button>
                {isAuthenticated && (
                    <button type="button" className="save-button" onClick={handleSaveSearch}>Save Search</button>
                )}
            </form>
            {results.length > 0 && (
                <DataTable value={results} showGridlines tableStyle={{ minWidth: '50rem' }}>
                    <Column field="indiv.value" header="Individual" />
                    <Column body={renderButton} header="Action" />
                </DataTable>
            )}
        </div>
    );
};

export default SearchPage;
