import { ResponsiveLine } from "@nivo/line";
import { Col, Container } from "react-bootstrap";
import { ResponsiveBar } from "@nivo/bar";
import { Period } from "./general/Period";

export default function Payments() {
    return (
        <>
            <Container className="d-flex ">
                <Col style={{ height: "500px" }}>
                    <ResponsiveLine
                        data={d1}
                        margin={{ top: 40, bottom: 30, right: 3, left: 21 }}
                        axisLeft={{
                            legend: "Количество консультаций",
                            legendOffset: -40,
                        }}
                        enableArea={true}
                        useMesh={true}
                    ></ResponsiveLine>
                </Col>
                <Col style={{ height: "500px" }}>
                    <ResponsiveBar
                        margin={{ top: 40, bottom: 30, right: 3, left: 40 }}
                        data={data}
                        enableLabel={false}
                        enableGridX={true}
                        enableGridY={false}
                        groupMode="grouped"
                        keys={["Первичная", "Вторичная"]}
                        // layout="horizontal"
                        indexBy="type"
                        // axisLeft={{
                        //     legend: "Тип консультации",
                        //     legendOffset: -40,
                        // }}
                    />
                </Col>
            </Container>
            <Period />
        </>
    );
}

const d1 = [
    {
        id: "Serie 1",
        color: "hsl(146, 70%, 50%)",
        data: [
            {
                x: 1,
                y: 4,
            },
            {
                x: 2,
                y: 2,
            },
            {
                x: 3,
                y: 5,
            },
            {
                x: 4,
                y: 1,
            },
            {
                x: 5,
                y: 8,
            },
        ],
    },
];

const data = [
    {
        type: "12",
        Первичная: 60,
        ПервичнаяColor: "hsl(146, 70%, 50%)",
        Вторичная: 90,
        ВторичнаяColor: "hsl(146, 70%, 50%)",
    },
    {
        type: "13",
        Первичная: 60,
        ПервичнаяColor: "hsl(146, 70%, 50%)",
        Вторичная: 90,
        ВторичнаяColor: "hsl(146, 70%, 50%)",
    },
    {
        type: "14",
        Первичная: 60,
        ПервичнаяColor: "hsl(146, 70%, 50%)",
        Вторичная: 90,
        ВторичнаяColor: "hsl(146, 70%, 50%)",
    },
    {
        type: "15",
        Первичная: 60,
        ПервичнаяColor: "hsl(146, 70%, 50%)",
        Вторичная: 90,
        ВторичнаяColor: "hsl(146, 70%, 50%)",
    },
    {
        type: "16",
        Первичная: 60,
        ПервичнаяColor: "hsl(146, 70%, 50%)",
        Вторичная: 90,
        ВторичнаяColor: "hsl(146, 70%, 50%)",
    },
    {
        type: "17",
        Первичная: 60,
        ПервичнаяColor: "hsl(146, 70%, 50%)",
        Вторичная: 90,
        ВторичнаяColor: "hsl(146, 70%, 50%)",
    },
    {
        type: "18",
        Первичная: 60,
        ПервичнаяColor: "hsl(146, 70%, 50%)",
        Вторичная: 90,
        ВторичнаяColor: "hsl(146, 70%, 50%)",
    },
    // {
    //     type: "Вторичная",
    // },
];
