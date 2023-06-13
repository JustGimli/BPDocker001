import "./App.scss";
import "bootstrap/dist/css/bootstrap.min.css";
import { Navigate, Route, Routes } from "react-router-dom";
import { All } from "./utils/Path";
import Error from "./pages/Error";
import { observer } from "mobx-react-lite";
import { useContext } from "react";
import { Context } from ".";

export const App = observer(() => {
    const { user } = useContext(Context);

    const renderRoutes = () => {
        return All.map(({ path, Component }) => (
            <Route key={path} path={path} element={<Component />} />
        ));
    };
    return (
        <Routes>
            {renderRoutes()}
            <Route path="/error" element={<Error />} />
            <Route path="*" element={<Navigate replace to="" />} />
        </Routes>
    );
});

export default App;
