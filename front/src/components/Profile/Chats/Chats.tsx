import { Col, Container, Row } from "react-bootstrap";
import { ChatListComponent } from "./ChatList/ChatList";
import { Messages } from "./Messages/Messages";

export const Chats = () => {
    return (
        <Container className="p-0 m-0">
            <Row>
                <Col md={3} sm={6} className="d-none d-sm-block p-0 m-0">
                    <ChatListComponent />
                </Col>
                <Col>
                    <Messages />
                </Col>
            </Row>
        </Container>
    );
};
