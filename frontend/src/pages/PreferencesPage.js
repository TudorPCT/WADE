import React, {useEffect, useState} from 'react';
import {DataTable} from 'primereact/datatable';
import {Column} from 'primereact/column';
import {Button} from 'primereact/button';
import axios from "axios";
import {useNavigate} from 'react-router-dom';
import './PreferencesPage.css';

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000";

const PreferencesPage = () => {
    const [data, setData] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get(`${API_URL}/api/preferences?key=search`)
            .then(response => setData(response.data))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    const handleDelete = (id) => {
        axios.delete(`${API_URL}/api/preferences?id=${id}`)
            .then(() => {
                setData(prevData => prevData.filter(item => item.id !== id));
            })
            .catch(error => console.error('Error deleting data:', error));
    };

    const handleSearchRedirect = (value) => {
        navigate(`/search?query=${encodeURIComponent(value)}`);
    };

    const actionBodyTemplate = (rowData) => {
        return (
            <>
                <Button
                    label="Search"
                    onClick={() => handleSearchRedirect(rowData.value)}
                    className="p-button-primary"
                />
                <Button
                    label="Delete"
                    onClick={() => handleDelete(rowData.id)}
                    className="p-button-danger"
                />
            </>
        );
    };

    return (
        <div
            className="preferences-page"
            prefix="schema: http://schema.org/"
            typeof="schema:WebPage"
        >
            <h1 property="schema:name">Preferences</h1>

            <section property="schema:mainEntity" typeof="schema:ItemList">
                <DataTable value={data} showGridlines>
                    <Column field="id" header="ID"/>
                    <Column field="value" header="Value"/>
                    <Column body={actionBodyTemplate} header="Actions"/>
                </DataTable>
            </section>
        </div>
    );
};

export default PreferencesPage;
