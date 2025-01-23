import React, { useState } from 'react';
import { login } from '../services/authService';

const LoginPage = () => {
    const [credentials, setCredentials] = useState({ username: '', password: '' });
    const [message, setMessage] = useState('');

    const handleInputChange = (e) => {
        setCredentials({ ...credentials, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await login(credentials);
            setMessage('Login successful!');
            console.log(response);
        } catch (error) {
            setMessage('Login failed!');
            console.error(error);
        }
    };

    return (
        <div vocab="http://schema.org/" typeof="schema:WebPage">
            <header typeof="schema:WebSite">
                <h1 property="schema:name">Login Page</h1>
            </header>
            <main typeof="schema:Action">
                <form onSubmit={handleSubmit} typeof="schema:PerformAction">
                    <label>
                        Username:
                        <input
                            type="text"
                            name="username"
                            placeholder="Username"
                            value={credentials.username}
                            onChange={handleInputChange}
                            required
                            property="schema:identifier"
                        />
                    </label>
                    <label>
                        Password:
                        <input
                            type="password"
                            name="password"
                            placeholder="Password"
                            value={credentials.password}
                            onChange={handleInputChange}
                            required
                            property="schema:password"
                        />
                    </label>
                    <button type="submit" property="schema:actionStatus">Login</button>
                </form>
                <p property="schema:result">{message}</p>
            </main>
        </div>
    );
};

export default LoginPage;
