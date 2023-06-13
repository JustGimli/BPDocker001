import { Container } from "react-bootstrap";
import { Link } from "react-router-dom";
import Chats from "../../../../store/Chats";
import { observer } from "mobx-react-lite";
// import Chats from "../../../../store/Chats";

interface IProp {
    id: number;
    name: string | number;
    lastMessage?: string;
    index: number;
}

export const ChatItem = observer(({ name, lastMessage, id, index }: IProp) => {
    const handleClick = () => {
        Chats.setCurrent(index);
    };

    return (
        <Container className="p-2 border-bottom">
            <Link
                to={id.toString()}
                onClick={handleClick}
                className="d-flex justify-content-between"
            >
                <Container className="d-flex flex-row">
                    <Container>
                        <img
                            src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp"
                            alt="avatar"
                            className="d-flex align-self-center me-3"
                            width="60"
                        />
                        <span className="badge bg-success badge-dot"></span>
                    </Container>
                    <Container className="pt-1">
                        <p className="fw-bold mb-0">{name}</p>
                        <p className="small text-muted">{}</p>
                    </Container>
                </Container>
                {/* <Container className="pt-1">
                <p className="small text-muted mb-1">Just now</p>
                <span className="badge bg-danger rounded-pill float-end">
                    3
                </span>
            </Container> */}
            </Link>
        </Container>
    );
});
