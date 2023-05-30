import { Container, Navbar } from "react-bootstrap";
import { Logo } from "../../imgs/Logo";

export default function AuthHeader() {
    return (
        <Navbar bg="ligth" className="position-absolute m-2">
            <Container>
                <Navbar.Brand>
                    <Logo />
                </Navbar.Brand>
            </Container>
        </Navbar>
    );
}
