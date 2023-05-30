import { Button, Col, Row } from "react-bootstrap";
import { CiSearch } from "react-icons/ci";
import { useState } from "react";
import { CreateBot } from "./components/CreateBot";
import { ListBot } from "./components/ListBot";

export default function ViewBots() {
    const [checked, setChecked] = useState<boolean>(false);

    const handleClick = (e: any) => {
        setChecked(!checked); //api response
    };

    return (
        <>
            <Col>
                <Row>
                    <Col className="text-start">
                        <Button
                            variant="light"
                            className="rounded-circle"
                            size="lg"
                            style={{
                                width: "60px",
                                height: "60px",
                                backgroundColor: "white",
                                boxShadow: "0px 2px 5px rgba(0, 0, 0, 0.3)",
                            }}
                        >
                            <CiSearch />
                        </Button>
                    </Col>
                    <Col className="text-end mt-2">
                        <Button
                            variant={checked ? "secondary" : "primary"}
                            onClick={handleClick}
                        >
                            + Создать бота
                        </Button>
                    </Col>
                </Row>
            </Col>
            <Col className="h-100">{checked ? <CreateBot /> : <ListBot />}</Col>
        </>
    );
}
