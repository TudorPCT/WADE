import React from 'react';

const Footer = () => {
    const linkStyle = {
        textDecoration: "none",
    };

    const style = {
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
    };

    return (
        <footer
            style={style}
            prefix="schema: http://schema.org/"
            typeof="schema:WPFooter"
        >
            <p className="p-text-secondary" property="schema:text">
                © 2025 Faculty Of Computer Science Iași - WADE. All rights reserved.
            </p>
            <a
                className="p-text-secondary"
                href="https://www.freepik.com/free-vector/blue-polygon-dark-background_16398424.htm"
                style={linkStyle}
                property="schema:url"
                target="_blank"
                rel="noopener noreferrer"
            >
                Image by rawpixel.com on Freepik
            </a>
            <a
                className="p-text-secondary"
                href="https://wade-fe-b58b6efc1256.herokuapp.com/report/report.html"
                style={linkStyle}
                property="schema:url"
                target="_blank"
                rel="noopener noreferrer"
            >
                Documentation
            </a>
        </footer>
    );
};

export default Footer;
