
import { AuthPage } from "../pages/Auth/Auth";
import CheckMailPage from "../pages/Auth/CheckMailPage";
import Recover from "../pages/Auth/Recover";

import { PROFILE, CHECKMAIL,  PUBLIC_ROOT, RECOVER, SCRIPT, BOT, MAIL } from "./consts";
import { Profile } from "../pages/Profile/Profile";
import ViewBots from "../components/Profile/MyBots/ViewBots";
import { ViewScript } from "../components/Profile/Script/ViewScript";
import Test from "../components/TEST";
import ViewMail from "../components/Profile/Mail/ViewMail";

export const publicRoutes = [
    {
        Component: AuthPage,
        path: PUBLIC_ROOT
    },
    {
        Component: Recover,
        path: RECOVER
    },
    {
        Component: CheckMailPage,
        path: CHECKMAIL
    }
]

export const ProfileRoutes = [
     {
        Component: ViewBots,
        path: BOT
    },
    {
        Component: ViewScript,
        path: SCRIPT
    },
    {
        Component: ViewMail,
        path: MAIL
    }
    
]

export const privateRoutes = [
   {
        Component: Profile,
        path: PROFILE
   },
    {
        Component: Test,
        path: '/test'
    }
]