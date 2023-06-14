import { Col, Container, Nav, Row } from "react-bootstrap";
import { NavLink } from "react-router-dom";

export const HeaderMenu = () => {
    return (
        <Nav
            className="flex-column text-center"
            style={{
                height: "91vh",
                boxShadow: "0px 2px 5px rgba(0, 0, 0, 0.3)",
                backgroundColor: "#FFFFFF",
            }}
            justify
        >
            <Container fluid className="mt-2">
                {arrayText.map((obj, ind) => (
                    <Container fluid className="h-auto" key={ind}>
                        <NavLink
                            to={`/profile/${obj.name}`}
                            style={({ isActive, isPending }) => {
                                return {
                                    textDecoration: "none",
                                    color: isActive ? "#4457FF" : "#7B7A83",
                                };
                            }}
                        >
                            <Row>
                                <Col name={obj.name}>
                                    <img
                                        src={require(`./${obj.name}.png`)}
                                        alt={`${obj.name}`}
                                    ></img>
                                </Col>
                            </Row>
                            <Row>
                                <Col name={obj.name}>{obj.label}</Col>
                            </Row>
                        </NavLink>
                    </Container>
                ))}
            </Container>
        </Nav>
    );
};

const arrayText = [
    {
        name: "bot",
        label: "Мои боты",
    },
    {
        name: "script",
        label: "Сценарий",
    },
    {
        name: "mail",
        label: "Рассылки",
    },
    {
        name: "answer",
        label: "Быстрые ответы",
    },
    {
        name: "chats",
        label: "Чаты",
    },
    {
        name: "channel",
        label: "Каналы",
    },
    {
        name: "stats",
        label: "Статистика",
    },
    {
        name: "integrations",
        label: "Интеграции",
    },
    {
        name: "settings",
        label: "Настройки",
    },
];
