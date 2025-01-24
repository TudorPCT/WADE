import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000/api";

class AuthService {
    constructor() {
        this.authenticated = false;
        this.token = localStorage.getItem("token");
    }

    async login(email, otp) {
        const requestPath = `${API_URL}/auth/login`;
        const response = await axios.post(requestPath, { email, otp });
        localStorage.setItem("token", response.data.jwt);
        this.authenticated = true;
        this.token = response.data.jwt;
        window.location.reload();
        return response;
    }

    logout() {
        localStorage.removeItem("token");
        this.authenticated = false;
        this.token = null;
    }

    async validateToken() {
        const requestPath = `${API_URL}/auth/validate`;
        try {
            await axios.get(requestPath);
            this.authenticated = true;
            return true;
        } catch (error) {
            this.logout();
            return false;
        }
    }

    isAuthenticated() {
        return this.authenticated;
    }

    hasToken() {
        return this.token !== null;
    }

    async generateOTP(email) {
        const requestPath = `${API_URL}/auth/generate-password`;
        try {
            await axios.post(requestPath, { email });
            return true;
        } catch (error) {
            return false;
        }
    }
}

export default new AuthService();
