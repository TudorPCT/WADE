import React, { useState } from 'react';
import { signup } from '../services/authService';

const SignupPage = () => {
    const [formData, setFormData] = useState({ username: '', password: '', email: '' });
    const [message, setMessage] = useState('');

    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await signup(formData);
            setMessage('Signup successful!');
            console.log(response);
        } catch (error) {
            setMessage('Signup failed!');
            console.error(error);
        }
    };

    return (
        <div vocab="http://schema.org/" typeof="schema:WebPage">
            <header typeof="schema:WebSite">
                <h1 property="schema:name">Signup Page</h1>
            </header>
            <main typeof="schema:RegisterAction">
                <form onSubmit={handleSubmit}>
                    <label>
                        Username:
                        <input
                            type="text"
                            name="username"
                            placeholder="Username"
                            value={formData.username}
                            onChange={handleInputChange}
                            required
                            property="schema:identifier"
                        />
                    </label>
                    <label>
                        Email:
                        <input
                            type="email"
                            name="email"
                            placeholder="Email"
                            value={formData.email}
                            onChange={handleInputChange}
                            required
                            property="schema:email"
                        />
                    </label>
                    <label>
                        Password:
                        <input
                            type="password"
                            name="password"
                            placeholder="Password"
                            value={formData.password}
                            onChange={handleInputChange}
                            required
                            property="schema:password"
                        />
                    </label>
                    <button type="submit" property="schema:actionStatus">Signup</button>
                </form>
                <p property="schema:result">{message}</p>
            </main>
        </div>
    );
};

export default SignupPage;
