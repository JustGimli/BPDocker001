import { Form, Button, Container, Row, Col } from "react-bootstrap";
import { Link } from "react-router-dom";
import Preview from "../../components/Auth/Preview";
import CarouselHeader from "../../components/Auth/AuthHeader";

export default function CheckMailPage() {
    return (
        <>
            <CarouselHeader />
            <Container className="h-100">
                <Row className="h-100">
                    <Col className="d-none d-md-flex">{/* <Preview /> */}</Col>
                    <Col className="d-flex justify-content-center align-items-center">
                        <div className="login">
                            <div className="form-container">
                                <p style={{ paddingTop: 10 }}>
                                    <Link
                                        to="/recover"
                                        style={{ textDecoration: "none" }}
                                    >
                                        Ввод почты
                                    </Link>
                                </p>
                                <Form>
                                    <h4>Проверьте свою почту</h4>
                                    <p>
                                        Мы отправили вам письмо по
                                        восстановлению пароля на почту
                                        test@yandex.ru
                                    </p>
                                </Form>
                                <div
                                    className="mt-2"
                                    style={{ textAlign: "center" }}
                                >
                                    <Button variant="primary" size="lg">
                                        <Link
                                            to="/"
                                            style={{
                                                color: "white",
                                                textDecoration: "none",
                                            }}
                                        >
                                            Вернуться к авторизации
                                        </Link>
                                    </Button>
                                </div>
                                <p style={{ paddingTop: 40 }}>
                                    Не пришло письмо?{" "}
                                    <Link
                                        to=""
                                        className="ms-2"
                                        style={{ textDecoration: "none" }}
                                    >
                                        Отправить новое
                                    </Link>
                                </p>
                            </div>
                        </div>
                    </Col>
                </Row>
            </Container>
        </>
    );
}
