import axios from "axios";

export const setupAuthInterceptors = () => {
    axios.defaults.baseURL = process.env.REACT_APP_API_URL || "http://127.0.0.1:5000/api";

    axios.interceptors.request.use(
        (config) => {

            const token = localStorage.getItem("token");

            if (token) {
                config.headers["Authorization"] = `Bearer ${token}`;
            }

            return config;
        },
        (error) => {
            return Promise.reject(error);
        }
    );

    axios.interceptors.response.use(
        (response) => {
            return response;
        },
        (error) => {
            if (error.response?.status === 401) {
                localStorage.removeItem("token");
                window.location.href = "/";
            }
            return Promise.reject(error);
        }
    );
};
