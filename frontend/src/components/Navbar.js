import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav>
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/login">Login</Link></li>
                <li><Link to="/signup">Signup</Link></li>
                <li><Link to="/preferences">Preferences</Link></li>
                <li><Link to="/search">Search</Link></li>
            </ul>
        </nav>
    );
};

export default Navbar;
