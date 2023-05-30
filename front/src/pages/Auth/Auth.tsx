import { Form, Button, Container, Row, Col } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import Preview from "../../components/Auth/Preview";
import { $api, $auth } from "../../utils/api/api";
import { useRef, useState } from "react";
import AuthHeader from "../../components/Auth/AuthHeader";
import User from "../../store/User";

interface ILogin {
    email: string;
    password: string;
}

export const AuthPage = (props: any) => {
    const [form, setForm] = useState<ILogin>({
        email: "",
        password: "",
    });
    const iptEmail = useRef<HTMLInputElement | null>(null);
    const iptPass = useRef<HTMLInputElement | null>(null);
    const navigate = useNavigate();

    const [emailError, setEmailError] = useState<boolean | undefined>();
    const [passwordError, setPasswordError] = useState<any>("");

    const handleForm = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        $auth
            .post("auth/users/", {
                email: form.email,
                password: form.password,
            })
            .then((respUser) => {
                $api.post("auth/jwt/create/", {
                    email: form.email,
                    password: form.password,
                }).then((resp) => {
                    User.setAuth(true);
                    User.setAsses(resp.data.access);
                    User.setRef(resp.data.refresh);
                });

                navigate("/profile", { replace: true });
            })
            .catch((er) => {
                const error = er.response.data;

                if (error.email) {
                    if (
                        error.email[0] ===
                        "user with this email already exists."
                    ) {
                        console.log("eror user exist");
                        $auth
                            .post("auth/jwt/create/", {
                                email: form.email,
                                password: form.password,
                            })
                            .then((resp) => {
                                User.setAuth(true);
                                User.setAsses(resp.data.access);
                                User.setRef(resp.data.refresh);
                                navigate("/profile", { replace: true });
                            })
                            .catch((error) => {
                                if (error.data.email) {
                                    setEmailError(error.data.email);
                                }
                            });
                    } else setEmailError(error.data.email);
                }

                if (error.password) {
                    setPasswordError(error.password[0]);
                }
            });

        setForm({
            email: "",
            password: "",
        });

        iptEmail.current!.value = "";
        iptPass.current!.value = "";
    };

    return (
        <>
            <AuthHeader />
            <Container className="h-100" fluid>
                <Row className="h-100">
                    <Col className="d-none d-md-flex mx-auto my-auto" md={6}>
                        <Preview />
                    </Col>
                    <Col className="mx-auto my-auto">
                        <Container fluid>
                            <Row className="justify-content-center">
                                <Col md={8}>
                                    <Form onSubmit={handleSubmit}>
                                        <h4>Создать аккаунт или войти</h4>
                                        <div
                                            className="mb-3"
                                            style={{ paddingTop: 40 }}
                                        >
                                            <Form.Group controlId="formBasicEmail">
                                                <Form.Label>Email</Form.Label>
                                                <Form.Control
                                                    onChange={handleForm}
                                                    className="border border-primary"
                                                    type="email"
                                                    placeholder="  Введите адрес электронной почты"
                                                    style={{ height: 56 }}
                                                    name="email"
                                                    ref={iptEmail}
                                                    isInvalid={emailError}
                                                />
                                                {emailError && (
                                                    <Form.Control.Feedback type="invalid">
                                                        {emailError}
                                                    </Form.Control.Feedback>
                                                )}
                                            </Form.Group>
                                        </div>
                                        <div className="mb-3">
                                            <Form.Group controlId="formBasicPassword">
                                                <Form.Label>Пароль</Form.Label>
                                                <Form.Control
                                                    name="password"
                                                    className="border border-primary"
                                                    type="password"
                                                    placeholder="  Придумайте или введите свой пароль"
                                                    style={{ height: 56 }}
                                                    onChange={handleForm}
                                                    ref={iptPass}
                                                    isInvalid={passwordError}
                                                />
                                                {passwordError && (
                                                    <Form.Control.Feedback type="invalid">
                                                        {passwordError}
                                                    </Form.Control.Feedback>
                                                )}
                                            </Form.Group>
                                            <Row className="pt-3">
                                                <Link
                                                    to="/recover"
                                                    style={{
                                                        textDecoration: "none",
                                                    }}
                                                >
                                                    Забыли пароль?
                                                </Link>
                                            </Row>
                                        </div>
                                        <div
                                            className="mt-2"
                                            style={{ textAlign: "center" }}
                                        >
                                            <Button
                                                variant="primary"
                                                size="lg"
                                                type="submit"
                                            >
                                                Создать аккаунт или войти
                                            </Button>
                                        </div>
                                    </Form>
                                </Col>
                            </Row>
                        </Container>
                    </Col>
                </Row>
            </Container>
        </>
    );
};
