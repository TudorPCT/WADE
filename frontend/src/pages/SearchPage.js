import React, { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { useAuth } from "../core/AuthProvider";
import { useNavigate, useLocation } from 'react-router-dom';
import './SearchPage.css';
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

const SearchPage = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const authService = useAuth();
    const isAuthenticated = authService.isAuthenticated();
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const searchQuery = params.get('query');
        if (searchQuery) {
            setQuery(searchQuery);
            fetchResults(searchQuery);
        }
    }, [location.search]);

    const fetchResults = async (searchQuery) => {
        try {
            const response = await fetch(`${API_URL}/api/search`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_input: searchQuery })
            });
            const data = await response.json();
            setResults(data.results.bindings);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleInputChange = (event) => {
        setQuery(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        navigate(`/search?query=${encodeURIComponent(query)}`);
    };

    const handleSaveSearch = () => {
        axios.post(`${API_URL}/api/preferences`, { key: 'search', value: query })
            .then(() => console.log('Search saved successfully'))
            .catch(error => console.error('Error saving search:', error));
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

    const renderFragment = (rowData) => {
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
        return fragment;
    };

    return (
        <div className="search-page">
            {results.length === 0 && <h1 className="search-page-title">Search Page</h1>}
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
                <DataTable value={results} showGridlines>
                    <Column body={renderFragment} header="Individual" />
                    <Column body={renderButton} header="Action" />
                </DataTable>
            )}
        </div>
    );
};

export default SearchPage;