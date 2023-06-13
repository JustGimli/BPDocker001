import { Container, Nav } from "react-bootstrap";
import { Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { hrefs } from "../../../utils/consts";
import { StatisticRoutes } from "../../../utils/Path";

export default function Stats() {
    const location = useLocation();
    const navigate = useNavigate();

    const handleNavLinks = (e: string | null) => {
        console.log(location.pathname);
        navigate(`/profile/stats/${e}`);
        console.log(e);
    };

    return (
        <>
            <Container>
                <Nav variant="tabs" onSelect={handleNavLinks} fill>
                    {data.map((item, index) => (
                        <Nav.Item key={index}>
                            <Nav.Link
                                eventKey={hrefs[index]}
                                active={
                                    location.pathname ===
                                    `/profile/stats/${hrefs[index]}`
                                        ? true
                                        : false
                                }
                            >
                                {item}
                            </Nav.Link>
                        </Nav.Item>
                    ))}
                </Nav>
            </Container>
            <Routes>
                {StatisticRoutes.map(({ path, Component }, index) => (
                    <Route element={<Component />} key={index} path={path} />
                ))}
            </Routes>
        </>
    );
}

const data = [
    "Общая статистика",
    "Статистика консультаций",
    "Статистика оплат",
    "Взаимодействие с пользователями",
];
