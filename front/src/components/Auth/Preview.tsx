import { RxStarFilled, RxStar } from "react-icons/rx";
import Carousel from "react-bootstrap/Carousel";
import { Col, Container, Row } from "react-bootstrap";

import { useEffect, useState } from "react";
import { $auth } from "../../utils/api/api";

interface IData {
    id: number;
    desc: string;
    img: string;
    name: string;
    surname: string;
    stars: string;
    label: string;
}

export default function Preview() {
    const [data, setData] = useState<Array<IData> | null>(null);

    useEffect(() => {
        $auth.get("rating/").then((resp: any) => {
            if (resp.data) {
                if (resp.data.length > 0) {
                    setData(resp.data);
                }
            }
        });
    }, []);

    return (
        <>
            {data ? (
                <>
                    <Container className="mh-100" fluid>
                        <Carousel variant="dark" controls={false}>
                            {data.map((data: IData) => {
                                return (
                                    <Carousel.Item
                                        key={data.id}
                                        className="mh-100"
                                        style={{ minHeight: "100%" }}
                                    >
                                        <Row>
                                            <Col className="text-center">
                                                {[...Array(5)].map((x, i) =>
                                                    i <= Number(data.stars) ? (
                                                        <RxStarFilled
                                                            key={i}
                                                            size={30}
                                                            style={{
                                                                color: "#FEC84B",
                                                            }}
                                                        />
                                                    ) : (
                                                        <RxStar
                                                            size={30}
                                                            key={i}
                                                        />
                                                    )
                                                )}
                                            </Col>
                                        </Row>
                                        <Row className="my-5">
                                            <Col
                                                className="text-center fs-sm fs-5 fs-4 "
                                                style={{
                                                    overflowWrap: "break-word",
                                                }}
                                            >
                                                {data.desc}
                                            </Col>
                                        </Row>
                                        <Row className=" my-3">
                                            <Col
                                                className="mx-auto"
                                                sm={4}
                                                md={4}
                                                lg={2}
                                            >
                                                <Container className="d-flex justify-content-center">
                                                    <img
                                                        className="rounded-circle"
                                                        src={
                                                            process.env
                                                                .REACT_APP_BASE_URL +
                                                            data.img
                                                        }
                                                        style={{
                                                            height: "120px",
                                                            width: "120px",
                                                        }}
                                                        alt="img"
                                                    ></img>
                                                </Container>
                                            </Col>
                                        </Row>
                                        <Container className="my-4">
                                            <Row className="">
                                                <Col className="text-center fs-5">
                                                    {data.name} {data.surname}
                                                </Col>
                                            </Row>
                                            <Row className="mb-5 fs-6">
                                                <Col className="text-center">
                                                    {data.label}
                                                </Col>
                                            </Row>
                                        </Container>
                                    </Carousel.Item>
                                );
                            })}
                        </Carousel>
                    </Container>
                    <Row className="my-5 position-absolute bottom-0 w-50 text-center">
                        <Col className="">email@exaple.com</Col>
                    </Row>
                </>
            ) : (
                <></>
            )}
        </>
    );
}
