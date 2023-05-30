import { Col, Container, Navbar, Row } from "react-bootstrap";
export default function Test() {
    return (
        <Navbar
            collapseOnSelect
            expand="md"
            style={{
                height: 80,
                boxShadow: "0px 2px 5px rgba(0, 0, 0, 0.3)",
                backgroundColor: "#FFFFFF",
            }}
        >
            <Container>
                {/* <Col>
                    <HiMenu />
                </Col> */}

                <Col>asd</Col>
            </Container>
        </Navbar>
    );
}
