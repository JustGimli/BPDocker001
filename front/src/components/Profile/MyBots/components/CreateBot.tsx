import {
    Badge,
    Button,
    Col,
    Container,
    Image,
    ProgressBar,
    Row,
} from "react-bootstrap";
import NewBot from "./createBot/NewBot";
import Greeting from "./createBot/Greeting";
import Token from "./createBot/Token";
import Setting from "./createBot/Setting";
import { useState } from "react";
import { AiFillCheckCircle, AiOutlineRight } from "react-icons/ai";

export const CreateBot = () => {
    const [activeComponent, setActiveComponent] = useState<any>("Setting");
    const [bar1, setBar1] = useState(0);
    const [bar2, setBar2] = useState(0);
    const [bar3, setBar3] = useState(0);

    const handleClick = () => {
        if (activeComponent === "Setting") {
            setActiveComponent("Token");
            setBar1(100);
        } else if (activeComponent === "Token") {
            setActiveComponent("Greeting");
            setBar2(100);
        } else if (activeComponent === "Greeting") {
            setActiveComponent("NewBot");
            setBar3(100);
        }
    };

    let componentToRender;

    if (activeComponent === "Setting") componentToRender = <Setting />;
    else if (activeComponent === "Token") componentToRender = <Token />;
    else if (activeComponent === "Greeting") componentToRender = <Greeting />;
    else if (activeComponent === "NewBot") componentToRender = <NewBot />;

    return (
        <>
            <Container
                className="rounded"
                style={{
                    boxShadow: "0px 2px 5px rgba(0, 0, 0, 0.3)",
                    backgroundColor: "#FFFFFF",
                }}
            >
                <Row>
                    <Col className="fs-5">Создание Telegram-бота</Col>
                </Row>
                <Container className="d-flex align-items-center py-4">
                    <Badge
                        pill
                        bg=""
                        className="text-primary fs-6 border border-primary"
                    >
                        1
                    </Badge>
                    <ProgressBar
                        now={bar1}
                        variant="primary"
                        style={{ height: "3px", width: 130 }}
                    />
                    <Badge
                        pill
                        bg=""
                        className={
                            "fs-6 border border" +
                            (bar1 === 100 ? "-primary text-primary" : "")
                        }
                        style={{
                            color: bar1 === 100 ? "" : "grey",
                        }}
                    >
                        2
                    </Badge>
                    <ProgressBar
                        now={bar2}
                        variant="primary"
                        style={{ height: "3px", width: 130 }}
                    />
                    <Badge
                        pill
                        bg=""
                        className={
                            "fs-6 border border" +
                            (bar2 === 100 ? "-primary text-primary" : "")
                        }
                        style={{
                            color: bar2 === 100 ? "" : "grey",
                        }}
                    >
                        3
                    </Badge>
                    <ProgressBar
                        now={bar3}
                        variant="primary"
                        style={{ height: "3px", width: 130 }}
                    />
                    <AiFillCheckCircle
                        size={30}
                        color={activeComponent === "NewBot" ? "blue" : "grey"}
                        className="bi bi-check"
                    />
                </Container>
                <Row>
                    <Col md={8}>
                        {componentToRender}
                        {activeComponent !== "NewBot" ? (
                            <Button
                                variant="primary"
                                size="lg"
                                onClick={() => handleClick()}
                            >
                                Далее
                                <AiOutlineRight />
                            </Button>
                        ) : (
                            ""
                        )}
                    </Col>
                    <Col md={4} className="mt-auto">
                        <Image
                            alt="bot"
                            src={require("./img/BigBot.png")}
                            fluid
                        />
                    </Col>
                </Row>
            </Container>
        </>
    );
};
