import { useTheme } from '@mui/material/styles';
import Image from "next/image";


export const Logo = () => {
  const theme = useTheme();
  const fillColor = theme.palette.primary.main;

  return (
    <div
      style={{
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Image src="/logo.png" width={100} height={50} quality={100} />
    </div>
  );
};
