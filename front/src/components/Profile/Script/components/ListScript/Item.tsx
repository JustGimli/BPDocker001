import { Col, Container, Row, Badge } from "react-bootstrap";

interface IProp {
    name: string;
    scripts: string;
}

export const ItemScrpt = ({ name, scripts }: IProp) => {
    return (
        <Container className="Item-Bot mr-auto">
            <Row>
                <Col>
                    <Badge bg="success text-white">
                        Сценарий не опубликован
                    </Badge>
                </Col>
            </Row>
            <Row className="mx-auto">
                <Col>{name}</Col>
            </Row>
            <Row>
                <Col>{scripts}</Col>
            </Row>
            <Container className="h-75 d-flex align-items-end">
                <Row className="w-100">
                    <Col>Отредактировано</Col>

                    <Col className="d-flex justify-content-end ">
                        <img src={require("../img/params.png")} alt="toolbar" />
                    </Col>
                </Row>
            </Container>
        </Container>
    );
};
