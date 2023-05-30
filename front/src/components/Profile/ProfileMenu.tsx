import { useMediaQuery } from "react-responsive";
import { HeaderMenu } from "./ProfileM/Menu";

export default function ProfileMenu() {
    const isDesktop = useMediaQuery({ minWidth: 1090 });
    const isTablet = useMediaQuery({ minWidth: 768, maxWidth: 1090 });

    return <>{(isDesktop || isTablet) && <HeaderMenu />}</>;
}
