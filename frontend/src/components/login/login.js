import React, { useState } from "react";
import { Dialog } from "primereact/dialog";
import { InputText } from "primereact/inputtext";
import { Button } from "primereact/button";
import { toast } from "react-toastify";

const OTPDialog = ({ authService, visible, onHide }) => {
    const [email, setEmail] = useState("");
    const [otp, setOtp] = useState("");
    const [step, setStep] = useState(1);

    const resetDialog = () => {
        setEmail("");
        setOtp("");
        setStep(1);
    }

    const handleSendOTP = async () => {
        if (!email) return;
        try {
            // if (await authService.generateOTP(email))
                setStep(2);
        } catch (error) {
            console.error("Error sending OTP:", error);
        }
    };

    const handleVerifyOTP = async () => {
        if (!otp) return;
        try {
            var result = await authService.login(email, otp);
            onHide();

            if (result){
                window.location.reload();
            }else{
                toast.error("Login failed! Please try again.");
            }
        } catch (error) {
            console.error("Error verifying OTP:", error);
        }
    };

    // Reset dialog states when hiding the dialog
    const handleHide = () => {
        resetDialog();
        onHide();
    };

    const renderDialogContent = () => {
        if (step === 1) {
            return (
                <div className="p-fluid">
                    <div className="field">
                        <label htmlFor="email" className="block mb-2">
                            Email
                        </label>
                        <InputText
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Enter your email"
                            className="w-full"
                        />
                    </div>
                </div>
            );
        } else {
            return (
                <div className="p-fluid">
                    <div className="field">
                        <label htmlFor="otp" className="block mb-2">
                            One-Time Password
                        </label>
                        <InputText
                            id="otp"
                            value={otp}
                            onChange={(e) => setOtp(e.target.value)}
                            placeholder="Enter the OTP sent to your email"
                            className="w-full"
                        />
                    </div>
                </div>
            );
        }
    };

    // Render different footer buttons depending on step
    const renderFooter = () => {
        if (step === 1) {
            return (
                <div>
                    <Button label="Cancel" icon="pi pi-times" onClick={handleHide} className="p-button-text" />
                    <Button label="Send OTP" icon="pi pi-check" onClick={handleSendOTP} autoFocus />
                </div>
            );
        } else {
            return (
                <div>
                    <Button label="Cancel" icon="pi pi-times" onClick={handleHide} className="p-button-text" />
                    <Button label="Verify OTP" icon="pi pi-check" onClick={handleVerifyOTP} autoFocus />
                </div>
            );
        }
    };

    return (
        <Dialog
            visible={visible}
            onHide={handleHide}
            header="Login"
            footer={renderFooter()}
            style={{ width: "30rem" }}
            modal
        >
            {renderDialogContent()}
        </Dialog>
    );
};

export default OTPDialog;
