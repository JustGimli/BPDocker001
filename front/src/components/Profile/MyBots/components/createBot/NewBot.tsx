import { Button, Col, Container, Row } from "react-bootstrap";
import { $api } from "../../../../../utils/api/api";
import Bot from "../../../../../store/CreateBot";

export default function NewBot() {
    const handleClick = (e: any) => {
        e.preventDefault();
        Bot.send();

        const form = Bot.form;

        $api.post("bots/create/", form, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });
    };
    return (
        <Container>
            <Row>
                <Col>
                    Поздравляем, бот готов! Осталось совсем немного! Настройте
                    бота в разделе “Сценарий”, а также подключите рассылки при
                    необходимости
                </Col>
            </Row>
            <Button variant="dark" size="lg" onClick={handleClick}>
                Готово
            </Button>
        </Container>
    );
}
