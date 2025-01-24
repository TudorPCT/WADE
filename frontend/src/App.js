import React, {useEffect, useState} from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Header from './components/header/Header';
import Footer from './components/Footer';
import 'primereact/resources/themes/lara-light-indigo/theme.css'; // or another theme
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import {useAuth} from "./core/AuthProvider";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const App = () => {
    const [loading, setLoading] = useState(true);
    const auth = useAuth();

    useEffect(() => {

        if (!auth.hasToken()) {
            return setLoading(false);
        }

        auth
            .validateToken()
            .finally(() => {
                setLoading(false);
            });
    }, [auth]);

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <Router>
            <Header />
            <Routes>
                <Route path="/" element={<h1>Welcome to the App</h1>} />
            </Routes>
            <Footer />
            <ToastContainer position="bottom-right"/>
        </Router>
    );
};

export default App;
