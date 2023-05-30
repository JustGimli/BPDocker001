import "./App.scss";
import "bootstrap/dist/css/bootstrap.min.css";
import { Navigate, Route, Routes } from "react-router-dom";
import { privateRoutes, publicRoutes } from "./utils/Path";
import Error from "./pages/Error";
import { observer } from "mobx-react-lite";
import User from "./store/User";

export const App = observer(() => {
    const renderRoutes = () => {
        if (User.data.isAuth) {
            return privateRoutes.map(({ path, Component }) => (
                <Route key={path} path={path} element={<Component />} />
            ));
        } else {
            return publicRoutes.map(({ path, Component }) => (
                <Route key={path} path={path} element={<Component />} />
            ));
        }
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
