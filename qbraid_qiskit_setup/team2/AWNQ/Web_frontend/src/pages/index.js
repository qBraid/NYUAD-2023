import Head from "next/head";
import { subDays, subHours } from "date-fns";
import { Box, Container, Unstable_Grid2 as Grid } from "@mui/material";
import { Layout as DashboardLayout } from "src/layouts/dashboard/layout";
import { OverviewBudget } from "src/sections/overview/overview-budget";
import { OverviewLatestOrders } from "src/sections/overview/overview-latest-orders";
import { OverviewLatestProducts } from "src/sections/overview/overview-latest-products";
import { OverviewSales } from "src/sections/overview/overview-sales";
import { OverviewTasksProgress } from "src/sections/overview/overview-tasks-progress";
import { OverviewTotalCustomers } from "src/sections/overview/overview-total-customers";
import { OverviewTotalProfit } from "src/sections/overview/overview-total-profit";
import { OverviewTraffic } from "src/sections/overview/overview-traffic";
import Map from "./map/index";
import Image from "next/image";

const now = new Date();

const Page = () => (
  <>
    <Box
      component="main"
      sx={{
        flexGrow: 1,
        py: 8,
      }}
    >
      <Container maxWidth="xl">
        <Grid container spacing={3}>
          <Grid xs={12} md={12} lg={12}>
            {/* <Map /> */}
            <div style={{ width: "100%", display: "flex", justifyContent: "center" }}>
              <Image src="/before.png" width={1000} height={300} quality={100} />
            </div>
         </Grid>

          <Grid xs={12} md={12} lg={12}>
            <OverviewLatestOrders
              orders={[
                {
                  id: "1",
                  address: "25",
                  avatar: "jade",
                  createdAt: subDays(subHours(now, 7), 1).getTime(),
                  email: "van",
                  name: "A1231",
                  phone: "...",
                },
                {
                  id: "2",
                  address: "4",
                  avatar: "sakeeth",
                  createdAt: subDays(subHours(now, 7), 1).getTime(),
                  email: "car",
                  name: "D3341",
                  phone: "...",
                },
                {
                  id: "3",
                  address: "19",
                  avatar: "aziz",
                  createdAt: subDays(subHours(now, 7), 1).getTime(),
                  email: "van",
                  name: "Y2390",
                  phone: "...",
                },
                {
                  id: "4",
                  address: "3",
                  avatar: "priya",
                  createdAt: subDays(subHours(now, 7), 1).getTime(),
                  email: "car",
                  name: "B1235",
                  phone: "...",
                },
              ]}
              sx={{ height: "100%" }}
            />
          </Grid>
        </Grid>
      </Container>
    </Box>
  </>
);

Page.getLayout = (page) => <DashboardLayout>{page}</DashboardLayout>;

export default Page;
