import { Container, Form } from "react-bootstrap";
import { $api } from "../../../../utils/api/api";
import Chats from "../../../../store/Chats";
import { useRef } from "react";

interface IProp {
    socketRef: React.RefObject<WebSocket | null>;
}

export const FormInput = ({ socketRef }: IProp) => {
    const formControl = useRef<any>();

    const sendData = (message: string) => {
        if (
            socketRef.current &&
            socketRef.current.readyState === WebSocket.OPEN
        ) {
            console.log("SEND DATA");
            socketRef.current.send(
                JSON.stringify({
                    type: "message",

                    data: {
                        message: message,
                        time: new Date(),
                        is_author: true,
                    },
                    chat_id: Chats.getCurrent()?.chat_id,
                })
            );
        }
    };

    const handleSubmit = (e: any) => {
        e.preventDefault();

        const FetchData = async () => {
            try {
                sendData(formControl.current.value);

                if (formControl.current !== null) {
                    formControl.current!.value = "";
                }
            } catch (error) {
                console.log(error);
            }
        };

        FetchData();
    };

    return (
        <Form onSubmit={handleSubmit}>
            <Container>
                <Form.Control
                    ref={formControl}
                    placeholder="Введите сообщение"
                ></Form.Control>
            </Container>
        </Form>
    );
};
