import { Col, Container } from "react-bootstrap";
import { ResponsiveLine } from "@nivo/line";
import { ResponsivePie } from "@nivo/pie";
import { Period } from "./general/Period";
import { PieData } from "../../../../utils/interface";
import { useState } from "react";

interface XY {
    x: string;
    y: string;
}

interface LineData {
    id: string;
    label?: string;
    data: Array<XY>;
}

export default function Consultation() {
    const [dataPie, setDataPie] = useState<Array<PieData>>([
        {
            id: "",
            label: "",
            value: 0,
            color: "",
        },
    ]);

    const [lineData, setLineData] = useState<Array<LineData>>([]);

    const handleData = (
        primary_consultaion: string,
        repeat_consultation: string,
        consultations_per: any,
        type: string
    ) => {
        const dataPie = [
            {
                id: "Первичная консультация",
                value: Number(primary_consultaion),
            },
            {
                id: "Повторная консультация",

                value: Number(repeat_consultation),
            },
        ];

        const ldata = [
            {
                id: "количество консультаций",
                data: consultations_per.map((obj: any) => {
                    return {
                        x: obj.period,
                        y: obj.count,
                        // color: obj.color,
                    };
                }),
            },
        ];

        setDataPie(dataPie);
        setLineData(ldata);
    };

    return (
        <>
            <Container className="d-flex p-0 m-0">
                <Col style={{ height: "500px" }} md={4}>
                    <ResponsivePie
                        margin={{ right: 70, left: 70 }}
                        data={dataPie}
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
                        data={lineData}
                        margin={{ top: 80, bottom: 80, right: 120, left: 120 }}
                        // axisLeft={{
                        //     legend: "Количество консультаций",
                        //     legendOffset: -40,
                        // }}
                        enableArea={true}
                        useMesh={true}
                    ></ResponsiveLine>
                </Col>
            </Container>
            <Period handleData={handleData} />
        </>
    );
}
