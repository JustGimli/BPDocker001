import { Form, Button, Container, Col, Carousel, Row } from "react-bootstrap";
import { Link } from "react-router-dom";
import Preview from "../../components/Auth/Preview";
import { AiFillStar } from "react-icons/ai";
import AuthHeader from "../../components/Auth/AuthHeader";

export default function Recover() {
    return (
        <>
            <AuthHeader />
            <Container className="h-100" fluid>
                <Row className="h-100">
                    <Col className="d-none d-md-flex">{/* <Preview /> */}</Col>
                    <Col className="d-flex justify-content-center align-items-center">
                        <div className="form-container">
                            <p style={{ paddingTop: 10 }}>
                                <Link to="/" style={{ textDecoration: "none" }}>
                                    Авторизация
                                </Link>
                            </p>
                            <Form>
                                <h4>Забыли пароль?</h4>
                                <p>
                                    Не волнуйтесь, мы отправим вам инструкцию по
                                    его восстановлению.
                                </p>
                                <div
                                    className="mb-3"
                                    style={{ paddingTop: 40 }}
                                >
                                    <Form.Group controlId="formBasicEmail">
                                        <Form.Label>Email</Form.Label>
                                        <Form.Control
                                            className="border border-primary"
                                            type="email"
                                            placeholder="  Введите адрес электронной почты"
                                            style={{ height: 56 }}
                                        />
                                    </Form.Group>
                                </div>
                            </Form>
                            <div
                                className="mt-2"
                                style={{ textAlign: "center" }}
                            >
                                <Button variant="primary" size="lg">
                                    <Link
                                        to="/check"
                                        style={{
                                            color: "white",
                                            textDecoration: "none",
                                        }}
                                    >
                                        Восстановить пароль
                                    </Link>
                                </Button>
                            </div>
                        </div>
                    </Col>
                </Row>
            </Container>
        </>
    );
}
