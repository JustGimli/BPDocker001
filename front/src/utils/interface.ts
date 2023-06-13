export  interface Project {
    id: number;
    name: string;
    created: string;
    is_active: boolean;
    send_type: string;
    report_message: boolean;
    report_message_type: string;
    admin_send: boolean;
    admin_send_type: string;
    timezone: string;
}


export  interface IBot {
        id?: number;
        name: string;
        desc?: string;
        img?: Blob;
        token: string;
        start_mes?: string;
        lang?: string,
        date_update: string
}

export interface IChat {
    id: number,
    is_active: boolean,
    chat_id: number,
    sender_id: number,
    created_at: string
}


export interface IMessage {
    id: number,
    is_author: boolean,
    time: string;
    message: string;
    is_read: boolean;
    // sender?: boolean;
}

export interface IPeriods {
    period: string;
    value: string
}

export interface PieData {
    id: string;
    label?: string;
    value: number;
    color?: string;
}