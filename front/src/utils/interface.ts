



export default interface IBot {
        id?: number;
        name: string;
        desc?: string;
        img?: Blob;
        token: string;
        start_mes?: string;
        lang?: string,
        date_update: string
}