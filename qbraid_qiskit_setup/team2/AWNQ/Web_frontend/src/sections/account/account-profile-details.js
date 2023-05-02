import { useCallback, useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  Divider,
  TextField,
  Unstable_Grid2 as Grid
} from '@mui/material';

const states = [
  {
    value: 'car',
    label: 'Car'
  },
  {
    value: 'van',
    label: 'Van'
  },
];

export const AccountProfileDetails = () => {
  const [values, setValues] = useState({
    firstName: '',
    lastName: 'Visser',
    email: 'demo@devias.io',
    phone: '',
    state: 'los-angeles',
    country: 'USA'
  });

  const handleChange = useCallback(
    (event) => {
      setValues((prevState) => ({
        ...prevState,
        [event.target.name]: event.target.value
      }));
    },
    []
  );

  const handleSubmit = useCallback(
    (event) => {
      event.preventDefault();
    },
    []
  );

  return (
    <form style={{ width: "100%" }} autoComplete="off" noValidate onSubmit={handleSubmit}>
      <Card sx={{ width: "100%" }}>
        <CardHeader subheader="" title="" />
        <CardContent sx={{ pt: 0 }}>
          <Box sx={{ m: -1.5 }}>
            <Grid container spacing={1}>
              <Grid xs={12} md={7}>
                <TextField
                  fullWidth
                  label="Plate #"
                  name="Platenumber"
                  onChange={handleChange}
                  required
                  value={values.firstName}
                />
              </Grid>
              <Grid xs={12} md={6}></Grid>
              <Grid xs={12} md={7}>
                <TextField
                  fullWidth
                  label="Vehicle type"
                  name="type"
                  onChange={handleChange}
                  required
                  select
                  SelectProps={{ native: true }}
                  value={values.state}
                >
                  {states.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </TextField>
              </Grid>
              <Grid xs={12} md={6}></Grid>
              <Grid xs={12} md={7}>
                <TextField
                  fullWidth
                  label="Phone Number"
                  name="phone"
                  onChange={handleChange}
                  type="number"
                  value={values.phone}
                />
              </Grid>
            </Grid>
          </Box>
        </CardContent>
        <Divider />
        <CardActions sx={{ justifyContent: "flex-end" }}>
          <Button href="/" variant="contained">Save</Button>
        </CardActions>
      </Card>
    </form>
  );
};
