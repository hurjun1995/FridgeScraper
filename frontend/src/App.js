import React from "react";
import { Box, Typography, Container } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

import SearchBar from "./components/SearchBar/SearchBar";

const useStyles = makeStyles(() => ({
  app: {
    height: "100vh",
    backgroundColor: "#ecf1f3",
  },
}));

function App() {
  const classes = useStyles();
  return (
    <Box className={classes.app}>
      <Container>
        <Typography variant="h2" gutterBottom>
          Fridge Scraper
        </Typography>
        <SearchBar />
      </Container>
    </Box>
  );
}

export default App;
