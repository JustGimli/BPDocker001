import { Container } from "react-bootstrap";
import { MessageList } from "./Message/MessageList";
import Chats from "../../../../store/Chats";
import { observer } from "mobx-react-lite";
import { Route, Routes } from "react-router-dom";
import { IChat } from "../../../../utils/interface";

export const Messages = observer(() => {
    return (
        <Container fluid className="h-100">
            <Routes>
                {Chats.chats.map((item: IChat | null, index) => (
                    <Route
                        key={item?.id}
                        path={item?.chat_id.toString()}
                        element={<MessageList />}
                    />
                ))}
            </Routes>
        </Container>
    );
});
