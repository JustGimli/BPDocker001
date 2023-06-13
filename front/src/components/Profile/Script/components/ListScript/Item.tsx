import { Col, Container, Row, Badge } from "react-bootstrap";

interface IProp {
    name: string;
    scripts: Array<string>;
    date_update: string;
    is_active: boolean;
}

export const ItemScript = ({
    name,
    scripts,
    date_update,
    is_active,
}: IProp) => {
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

    return (
        <Container
            className="Item-Bot d-flex flex-column p-0 mt-5"
            style={{ backgroundColor: "#FFFFFF" }}
        >
            <Row className="px-2 pt-2">
                <Col>
                    {is_active ? (
                        <Badge bg="primary text-white">MedBotTest</Badge>
                    ) : (
                        <Badge
                            bg="text-white"
                            className="p-2"
                            style={{ background: "#D67300" }}
                        >
                            Сценарий не опубликован
                        </Badge>
                    )}
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
            <Row className="">
                <Col
                    className="mx-auto"
                    style={{
                        overflowWrap: "break-word",
                        inlineSize: "300px",
                    }}
                >
                    <ul>
                        {scripts.map((script, index) => (
                            <li className="text-primary" key={index}>
                                {script}
                            </li>
                        ))}
                    </ul>
                </Col>
            </Row>
            <Container className="mt-auto pe-0">
                <Row className="w-100 pb-1 ">
                    <Col>
                        <Col style={{ fontSize: "12px" }}>Отредактировано</Col>
                        <Col style={{ fontSize: "12px" }}>
                            {convertedDateTime}
                        </Col>
                    </Col>

                    <Col className="d-flex justify-content-end p-0">
                        <img src={require("./img/params.png")} alt="toolbar" />
                    </Col>
                </Row>
            </Container>
        </Container>
    );
};
