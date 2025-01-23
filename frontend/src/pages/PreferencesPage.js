import React, { useState, useEffect } from 'react';
import { getPreferences, updatePreferences } from '../services/preferencesService';

const PreferencesPage = () => {
    const [preferences, setPreferences] = useState({});
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchPreferences = async () => {
            try {
                const data = await getPreferences();
                setPreferences(data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchPreferences();
    }, []);

    const handleInputChange = (e) => {
        setPreferences({ ...preferences, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await updatePreferences(preferences);
            setMessage('Preferences updated successfully!');
        } catch (error) {
            setMessage('Failed to update preferences!');
            console.error(error);
        }
    };

    return (
        <div vocab="http://schema.org/" typeof="schema:WebPage">
            <header typeof="schema:WebSite">
                <h1 property="schema:name">Preferences Page</h1>
            </header>
            <main typeof="schema:Action">
                <form onSubmit={handleSubmit} typeof="schema:UpdateAction">
                    <label>
                        Theme:
                        <input
                            type="text"
                            name="theme"
                            value={preferences.theme || ''}
                            onChange={handleInputChange}
                            property="schema:identifier"
                        />
                    </label>
                    <label>
                        Notifications:
                        <input
                            type="text"
                            name="notifications"
                            value={preferences.notifications || ''}
                            onChange={handleInputChange}
                            property="schema:identifier"
                        />
                    </label>
                    <button type="submit" property="schema:actionStatus">Save</button>
                </form>
                <p property="schema:result">{message}</p>
            </main>
        </div>
    );
};

export default PreferencesPage;
