import { AuthPage } from "../pages/Auth/Auth";
import CheckMailPage from "../pages/Auth/CheckMailPage";
import Recover from "../pages/Auth/Recover";
import { PROFILE, CHECKMAIL,  PUBLIC_ROOT, RECOVER, SCRIPT, BOT, MAIL, SETTINGS, STATS, GENERAL, CONSULTATION, PAYMENTS, USERS } from "./consts";
import { Profile } from "../pages/Profile/Profile";
import ViewBots from "../components/Profile/ViewBots";
import { ViewScript } from "../components/Profile/Script/ViewScript";
// import Test from "../components/TEST";
import ViewMail from "../components/Profile/Mail/ViewMail";
import { Chats } from "../components/Profile/Chats/Chats";
import { CHATS } from "./consts";
import { Settings } from "../components/Profile/Settings/Settings";
import Stats from "../components/Profile/Statistic/Stats";
import General from "../components/Profile/Statistic/components/General";
import Consultation from "../components/Profile/Statistic/components/Cons";
import Payments from "../components/Profile/Statistic/components/Payments";
import Users from "../components/Profile/Statistic/components/Users";

export const StatisticRoutes = [
    {
        Component: General,
        path: GENERAL
    },
    {
        Component: Consultation,
        path: CONSULTATION
    },
    {
        Component: Payments,
        path: PAYMENTS
    },
    {
        Component: Users,
        path: USERS
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
    },
    {
        Component: Chats,
        path: CHATS
    }, 
    {
        Component: Settings,
        path: SETTINGS
    },
    {
        Component: Stats,
        path: STATS
    }
    
]

export const All = [
   {
        Component: Profile,
        path: PROFILE
   },
    // {
    //     Component: Test,
    //     path: '/test'
    // },
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