import { Container, Row } from "react-bootstrap";
import { useEffect, useRef, useState } from "react";
import { IMessage } from "../../../../../utils/interface";
import { $api } from "../../../../../utils/api/api";
import Chats from "../../../../../store/Chats";
import { Message } from "./MessageItem";
import { observer } from "mobx-react-lite";
import { useInView } from "react-intersection-observer";
import { FormInput } from "../FormInput";

export const MessageList = observer(() => {
    const [next, setNext] = useState<string | null>(null);
    const [messages, setMessages] = useState<Array<IMessage> | null>(null);
    const [ref, inView, entry] = useInView({
        threshold: 1,
    });
    const list = useRef<any>(null);
    const socketRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        const chat = Chats.getCurrent();

        const FetchData = async () => {
            try {
                const response = await $api(`chats/messages/${chat?.chat_id}`);
                const data = response.data;
                setNext(data.next);
                setMessages(data.results);
                // list.current.scrollTop = list.current.scrollHeight;
            } catch (error) {
                console.log(error);
            }
        };

        if (chat) {
            FetchData();
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [Chats.current]);

    useEffect(() => {
        const FetchData = async () => {
            try {
                const response = await $api(`${next}`);
                const data = response.data;
                setNext(data.next);
                if (messages) {
                    setMessages([...(messages || []), ...data.results]);
                } else {
                    setMessages(data.results);
                }
            } catch (error) {
                console.log(error);
            }
        };

        if (inView && next) {
            FetchData();
        }
    }, [inView]);

    useEffect(() => {
        socketRef.current = new WebSocket(
            `ws://127.0.0.1:8000/ws/?access_token=${localStorage.getItem(
                "token"
            )}`
        );

        socketRef.current.onopen = () => {
            console.log("WebSocket connection established");
        };

        socketRef.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log(data);
            setMessages((messages) => [...(messages || []), data]);
        };

        socketRef.current.onclose = () => {
            console.log("WebSocket connection closed");
        };

        socketRef.current.onerror = (error) => {
            console.log(error);
        };

        return () => {
            if (socketRef.current) {
                socketRef.current.close();
            }
        };
    });

    return (
        <Container fluid>
            <Row
                className="d-flex  flex-column overflow-auto flex-nowrap"
                style={{ maxHeight: "calc(100vh - 170px)" }}
                ref={list}
            >
                {messages &&
                    messages.map((message, index) => (
                        <>
                            {index === 0 ? (
                                <Container fluid className="p-0 m-0" ref={ref}>
                                    <Message
                                        key={message.id}
                                        message={message.message}
                                        is_author={message.is_author}
                                        date={message.time}
                                    />
                                </Container>
                            ) : (
                                <Message
                                    key={message.id}
                                    message={message.message}
                                    is_author={message.is_author}
                                    date={message.time}
                                />
                            )}
                        </>
                    ))}
            </Row>
            <Row className="position-absolute bottom-0 left-0 p-4 w-50">
                <FormInput socketRef={socketRef} />
            </Row>
        </Container>
    );
});
