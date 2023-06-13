import {  makeAutoObservable } from "mobx";



interface CreateBot {
    [key: string]: any;
        id?: number;
        name: string;
        desc?: string;
        img?: Blob;
        token: string;
        lang?: string,
        start_message?: string;
    }


class Bot {

    instance_bot: CreateBot = {
        name: '',
        desc: '',
        lang: '',
        token: '',
        start_message: '',
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
        this.instance_bot.start_message = message;
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
        for (const name in this.instance_bot) {
            this.form.append(name, this.instance_bot[name])
        }
    }
} 


// eslint-disable-next-line import/no-anonymous-default-export
export default new Bot();