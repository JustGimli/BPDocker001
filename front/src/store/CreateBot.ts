import {  makeAutoObservable } from "mobx";


interface CreateBot {
    [key: string]: any;
        id?: number;
        name: string;
        desc?: string;
        img?: Blob;
        token: string;
        start_mes?: string;
        lang?: string,
    }


class Bot {

    instance_bot: CreateBot = {
        name: '',
        desc: '',
        lang: '',
        token: '',
        start_mes: '',
    } 
    
    form = new FormData();

    constructor() {
        makeAutoObservable(this)
    }

    addName(name: string) {
        this.instance_bot.name = name;
    }

    addToken(token: string) {
        this.instance_bot.token = token;
    }
    
    addStartMes(message: string) {
        this.instance_bot.start_mes = message;
    }

    addDesc(desc: string) {
        this.instance_bot.desc = desc
    }

    addLang(lang: string) {
        this.instance_bot.lang = lang
    }

    addImg(img: File) {
        this.form.append('img', img)
    }

    send() {
        for (const prop in this.instance_bot) {
            this.form.append(`${prop}`, this.instance_bot[prop])
        }
    }
} 


// eslint-disable-next-line import/no-anonymous-default-export
export default new Bot();