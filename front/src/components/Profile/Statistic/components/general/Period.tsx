import { Nav } from "react-bootstrap";
import { IPeriods } from "../../../../../utils/interface";
import { periods } from "../../../../../utils/consts";
import { useLocation } from "react-router-dom";
import { $api } from "../../../../../utils/api/api";

interface IProp {
    handleData?: any;
}

export const Period = ({ handleData }: IProp) => {
    const location = useLocation();

    const handleClick = (e: any) => {
        e.preventDefault();
        const FetchData = async (path: string, period: string) => {
            try {
                const data = await $api.get(`statistics/${path}/`, {
                    params: { period: period },
                });
                if (path === "general") {
                    const active_users_count = data.data.active_users_count;
                    const new_users_count = data.data.new_users_count;
                    handleData(active_users_count, new_users_count);
                } else if (path === "consultation") {
                    const primary_consultaion = data.data.primary_consultaion;
                    const repeat_consultation = data.data.repeat_consultation;
                    const consultations_per = data.data.consultations_per;

                    handleData(
                        primary_consultaion,
                        repeat_consultation,
                        consultations_per
                    );
                }
            } catch (err) {
                console.log(err);
            }
        };

        const path = location.pathname.split("/")[3];
        const period = e.target.id;

        FetchData(path, period);
    };

    return (
        <Nav variant="tabs" fill>
            {periods.map(({ period, value }: IPeriods) => (
                <Nav.Item key={value}>
                    <Nav.Link id={value} eventKey={value} onClick={handleClick}>
                        {period}
                    </Nav.Link>
                </Nav.Item>
            ))}
        </Nav>
    );
};
