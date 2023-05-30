import React, { useState } from "react";
import { Card, Col, Container, Navbar, Row } from "react-bootstrap";
import { Logo } from "../../imgs/Logo";
import { HiMenu } from "react-icons/hi";
import { MainBar } from "./ProfileHeader/mainBar";
import { useMediaQuery } from "react-responsive";
import { HeaderMenu } from "./ProfileM/Menu";

export default function ProfileHeader() {
    const isDesktop = useMediaQuery({ minWidth: 1090 });
    const isTablet = useMediaQuery({ minWidth: 768, maxWidth: 1090 });
    const isMobile = useMediaQuery({ maxWidth: 767 });
    const [isProfile, setisProfile] = useState<boolean>(false);

    const handleClick = () => {
        setisProfile(!isProfile);
    };

    return (
        <>
            <Navbar
                collapseOnSelect
                expand="md"
                style={{
                    height: 80,
                    boxShadow: "0px 2px 5px rgba(0, 0, 0, 0.3)",
                    backgroundColor: "#FFFFFF",
                }}
            >
                <Container fluid>
                    {(isTablet || isDesktop) && (
                        <Navbar.Brand style={isTablet ? { width: "10%" } : {}}>
                            <Logo />
                        </Navbar.Brand>
                    )}

                    <Col md={9} className="text-left">
                        <Container>
                            {(isDesktop || isTablet) && (
                                <Card>
                                    <Col>
                                        <MainBar />
                                    </Col>
                                </Card>
                            )}
                        </Container>
                        {isMobile && <HiMenu size={30} onClick={handleClick} />}
                    </Col>
                    <Col md={2}>
                        <Container fluid>
                            <Row>
                                <Col md={5}>
                                    {/* <Row>
                                    <Col
                                        className="text-muted"
                                        md={5}
                                        style={{ fontSize: "smaller " }}
                                    >
                                        Баланс кабинета
                                    </Col>
                                </Row>

                                <Row>
                                    <Col>0 R</Col>
                                </Row> */}
                                </Col>
                                {(isTablet || isDesktop) && (
                                    <Col>
                                        <img
                                            alt="doctor"
                                            src={require("./ProfileHeader/doctor.png")}
                                        ></img>
                                    </Col>
                                )}
                            </Row>
                        </Container>
                        {isMobile && (
                            <img
                                alt="doctor"
                                src={require("./ProfileHeader/doctor.png")}
                            ></img>
                        )}
                    </Col>
                </Container>
            </Navbar>

            {isProfile && (
                <Container
                    className="h-80 d-flex m-0 p-0"
                    style={{ zIndex: 99, position: "absolute" }}
                    fluid
                >
                    <HeaderMenu />
                </Container>
            )}
        </>
    );
}
