import { Card } from "react-bootstrap";

interface IProp {
    message: string;
    is_author: boolean;
    date: string;
}

export const Message = ({ message, is_author, date }: IProp) => {
    const convertDateTime = (isoDateTime: string) => {
        const date = new Date(isoDateTime);
        const options: Intl.DateTimeFormatOptions = {
            day: "numeric",
            month: "long",
            year: "numeric",
            hour: "numeric",
            minute: "numeric",
        };

        return date.toLocaleDateString("ru-RU", options);
    };

    const convertedDateTime = convertDateTime(date);

    return (
        <li className="d-flex justify-content-between mb-4">
            {is_author ? (
                <></>
            ) : (
                <img
                    src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-5.webp"
                    alt="avatar"
                    className="rounded-circle d-flex align-self-start ms-3 shadow-1-strong"
                    width="60"
                ></img>
            )}
            <Card className="w-100">
                <Card.Header className="d-flex justify-content-between p-3">
                    <p className="fw-bold mb-0">USER</p>
                    <p className="text-muted small mb-0">
                        <i className="far fa-clock"></i> {convertedDateTime}
                    </p>
                </Card.Header>
                <Card.Body>
                    <p className="mb-0">{message}</p>
                </Card.Body>
            </Card>

            {is_author ? (
                <img
                    src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-5.webp"
                    alt="avatar"
                    className="rounded-circle d-flex align-self-start ms-3 shadow-1-strong"
                    width="60"
                ></img>
            ) : (
                <></>
            )}
        </li>
    );
};
