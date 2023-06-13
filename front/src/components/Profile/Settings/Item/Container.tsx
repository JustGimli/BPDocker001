import { useState } from "react";
import { Col, Container, Form, Row } from "react-bootstrap";
import Project from "../../../../store/Project";
import { observer } from "mobx-react-lite";

interface IItem {
    title: string;
    checked: boolean;
}

interface IProp {
    name: string;
    items: Array<IItem>;
    isRadioButton: boolean;
    checked?: boolean;
}

export const SettingsBox = observer(
    ({ name, items, isRadioButton, checked }: IProp) => {
        const handleChange = (e: any) => {
            const text = e.target.getAttribute("value");

            if (text === "Только на сообщения админов") {
                Project.setSendType("admin");
            } else if (text === "На все сообщения") {
                Project.setSendType("all");
            } else if (text === "В личных сообщениях бота") {
                Project.setReportMessageType("private");
            } else if (text === "Во всех чатах") {
                Project.setReportMessageType("all");
            } else if (text === "С опубликованной версией проекта") {
                Project.setAdminSendType("published");
            } else if (text === "С неопубликованной версией проекта") {
                Project.setAdminSendType("unpublished");
            }
        };

        const handleChecked = (e: any) => {
            const text = e.target.getAttribute("name");
            if (text && text === "Бот включен и будет отвечать") {
                Project.setIsActive(!Project.project?.is_active);
            } else if (
                text &&
                text ===
                    "Выводить отладочные сообщения администратору при общении"
            ) {
                Project.setReportMessage(!Project.project?.report_message);
            }
        };

        return (
            <Container
                className="p-3"
                style={{
                    height: "190px",
                    width: "400px",
                    boxShadow: "0px 2px 5px rgba(0, 0, 0, 0.3)",
                    borderRadius: "10px",
                }}
            >
                <Row>
                    <Col>
                        {isRadioButton && (
                            <Form.Check
                                label={name}
                                name={name}
                                type="checkbox"
                                className="fw-bold"
                                checked={checked}
                                onClick={handleChecked}
                            />
                        )}
                        {!isRadioButton && (
                            <Container fluid className="fw-bold p-0 m-0">
                                {name}
                            </Container>
                        )}
                    </Col>
                </Row>
                <Container className="p-3">
                    {items.map((item, ind) => (
                        <Form.Check
                            key={ind}
                            label={item.title}
                            type="radio"
                            name={name}
                            value={item.title}
                            checked={item.checked}
                            onChange={handleChange}
                            className={`fw-light  ${
                                item.checked ? "text-primary" : "text-secondary"
                            }`}
                        />
                    ))}
                </Container>
            </Container>
        );
    }
);
