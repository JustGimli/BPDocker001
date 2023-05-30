import { Col, Container, Form, Row } from "react-bootstrap";
import Bot from "../../../../../store/CreateBot";
import React from "react";

export default function Token() {
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        Bot.addToken(e.target.value);
    };

    return (
        <Container>
            <Row>
                <Col className="fs-5">Настройка токена</Col>
            </Row>
            <Row>
                <Col>
                    Нового бота необходимо зарегистрировать в Telegram.
                    Перейдите в мессенджер Telegram, найдите там бота
                    @BotFather. Выполните в нём команду /newbot чтобы
                    зарегистрировать вашего бота и получить токен.
                </Col>
            </Row>
            <Form onSubmit={(e) => e.preventDefault()}>
                <Form.Group
                    controlId="formBasicEmail"
                    className="col-6 form-control-lg"
                >
                    <Form.Label>Токен</Form.Label>
                    <Form.Control
                        className="border border-dark"
                        type="text"
                        placeholder=" Введите токен"
                        onChange={handleInputChange}
                        style={{ height: 56 }}
                    />
                </Form.Group>
            </Form>
        </Container>
    );
}
