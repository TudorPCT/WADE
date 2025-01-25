import React, { useState, useEffect, useRef } from "react";
import { Menu } from "primereact/menu";
import { Button } from "primereact/button";
import "./Header.css";
import OTPDialog from "../login/login";
import { useAuth } from "../../core/AuthProvider";
import { useNavigate } from "react-router-dom"; // Import useNavigate hook

const Header = () => {
    const [logoUrl] = useState("/logo.svg");
    const [logoAlt] = useState("Logo");
    const [title1] = useState("Code");
    const [title2] = useState("Owl");
    const [menuItems, setMenuItems] = useState([]);
    const menuRef = useRef(null); // Reference for the menu component
    const [showOTPDialog, setShowOTPDialog] = useState(false);
    const authService = useAuth();
    const navigate = useNavigate(); // Initialize useNavigate hook

    const handleDialogHide = () => {
        setShowOTPDialog(false);
    };

    const refreshMenuItems = () => {
        setMenuItems([
            {
                label: "Navigate",
                items: [
                    {
                        label: "Home",
                        icon: "pi pi-home",
                        command: () => navigate("/"), // Use navigate here
                    },
                    {
                        label: "Search",
                        icon: "pi pi-fw pi-search",
                        command: () => navigate("/search"), // Use navigate here
                    },
                    {
                        label: "Saved Searches",
                        icon: "pi pi-save",
                        command: () => navigate("/saved"), // Use navigate here
                    },
                ],
            },
            {
                label: "Options",
                items: [
                    authService.isAuthenticated()
                        ? {
                            label: "Logout",
                            icon: "pi pi-sign-out",
                            command: () => {
                                authService.logout();
                                window.location.reload();
                            },
                        }
                        : {
                            label: "Login",
                            icon: "pi pi-sign-in",
                            command: () => setShowOTPDialog(true),
                        },
                ],
            },
        ]);
    };

    useEffect(() => {
        refreshMenuItems(); // Initialize menu items
    }, [authService]);

    return (
        <div className="main">
            <div className="branding">
                <div className="logo-wrapper">
                    <img
                        id="logo"
                        src={logoUrl}
                        alt={logoAlt}
                        style={{ width: "80%", height: "auto", minWidth: "40px" }}
                    />
                </div>
                <h1>
                    <span className="branding-text p-text-secondary">{title1}</span>
                    <span className="branding-text p-text-secondary" style={{color: "rgb(34, 211, 238)"}}>{title2}</span>
                </h1>
            </div>

            <div className="nav">
                <Menu model={menuItems} popup ref={menuRef} />
                <Button
                    icon="pi pi-bars"
                    label="Menu"
                    onClick={(event) => menuRef.current.toggle(event)}
                />
            </div>
            <OTPDialog
                authService={authService}
                visible={showOTPDialog}
                onHide={handleDialogHide}
            />
        </div>
    );
};

export default Header;
