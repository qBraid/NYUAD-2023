import Head from "next/head";
import { subDays, subHours } from "date-fns";
import { useState, useEffect } from "react";
import { Box, Container, Unstable_Grid2 as Grid } from "@mui/material";
import { Layout as DashboardLayout } from "src/layouts/dashboard/layout";
import { OverviewBudget } from "src/sections/overview/overview-budget";
import { OverviewLatestOrders2 } from "src/sections/overview/overview-latest-orders2";
import { OverviewLatestProducts } from "src/sections/overview/overview-latest-products";
import { OverviewSales } from "src/sections/overview/overview-sales";
import { OverviewTasksProgress } from "src/sections/overview/overview-tasks-progress";
import { OverviewTotalCustomers } from "src/sections/overview/overview-total-customers";
import { OverviewTotalProfit } from "src/sections/overview/overview-total-profit";
import { OverviewTraffic } from "src/sections/overview/overview-traffic";
import Map from "./map/index";
import Image from "next/image";
import Loading from "src/components/loading";

const now = new Date();

const delayFetch = (delay) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve('Data fetched successfully!');
    }, delay);
  });
};

const Page = () => {
  const [data, setData] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      const response = await delayFetch(5000);
      setData(true);
    };

    loadData();
  }, []);

  return data ? (
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
              {/*<Map />*/}
              <div style={{ width: "100%", display: "flex", justifyContent: "center" }}>
                <Image
                  style={{ objectPosition: "cover" }}
                  src="/after.png"
                  width={1000}
                  height={300}
                  quality={100}
                />
              </div>
            </Grid>
            <Grid xs={12} md={12} lg={12}>
              <OverviewLatestOrders2
                orders={[
                  {
                    id: "1",
                    address: "2",
                    avatar: "jade",
                    createdAt: subDays(subHours(now, 7), 1).getTime(),
                    email: "van",
                    name: "A1231",
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
                  {
                    id: "1",
                    address: "3",
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
                    id: "1",
                    address: "4",
                    avatar: "jade",
                    createdAt: subDays(subHours(now, 7), 1).getTime(),
                    email: "van",
                    name: "A1231",
                    phone: "...",
                  },
                  {
                    id: "3",
                    address: "5",
                    avatar: "aziz",
                    createdAt: subDays(subHours(now, 7), 1).getTime(),
                    email: "van",
                    name: "Y2390",
                    phone: "...",
                  },
                  {
                    id: "1",
                    address: "8",
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
                    address: "5",
                    avatar: "aziz",
                    createdAt: subDays(subHours(now, 7), 1).getTime(),
                    email: "van",
                    name: "Y2390",
                    phone: "...",
                  },
                  {
                    id: "3",
                    address: "2",
                    avatar: "aziz",
                    createdAt: subDays(subHours(now, 7), 1).getTime(),
                    email: "van",
                    name: "Y2390",
                    phone: "...",
                  },
                  {
                    id: "3",
                    address: "2",
                    avatar: "aziz",
                    createdAt: subDays(subHours(now, 7), 1).getTime(),
                    email: "van",
                    name: "Y2390",
                    phone: "...",
                  },
                  {
                    id: "3",
                    address: "4",
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
  ) : (
    <>
      <Loading></Loading>
    </>
  );
}

Page.getLayout = (page) => <DashboardLayout>{page}</DashboardLayout>;

export default Page;
