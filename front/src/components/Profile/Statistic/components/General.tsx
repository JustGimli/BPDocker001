import { Container } from "react-bootstrap";
import { ResponsivePie } from "@nivo/pie";
import { Period } from "./general/Period";
import { useState } from "react";
import { PieData } from "../../../../utils/interface";

export default function General() {
    const [data, setData] = useState<Array<PieData>>([
        {
            id: "",
            label: "",
            value: 0,
            color: "",
        },
    ]);

    const handleSetData = (
        active_users_count: string,
        new_users_count: string
    ) => {
        const data = [
            {
                id: "Новые пользователи",
                label: "",
                value: Number(new_users_count),
                color: "",
            },
            {
                id: "Активные пользователи",
                label: "",
                value: Number(active_users_count),
                color: "",
            },
        ];

        setData(data);
    };

    const CenteredMetric = ({ centerX, centerY }: any) => {
        const total = data.reduce((sum, { value }) => sum + value, 0);

        return (
            <g>
                <text
                    x={centerX}
                    y={centerY + 10}
                    textAnchor="middle"
                    dominantBaseline="central"
                    style={{ fontSize: "14px" }}
                >
                    Всего:
                </text>
                <text
                    x={centerX}
                    y={centerY - 10}
                    textAnchor="middle"
                    dominantBaseline="central"
                    style={{ fontSize: "24px", fontWeight: "bold" }}
                >
                    {total}
                </text>
            </g>
        );
    };

    return (
        <>
            <Container fluid className="p-0 m-0" style={{ height: "500px" }}>
                <ResponsivePie
                    margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
                    data={data}
                    isInteractive={true}
                    activeOuterRadiusOffset={8}
                    cornerRadius={3}
                    innerRadius={0.5}
                    enableArcLabels={false}
                    arcLinkLabel={(d) => `${d.id} (${d.formattedValue})`}
                    padAngle={1}
                    layers={[
                        "arcs",
                        "arcLabels",
                        "arcLinkLabels",
                        "legends",
                        CenteredMetric,
                    ]}
                />
            </Container>
            <Period handleData={handleSetData} />
        </>
    );
}
