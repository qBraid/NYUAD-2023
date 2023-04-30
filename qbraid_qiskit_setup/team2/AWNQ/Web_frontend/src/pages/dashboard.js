import Head from 'next/head';
import ArrowUpOnSquareIcon from '@heroicons/react/24/solid/ArrowUpOnSquareIcon';
import ArrowDownOnSquareIcon from '@heroicons/react/24/solid/ArrowDownOnSquareIcon';
import PlusIcon from '@heroicons/react/24/solid/PlusIcon';
import { OverviewLatestOrders2 } from "src/sections/overview/overview-latest-orders2";
import { OverviewLatestOrders } from "src/sections/overview/overview-latest-orders";
import { subDays, subHours } from "date-fns";
import { useState, useEffect } from "react";

import {
  Box,
  Button,
  Container,
  Pagination,
  Stack,
  SvgIcon,
  Typography,
  Unstable_Grid2 as Grid
} from '@mui/material';
import { Layout as DashboardLayout } from 'src/layouts/dashboard/layout';
import { CompanyCard } from 'src/sections/companies/company-card';
import { CompaniesSearch } from 'src/sections/companies/companies-search';
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
        <Stack spacing={3}>
          <Stack direction="row" justifyContent="space-between" spacing={4}>
            <Stack spacing={1}>
              <Typography variant="h4">Dashboard</Typography>
            </Stack>
          </Stack>
        </Stack>
        <Grid container spacing={3}>
          <Grid xs={12} md={12} lg={12}>
            {/*<Map />*/}
            <div style={{ width: "100%", display: "flex", justifyContent: "center", marginTop:"40px" }}>
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

Page.getLayout = (page) => (
  <DashboardLayout>
    {page}
  </DashboardLayout>
);

export default Page;
