import { Badge, Col, Container, Nav, NavDropdown, Row } from "react-bootstrap";
import { AiOutlineExclamationCircle } from "react-icons/ai";
import { GrDocumentText } from "react-icons/gr";
import { useMediaQuery } from "react-responsive";

export const MainBar = () => {
    const isDesktop = useMediaQuery({ minWidth: 1090 });
    const isTablet = useMediaQuery({ minWidth: 768, maxWidth: 1090 });
    const isMobile = useMediaQuery({ maxWidth: 767 });
    return (
        <>
            {(isDesktop || isTablet) && (
                <Container fluid>
                    <Row>
                        <Col>
                            <Nav>
                                <Row className="d-block">
                                    <Col>
                                        <Nav.Item className="px-2">
                                            проект
                                        </Nav.Item>
                                    </Col>
                                    <Col>
                                        <NavDropdown
                                            title="Новый проект"
                                            id="collasible-nav-dropdown"
                                        >
                                            <NavDropdown.Item href="#action/3.1">
                                                ActisTabletion
                                            </NavDropdown.Item>
                                            <NavDropdown.Divider />
                                            <NavDropdown.Item href="#action/3.2">
                                                Another action
                                            </NavDropdown.Item>
                                        </NavDropdown>
                                    </Col>
                                </Row>
                            </Nav>
                        </Col>
                        <Col>
                            <Container
                                fluid
                                className="d-flex align-items-center "
                            >
                                <Row className="m-1">
                                    <Col>
                                        <Badge
                                            pill
                                            bg="warning"
                                            className="fs-6  text-light d-flex align-items-center"
                                        >
                                            <AiOutlineExclamationCircle
                                                size={36}
                                            />
                                            {isDesktop && (
                                                <Row>
                                                    <Col>
                                                        ИЗМЕНЕНИЯ НЕ
                                                        ОПУБЛИКОВАНЫ
                                                    </Col>
                                                </Row>
                                            )}
                                        </Badge>
                                    </Col>
                                </Row>
                                <Nav>
                                    <Row className="d-block mx-2 text-center">
                                        <Col>
                                            <GrDocumentText size={25} />
                                        </Col>
                                        <Col>
                                            <Nav.Link href="">
                                                Документация
                                            </Nav.Link>
                                        </Col>
                                    </Row>
                                </Nav>
                                <Row className="d-block ">
                                    <Col>
                                        <img
                                            alt="russianFlag"
                                            src={require("./russianFlag.png")}
                                        />
                                    </Col>
                                    Русский
                                </Row>
                            </Container>
                        </Col>
                    </Row>
                </Container>
            )}
        </>
    );
};
