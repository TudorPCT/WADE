import React, {useEffect, useState} from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Header from './components/header/Header';
import Footer from './components/Footer';
import 'primereact/resources/themes/lara-dark-cyan/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import {useAuth} from "./core/AuthProvider";
import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import {ProgressSpinner} from 'primereact/progressspinner';
import Background from './assets/v796-nunny-02.jpg';
import SearchPage from './pages/SearchPage';
import PreferencesPage from './pages/PreferencesPage';
import SoftwareOntologyPage from './pages/SoftwareOntologyPage';

const App = () => {
    const [loading, setLoading] = useState(true);
    const auth = useAuth();
    const styleSpinner = {
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        width: "100vw",
        position: "fixed",
        top: 0,
        left: 0,
        backgroundColor: "rgba(255, 255, 255, 0.8)",
        zIndex: 9999,
    };

    const style = {
        backgroundImage: `url(${Background})`,
        backgroundSize: "cover",
        backgroundPosition: "bottom left",
        backgroundRepeat: "no-repeat",
        backgroundAttachment: "fixed",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        minHeight: "100vh",
    }

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
        return <div style={styleSpinner}><ProgressSpinner/></div>
    }

    return (
        <div style={style}>
            <Router>
                <div style={{flexGrow: "100"}}>
                    <Header/>
                    <Routes>
                        <Route path="/" element={<h1>Welcome to the App</h1>}/>
                        <Route path="/search" element={<SearchPage/>}/>
                        <Route path="/saved" element={<PreferencesPage/>}/>
                        <Route path="/software-ontology" element={<SoftwareOntologyPage />} />
                    </Routes>
                </div>
                <Footer />
                <ToastContainer position="bottom-right"/>
            </Router>
        </div>
    );
};

export default App;
