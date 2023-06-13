import { Col, Container } from "react-bootstrap";
import { ResponsiveLine } from "@nivo/line";
import { ResponsivePie } from "@nivo/pie";
import { Period } from "./general/Period";

export default function Users() {
    return (
        <>
            <Container className="d-flex p-0 m-0">
                <Col style={{ height: "500px" }} md={4}>
                    <ResponsivePie
                        margin={{ right: 70, left: 70 }}
                        data={data}
                        isInteractive={true}
                        activeOuterRadiusOffset={8}
                        cornerRadius={3}
                        innerRadius={0.5}
                        enableArcLabels={false}
                        arcLinkLabel={(d) => `${d.id} (${d.formattedValue})`}
                        padAngle={1}
                        enableArcLinkLabels={false}
                        layers={[
                            "arcs",
                            "arcLabels",
                            "arcLinkLabels",
                            "legends",
                        ]}
                    />
                </Col>
                <Col>
                    <ResponsiveLine
                        data={d1}
                        margin={{ top: 80, bottom: 80, right: 120, left: 120 }}
                        axisLeft={{
                            legend: "Количество консультаций",
                            legendOffset: -40,
                        }}
                        enableArea={true}
                        useMesh={true}
                    ></ResponsiveLine>
                </Col>
            </Container>
            <Period />
        </>
    );
}
const data = [
    {
        id: "консультация",
        label: "elixir",
        value: 575,
        color: "red",
    },
    {
        id: "не использовали",
        label: "",
        value: 300,
        color: "blue",
    },
];

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
