import { Button, Col, Container, Form, Row } from "react-bootstrap";
import { SettingsBox } from "./Container";
import { observer } from "mobx-react-lite";
import Project from "../../../../store/Project";

export const SettingsItem = observer(() => {
    const hard = [
        {
            name: "Бот включен и будет отвечать",
            items: [
                {
                    title: "На все сообщения",
                    checked: Project.project?.send_type === "all",
                },
                {
                    title: "Только на сообщения админов",
                    checked: Project.project?.send_type === "admin",
                },
            ],
            isRadioButton: true,
            checked: Project.project?.is_active,
        },

        {
            name: "Выводить отладочные сообщения администратору при общении",
            items: [
                {
                    title: "В личных сообщениях бота",
                    checked: Project.project?.report_message_type === "private",
                },
                {
                    title: "Во всех чатах",
                    checked: Project.project?.report_message_type === "all",
                },
            ],
            isRadioButton: true,
            checked: Project.project?.report_message === true,
        },
        {
            name: "Администратор общается",
            items: [
                {
                    title: "С опубликованной версией проекта",
                    checked: Project.project?.admin_send_type === "published",
                },

                {
                    title: "С неопубликованной версией проекта",
                    checked: Project.project?.admin_send_type === "unpublished",
                },
            ],

            isRadioButton: false,
        },
    ];

    return (
        <Container
            className="p-4"
            style={{
                boxShadow: "0px 2px 5px rgba(0, 0, 0, 0.3)",
                backgroundColor: "#FFFFFF",
                borderRadius: "10px",
            }}
            fluid
        >
            <Row className="my-1">
                <Col
                    className="fw-bold"
                    style={{ fontWeight: "500", fontSize: "18px" }}
                >
                    Настройки проекта
                </Col>
            </Row>
            <Row className="my-2">
                <Col className="fw-light" style={{ fontSize: "16px" }}>
                    {Project.project?.name || "Новый проект"}
                </Col>
            </Row>
            <Row className="mb-3">
                <Col className="fw-bold" style={{ fontSize: "14px" }}></Col>
            </Row>
            <Row>
                <Col className="fw-light mb-4">Режим работы проекта</Col>
            </Row>
            <Container className="d-flex justify-content-around flex-row flex-wrap mb-5">
                {hard.map((obj, ind) => (
                    <SettingsBox
                        key={ind}
                        name={obj.name}
                        items={obj.items}
                        isRadioButton={obj.isRadioButton}
                        checked={obj.checked}
                    />
                ))}
            </Container>
            <Row>
                <Col>Часовой пояс</Col>
            </Row>
            <Form.Select className="border border-primary w-25 mb-5">
                <option value="option1">Europe/Moscow</option>
                <option value="option1">Europe/Minsk</option>
            </Form.Select>
            <Row>
                <Col>Удаление проекта</Col>
            </Row>
            <Button className="bg-danger">Удалить проект</Button>
        </Container>
    );
});
