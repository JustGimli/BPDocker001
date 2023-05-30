import { useEffect, useState } from "react";
import IBot from "../../../../utils/interface";
import { $api } from "../../../../utils/api/api";
import { ItemBot } from "./ListBot/ItemBot";
import { Container } from "react-bootstrap";
import { NItem } from "../../../generalComp/NItem";

export const ListBot = () => {
    const [listBot, setListBot] = useState<Array<IBot> | null>(null);

    useEffect(() => {
        (async () => {
            try {
                const data = await $api("bots");
                const responseData: Array<IBot> = data.data;
                setListBot(responseData);
            } catch (error) {}
        })();
    }, []);

    const Item = (
        <Container
            className="d-flex ustify-content-between flex-row flex-wrap "
            fluid
        >
            {listBot?.map((item, ind) => (
                <ItemBot
                    name={item.name}
                    desc={item.desc}
                    date_update={item.date_update}
                />
            ))}
        </Container>
    );

    return listBot ? <>{Item}</> : <NItem text="Список ваших ботов пуст" />;
};
