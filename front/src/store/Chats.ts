import { makeAutoObservable } from "mobx";
import { IChat } from "../utils/interface";

class Chats {
    current: number | null = null;
    chats: Array<IChat | null> = [];

    constructor() {
        makeAutoObservable(this);
    }

    setCurrent(num: number) {
        if (num < this.chats.length) {
            this.current = num;
        }
    }

    getCurrent() {
        if (this.current !== null) {
            return this.chats[this.current];
        }
        return null;
    }

    addChat(chat: Array<IChat>) {
        this.chats = [];
        this.chats.push(...chat);
    }

    getChats() {
        if (this.chats.length === 0) {
            return null;
        }
        return this.chats;
    }
}

// eslint-disable-next-line import/no-anonymous-default-export
export default new Chats();
