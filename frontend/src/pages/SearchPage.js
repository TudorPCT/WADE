import React, { useState } from 'react';
import { searchOntologies } from '../services/ontologyService';

const SearchPage = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = async () => {
        try {
            const data = await searchOntologies(query);
            setResults(data);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div vocab="http://schema.org/" typeof="schema:SearchResultsPage">
            <header typeof="schema:WebSite">
                <h1 property="schema:name">Search Page</h1>
            </header>
            <main typeof="schema:SearchAction">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search..."
                    property="schema:query"
                />
                <button onClick={handleSearch} property="schema:actionStatus">Search</button>
                <ul>
                    {results.map((result, index) => (
                        <li key={index} typeof="schema:Thing">
                            <span property="schema:name">{result.name}</span>
                        </li>
                    ))}
                </ul>
            </main>
        </div>
    );
};

export default SearchPage;
