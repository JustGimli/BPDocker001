import { useEffect, useState } from "react";
import { Badge, Col, Container, Nav, NavDropdown, Row } from "react-bootstrap";
import { AiOutlineExclamationCircle } from "react-icons/ai";
import { GrDocumentText } from "react-icons/gr";
import { useMediaQuery } from "react-responsive";
import { $api } from "../../../utils/api/api";
import { Project } from "../../../utils/interface";
import ProjectComponent from "../../../store/Project";
import { observer } from "mobx-react-lite";
import { ProjectsNavs } from "./components/projectsNavs";

export const MainBar = observer(() => {
    const [isCreatingProject, setIsCreatingProject] = useState<boolean>(false);
    const [projects, setProjects] = useState<Array<Project> | null>();
    const isDesktop = useMediaQuery({ minWidth: 1090 });
    const isTablet = useMediaQuery({ minWidth: 768, maxWidth: 1090 });

    const handleCreateProject = () => {
        setIsCreatingProject(true);
    };

    useEffect(() => {
        const FetchData = async () => {
            try {
                const data = await $api.get("projects/");

                if (data.data) {
                    if (!ProjectComponent.project) {
                        ProjectComponent.setProject(data.data[0]);
                        setProjects(data.data);
                    }
                }
            } catch (err) {
                console.log(err);
            }
        };

        FetchData();
    }, []);

    return (
        <>
            {(isDesktop || isTablet) && (
                <Container fluid>
                    <Row>
                        <Col>
                            <Nav>
                                <Row className="d-block">
                                    <Col>
                                        <Nav.Item
                                            className="px-2"
                                            style={{ fontSize: "14px" }}
                                        >
                                            проект
                                        </Nav.Item>
                                    </Col>
                                    <Col>
                                        {projects && (
                                            <NavDropdown
                                                title={
                                                    ProjectComponent.project
                                                        ?.name || "Новый проект"
                                                }
                                                id="collasible-nav-dropdown"
                                            >
                                                {isCreatingProject ? (
                                                    <></>
                                                ) : (
                                                    <ProjectsNavs
                                                        handler={
                                                            handleCreateProject
                                                        }
                                                        currentName={
                                                            ProjectComponent
                                                                .project?.name
                                                        }
                                                        projects={projects}
                                                    />
                                                )}
                                            </NavDropdown>
                                        )}
                                    </Col>
                                </Row>
                            </Nav>
                        </Col>
                        <Col>
                            <Container
                                fluid
                                className="d-flex align-items-center "
                            >
                                <Row className="m-1">
                                    <Col>
                                        <Badge
                                            pill
                                            bg="warning"
                                            className="fs-6  text-light d-flex align-items-center"
                                        >
                                            <AiOutlineExclamationCircle
                                                size={36}
                                            />
                                            {isDesktop && (
                                                <Row>
                                                    <Col>
                                                        ИЗМЕНЕНИЯ НЕ
                                                        ОПУБЛИКОВАНЫ
                                                    </Col>
                                                </Row>
                                            )}
                                        </Badge>
                                    </Col>
                                </Row>
                                <Nav>
                                    <Row className="d-block mx-2 text-center">
                                        <Col>
                                            <GrDocumentText size={25} />
                                        </Col>
                                        <Col>
                                            <Nav.Link href="">
                                                Документация
                                            </Nav.Link>
                                        </Col>
                                    </Row>
                                </Nav>
                                <Row className="d-block ">
                                    <Col>
                                        <img
                                            alt="russianFlag"
                                            src={require("./static/russianFlag.png")}
                                        />
                                    </Col>
                                    Русский
                                </Row>
                            </Container>
                        </Col>
                    </Row>
                </Container>
            )}
        </>
    );
});
