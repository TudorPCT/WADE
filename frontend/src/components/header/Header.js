import React, {useEffect, useRef, useState} from "react";
import {Menu} from "primereact/menu";
import {Button} from "primereact/button";
import "./Header.css";
import OTPDialog from "../login/login";
import {useAuth} from "../../core/AuthProvider";
import {useNavigate} from "react-router-dom";

const Header = () => {
    const [logoUrl] = useState("/logo.svg");
    const [logoAlt] = useState("Logo");
    const [title1] = useState("Code");
    const [title2] = useState("Owl");
    const [menuItems, setMenuItems] = useState([]);
    const menuRef = useRef(null);
    const [showOTPDialog, setShowOTPDialog] = useState(false);
    const authService = useAuth();
    const navigate = useNavigate();

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
                        command: () => navigate("/"),
                    },
                    {
                        label: "Search",
                        icon: "pi pi-fw pi-search",
                        command: () => navigate("/search"),
                    },
                    authService.isAuthenticated() && {
                        label: "Saved Searches",
                        icon: "pi pi-save",
                        command: () => navigate("/saved"),
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
        refreshMenuItems();
    }, [authService]);

    return (
        <header
            className="main"
            prefix="schema: http://schema.org/"
            typeof="schema:WPHeader"
        >
            <div className="branding">
                <div className="logo-wrapper">

                    <img
                        id="logo"
                        src={logoUrl}
                        alt={logoAlt}
                        style={{width: "80%", height: "auto", minWidth: "40px"}}
                        property="schema:logo"
                    />
                </div>

                <h1 property="schema:headline">
                    <span className="branding-text p-text-secondary">{title1}</span>
                    <span
                        className="branding-text p-text-secondary"
                        style={{color: "rgb(34, 211, 238)"}}
                    >
                        {title2}
                    </span>
                </h1>
            </div>

            <div
                className="nav"
                property="schema:hasPart"
                typeof="schema:SiteNavigationElement"
            >
                <Menu model={menuItems} popup ref={menuRef}/>
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
        </header>
    );
};

export default Header;
