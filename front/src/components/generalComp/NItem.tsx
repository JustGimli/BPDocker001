import { Col, Container, Row } from "react-bootstrap";
import { SmileBot } from "../Profile/MyBots/components/img/smiileBot";

interface IProp {
    text: string;
}

export const NItem = ({ text }: IProp) => {
    return (
        <Container className="position-absolute top-50 start-50 translate-middle">
            <Row>
                <Col>
                    <Container className="d-flex justify-content-center">
                        <SmileBot />
                    </Container>
                </Col>
            </Row>
            <Row>
                <Container className="d-flex justify-content-center">
                    {text}
                </Container>
            </Row>
        </Container>
    );
};
