import { Badge, Col, Container, Row } from "react-bootstrap";
import { SlPeople } from "react-icons/sl";

interface IBot {
    name: string;
    desc?: string;
    date_update: string;
}

export const ItemBot = ({ name, desc, date_update }: IBot) => {
    const convertDateTime = (isoDateTime: string) => {
        const date = new Date(isoDateTime);
        const options: Intl.DateTimeFormatOptions = {
            day: "numeric",
            month: "long",
            year: "numeric",
            hour: "numeric",
            minute: "numeric",
        };

        return date.toLocaleDateString("ru-RU", options);
    };

    const convertedDateTime = convertDateTime(date_update);
    // const isMobile = useMediaQuery({ maxWidth: 767 });

    return (
        <Container
            className="Item-Bot d-flex flex-column p-0 mt-5"
            style={{ backgroundColor: "#FFFFFF" }}
        >
            <Row>
                <Col>
                    <Badge bg="success text-white">MedBotTest</Badge>
                </Col>
                <Col>
                    <Badge>
                        123
                        <SlPeople />
                    </Badge>
                </Col>
            </Row>
            <Row className="my-4 mx-3">
                <Col
                    style={{
                        overflowWrap: "break-word",
                        inlineSize: "300px",
                    }}
                >
                    {name}
                </Col>
            </Row>
            <Row className="mx-auto">
                <Col
                    className="mx-auto"
                    style={{
                        overflowWrap: "break-word",
                        inlineSize: "300px",
                    }}
                >
                    {desc}
                </Col>
            </Row>
            <Container fluid className="mt-auto pe-0">
                <Row className="w-100 pb-1 ">
                    <Col>
                        <Col style={{ fontSize: "12px" }}>Отредактировано</Col>
                        <Col style={{ fontSize: "12px" }}>
                            {convertedDateTime}
                        </Col>
                    </Col>

                    <Col className="d-flex justify-content-end p-0">
                        <img src={require("../img/params.png")} alt="toolbar" />
                    </Col>
                </Row>
            </Container>
        </Container>
    );
};
