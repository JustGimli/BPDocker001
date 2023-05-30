/* eslint-disable import/no-anonymous-default-export */
import { makeAutoObservable } from "mobx"
import { makePersistable } from "mobx-persist-store";


class Menu {
    comp = 'bot' 

    constructor() {
        makeAutoObservable(this)

        makePersistable(this, {name: 'path', properties: ['comp'], storage: window.localStorage})
    }

    SetItem(str: any) {
        this.comp = str;
    }
}


export default new Menu();