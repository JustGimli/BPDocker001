import { useRef } from "react";
import Bot from "../../../../../store/CreateBot";
import { Col, Container, Form, FormControl, Row } from "react-bootstrap";

const Setting = () => {
    const handleName = (e: any) => {
        Bot.addName(e.target.value);
    };

    const handleDesc = (e: any) => {
        Bot.addDesc(e.target.value);
    };

    const inputFileRef = useRef<any>();

    const handleUploadClick = () => {
        inputFileRef.current.click();
    };

    const handleFileChange = (e: any) => {
        const file = e.target.files[0];
        if (file) {
            Bot.addImg(file);
        }
    };

    return (
        <Container>
            <Row>
                <Container>
                    <Row className="py-2 fs-5">
                        <Col>Настройка бота</Col>
                    </Row>
                    <Row className="w-50">
                        <Col>
                            <FormControl
                                type="file"
                                className="w-50"
                                // onChange={handlePhoto}
                            />
                        </Col>
                        <Col md={8} className="col-4 form-control-sm">
                            Загрузите изображение для ботпика (аватарка). Файл в
                            формате jpg, png или gif не более 20 МБ.Оптимальный
                            размер изображения 240×240 px.
                        </Col>
                    </Row>
                </Container>
            </Row>
            <Form onSubmit={(e) => e.preventDefault()}>
                <Row></Row>
                <Form.Group
                    controlId="formBasicName"
                    className="col-6 form-control-lg"
                >
                    <Form.Label>Название бота</Form.Label>
                    <Form.Control
                        className="border border-primary"
                        type="email"
                        placeholder="  Введите название бота"
                        onChange={handleName}
                        style={{ height: 56 }}
                    />
                </Form.Group>
                <Form.Group
                    controlId="formBasicDesc"
                    className="col-6 form-control-lg"
                >
                    <Form.Label>Описание</Form.Label>
                    <Form.Control
                        className="border    border-primary"
                        type="email"
                        placeholder="  Введите описание бота"
                        onChange={handleDesc}
                        style={{ height: 56 }}
                    />
                </Form.Group>
                <Form.Group
                    controlId="formDropdown"
                    className="col-2 form-control-lg d-flex w-50"
                >
                    <Form.Select
                        className="border border-primary"
                        style={{ height: 45 }}
                        // onChange={handleLanguageChange}
                    >
                        <option value="option1">Русский</option>
                        <option value="option2">Английский</option>
                    </Form.Select>
                    <Form.Label>
                        {" "}
                        <Row className="mx-2 fs-6">
                            <Col>
                                Язык бота, на котором он будет общаться. Можно
                                будет изменить в настройках.
                            </Col>
                        </Row>
                    </Form.Label>
                </Form.Group>
                <Container></Container>
            </Form>
        </Container>
    );
};

export default Setting;
