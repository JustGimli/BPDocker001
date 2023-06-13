import React, { createContext } from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { BrowserRouter } from "react-router-dom";
import User from "./store/User";

interface State {
    user: User;
}

export const user = new User();

export const Context = createContext<State>({
    user,
});

const root = ReactDOM.createRoot(
    document.getElementById("root") as HTMLElement
);
root.render(
    <React.StrictMode>
        <BrowserRouter>
            <Context.Provider value={{ user }}>
                <App />
            </Context.Provider>
        </BrowserRouter>
    </React.StrictMode>
);
