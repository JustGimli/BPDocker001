import { makeAutoObservable } from "mobx";
import {Project} from "../utils/interface"




class ProjectComponent {
    project: Project | null = null

    
    constructor() {
        makeAutoObservable(this)
    }

    setProject(obj: Project) {
        this.project = obj;
    }

    setIsActive(obj: boolean) {
        if (this.project) {
            this.project.is_active = obj;
        }
    }

    setReportMessage(obj: boolean) {
        if (this.project) {
            this.project.report_message = obj;
        }
   }

   setSendType (obj: string) {
    if (this.project) {
        this.project.send_type = obj;
    }
   }
    setReportMessageType (obj: string) {
        if (this.project) {
            this.project.report_message_type = obj;
        }
    }

    setAdminSendType (obj: string) {
        if (this.project) {
            this.project.admin_send_type = obj;
        }
    }
}


// eslint-disable-next-line import/no-anonymous-default-export
export default new ProjectComponent();