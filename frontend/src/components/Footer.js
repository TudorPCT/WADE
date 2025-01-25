import React from 'react';

const Footer = () => {
    const linkStyle = {
        textDecoration: "none",
    }

    const style = {
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
    }

    return (
        <footer style={style}>
            <p className="p-text-secondary">© 2025 Faculty Of Computer Science Iași - WADE. All rights reserved.</p>
            <a className="p-text-secondary" href="https://www.freepik.com/free-vector/blue-polygon-dark-background_16398424.htm" style={linkStyle}>Image by rawpixel.com on Freepik</a>
        </footer>
    );
};

export default Footer;
