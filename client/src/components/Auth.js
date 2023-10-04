import React, { useState } from "react";
import { Button, TextField, Paper, Typography, Tabs, Tab } from "@mui/material";
import { useFormik } from "formik";
import * as Yup from "yup";
import { useNavigate } from "react-router-dom";

const Auth = () => {
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const [message, setMessage] = useState("");

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
    formik.setSubmitting(false);
  };

  const validationSchema = Yup.object({
    email: Yup.string().email("Invalid email format").required("Required"),
    password: Yup.string()
      .min(6, "Minimum 6 characters required")
      .required("Required"),
    firstName: Yup.string().required("Required"),
    lastName: Yup.string().required("Required"),
  });

  const handleRegister = async () => {
    try {
        const response = await fetch("http://localhost:8000/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: formik.values.email,
                password: formik.values.password,
                firstName: formik.values.firstName,
                lastName: formik.values.lastName,
            }),
        });

        const data = await response.json();
        if (data.email) {
            setMessage("Registered successfully! Please log in.");
            setTabValue(0);
        } else {
            setMessage("Registration failed. Please try again.");
        }
    } catch (error) {
        setMessage("An error occurred. Please try again.");
    }
};


  const handleLogin = async () => {
    try {
      const response = await fetch("http://localhost:8000/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `username=${formik.values.email}&password=${formik.values.password}&grant_type=password&scope=read`,
      });

      const data = await response.json();
      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        setMessage("Logged in successfully!");
        navigate("/user_details");
      } else {
        setMessage("Login failed. Please check your credentials.");
      }
    } catch (error) {
      setMessage("An error occurred. Please try again.");
    }
  };

  const formik = useFormik({
    initialValues: {
      email: "",
      password: "",
      firstName: "",
      lastName: "",
    },
    validationSchema: validationSchema,
    onSubmit: tabValue === 0 ? handleLogin : handleRegister,
  });

  return (
    <Paper style={{ padding: "2rem", width: "400px" }}>
      <Tabs
        value={tabValue}
        onChange={handleTabChange}
        indicatorColor="primary"
        textColor="primary"
        centered
        sx={{ padding: "2rem" }}
      >
        <Tab label="Login" />
        <Tab label="Register" />
      </Tabs>

      {tabValue === 0 ? (
        <Typography variant="h4">Login</Typography>
      ) : (
        <Typography variant="h4">Register</Typography>
      )}

      <form onSubmit={formik.handleSubmit}>
        {tabValue === 1 && (
          <>
            <TextField
              fullWidth
              margin="normal"
              name="firstName"
              label="First Name"
              variant="outlined"
              value={formik.values.firstName}
              onChange={formik.handleChange}
              error={
                formik.touched.firstName && Boolean(formik.errors.firstName)
              }
              helperText={formik.touched.firstName && formik.errors.firstName}
            />
            <TextField
              fullWidth
              margin="normal"
              name="lastName"
              label="Last Name"
              variant="outlined"
              value={formik.values.lastName}
              onChange={formik.handleChange}
              error={formik.touched.lastName && Boolean(formik.errors.lastName)}
              helperText={formik.touched.lastName && formik.errors.lastName}
            />
          </>
        )}
        <TextField
          fullWidth
          margin="normal"
          name="email"
          label="Email"
          variant="outlined"
          value={formik.values.email}
          onChange={formik.handleChange}
          error={formik.touched.email && Boolean(formik.errors.email)}
          helperText={formik.touched.email && formik.errors.email}
        />
        <TextField
          fullWidth
          margin="normal"
          name="password"
          label="Password"
          type="password"
          variant="outlined"
          value={formik.values.password}
          onChange={formik.handleChange}
          error={formik.touched.password && Boolean(formik.errors.password)}
          helperText={formik.touched.password && formik.errors.password}
        />
        <Button color="primary" variant="contained" fullWidth type="submit">
          {tabValue === 0 ? "Login" : "Register"}
        </Button>
      </form>

      {message && <p>{message}</p>}
    </Paper>
  );
};

export default Auth;
