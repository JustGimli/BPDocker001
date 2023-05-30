import { Col, Container, Row } from "react-bootstrap";
import ProfileHeader from "../../components/Profile/ProfileHeader";
import ProfileMenu from "../../components/Profile/ProfileMenu";
import { Route, Routes } from "react-router-dom";
import { ProfileRoutes } from "../../utils/Path";
import { useMediaQuery } from "react-responsive";

export const Profile = () => {
    const isMobile = useMediaQuery({ maxWidth: 767 });

    return (
        <Container
            fluid
            className={"m-0 p-0 h-100"}
            style={{
                backgroundColor: "#F9FAFC",
                overflow: !isMobile ? "hidden" : "",
            }}
        >
            <ProfileHeader />
            <Container className="h-100 d-flex m-0 p-0" fluid>
                <Row>
                    <Col>
                        <ProfileMenu />
                    </Col>
                </Row>
                <Row
                    className={`d-block mt-4 ${
                        isMobile ? "mx-2" : "mx-5"
                    }  pt-3 w-75`}
                >
                    <Routes>
                        {ProfileRoutes.map(({ path, Component }) => (
                            <Route
                                key={path}
                                path={path}
                                element={<Component />}
                            />
                        ))}
                    </Routes>
                </Row>
            </Container>
        </Container>
    );
};
