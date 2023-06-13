import { useEffect, useState } from "react";
import { $api } from "../../../../utils/api/api";
import { Container } from "react-bootstrap";
import { ItemScript } from "./ListScript/Item";
import { NItem } from "../../../generalComp/NItem";

interface IStat {
    id: number;
    name: string;
    date_update: string;
    primary: boolean;
    secondary: boolean;
    text: Array<string>;
    is_active: boolean;
}

export const ListScript = () => {
    const [listStat, setListStat] = useState<Array<IStat> | undefined>();

    useEffect(() => {
        (async () => {
            try {
                const data = await $api("/bots/status/");
                const responseData: Array<IStat> = data.data;

                for (let i = 0; i < responseData.length; i++) {
                    responseData[i].text = [];
                    if (responseData[i].primary) {
                        responseData[i].text[responseData[i].text.length] =
                            "Первичная консультация";
                    }

                    if (responseData[i].secondary) {
                        responseData[i].text[responseData[i].text.length] =
                            "Повторная консультация";
                    }
                }

                setListStat(responseData);
            } catch (error) {
                console.log(error);
            }
        })();
    }, []);

    const Item = (
        <Container
            className="d-flex justify-content-between flex-row flex-wrap "
            fluid
        >
            {listStat?.map((item, ind) => (
                <ItemScript
                    key={item.id}
                    name={item.name}
                    scripts={item.text}
                    date_update={item.date_update}
                    is_active={item.is_active}
                />
            ))}
        </Container>
    );

    return <>{listStat ? Item : <NItem text="Список сценариев пуст" />}</>;
};
