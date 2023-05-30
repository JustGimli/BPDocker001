import React from "react";
import { Button, Col, Container, Form, Row } from "react-bootstrap";
import Bot from "../../../../../store/CreateBot";

export default function Greeting() {
    const handleInputChange = (e: any) => {
        Bot.addStartMes(e.target.value);
    };

    return (
        <Container>
            <Row>
                <Col>
                    Введите текст приветственного сообщения, которое бот будет
                    присылать своим новым подписчикам сразу после того как они
                    подпишутся на бота.
                </Col>
            </Row>
            <Form onSubmit={(e) => e.preventDefault()}>
                <Form.Group
                    controlId="formBasicEmail"
                    className="col-6 form-control-lg"
                >
                    <Form.Control
                        className="border border-dark"
                        type="text"
                        placeholder=" Привет! Я MedBot"
                        style={{ height: 210, width: 513 }}
                        onChange={handleInputChange}
                    />
                </Form.Group>
                <Button
                    className="border border-dark"
                    variant="black"
                    size="lg" /* onClick={(e) => sendDataToServer(e)} */
                >
                    Пропустить и настроить позже
                </Button>
            </Form>
        </Container>
    );
}
