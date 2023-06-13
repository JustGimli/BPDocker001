import { Col, Container, Form, InputGroup, Row } from "react-bootstrap";
import { SmileBot } from "./../../MyBots/components/img/smiileBot";
import { useEffect } from "react";
import { AiOutlineSearch } from "react-icons/ai";
import { ChatItem } from "./ChatItem";
import { $api } from "../../../../utils/api/api";
import { IChat } from "../../../../utils/interface";
import { observer } from "mobx-react-lite";
import Chats from "../../../../store/Chats";

export const ChatListComponent = observer(() => {
    useEffect(() => {
        const FetchData = async () => {
            try {
                const response = await $api.get("chats/list/");
                const data = response.data;
                if (data) {
                    Chats.addChat(data);
                }
            } catch (error) {
                console.log(error);
            }
        };

        FetchData();
    }, []);

    return (
        <Container className="m-0 p-0">
            <Row className="border m-0 p-0">
                <Form className="mt-4">
                    <Form.Group>
                        <Container className="input-group rounded mb-3">
                            <Form.Control
                                type="search"
                                className="rounded"
                                placeholder="Search"
                            />
                            <InputGroup.Text
                                onClick={(e: any) => console.log(e)}
                                className="border-0"
                                id="search-addon"
                            >
                                <AiOutlineSearch size={20} />
                            </InputGroup.Text>
                        </Container>
                    </Form.Group>
                </Form>
                <Container className="d-flex">
                    <Col>Все обращения</Col>
                    <Col>Ждут ответа</Col>
                </Container>
            </Row>

            {Chats.getChats() ? (
                <Container className="d-flex flex-row justify-content-start">
                    <Container className="d-flex flex-row " fluid>
                        <Row>
                            {Chats.chats.map((item: IChat | null, index) => (
                                <ChatItem
                                    key={index}
                                    name={item!.chat_id}
                                    id={item!.chat_id}
                                    index={index}
                                />
                            ))}
                        </Row>
                    </Container>
                </Container>
            ) : (
                <Container
                    className="text-center border d-flex justify-content-center align-items-center p-0 m-0"
                    style={{ height: "79vh" }}
                >
                    <Row>
                        <SmileBot />
                        <p>У вас еще нет ни одного диалога</p>
                    </Row>
                </Container>
            )}
        </Container>
    );
});
