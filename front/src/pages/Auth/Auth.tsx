import { Form, Button, Container, Row, Col } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import Preview from "../../components/Auth/Preview";
import { useContext, useEffect, useRef, useState } from "react";
import AuthHeader from "../../components/Auth/AuthHeader";
import { Context } from "../../index";
import { observer } from "mobx-react-lite";
import { $api } from "../../utils/api/api";

interface ILogin {
    email: string;
    password: string;
}

export const AuthPage = observer((props: any) => {
    const [form, setForm] = useState<ILogin>({
        email: "",
        password: "",
    });
    const iptEmail = useRef<HTMLInputElement | null>(null);
    const iptPass = useRef<HTMLInputElement | null>(null);
    const navigate = useNavigate();
    const { user } = useContext(Context);

    useEffect(() => {
        async function FetchData() {
            if (localStorage.getItem("token")) {
                await user.checkAuth();
            }

            if (user.isAuth) {
                navigate("/profile");
            }
        }
        FetchData();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const handleForm = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        const { email, password } = form;

        if (email !== "" && password !== "") {
            await user.login(email, password);
        }

        if (user.isAuth) {
            try {
                const data = await $api.get("/projects");

                if (data.data.length === 0) {
                    try {
                        const data = await $api.post("/projects/create/");
                    } catch (err) {
                        console.log(err);
                    }
                }
            } catch (err) {
                console.log(err);
            }
            navigate("profile/");
        }

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
                                                    placeholder={
                                                        user.emailError
                                                            ? user.emailError
                                                            : "  Введите адрес электронной почты"
                                                    }
                                                    style={{
                                                        height: 56,
                                                    }}
                                                    name="email"
                                                    ref={iptEmail}
                                                    isInvalid={Boolean(
                                                        user.emailError
                                                    )}
                                                />
                                            </Form.Group>
                                        </div>
                                        <div className="mb-3">
                                            <Form.Group controlId="formBasicPassword">
                                                <Form.Label>Пароль</Form.Label>
                                                <Form.Control
                                                    name="password"
                                                    className="border border-primary"
                                                    type="password"
                                                    placeholder={
                                                        user.passwordError
                                                            ? user.passwordError
                                                            : "  Придумайте или введите свой пароль"
                                                    }
                                                    style={{ height: 56 }}
                                                    onChange={handleForm}
                                                    ref={iptPass}
                                                    isInvalid={Boolean(
                                                        user.passwordError
                                                    )}
                                                />

                                                {user.detail && (
                                                    <Form.Control.Feedback type="invalid">
                                                        {user.detail}
                                                    </Form.Control.Feedback>
                                                )}
                                            </Form.Group>

                                            <Row
                                                className={
                                                    user.detail
                                                        ? "pt-0"
                                                        : "pt-3"
                                                }
                                            >
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
});
