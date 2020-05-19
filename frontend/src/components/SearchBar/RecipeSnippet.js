import React from "react";
import { Grid, Typography, Paper } from "@material-ui/core"
import { makeStyles } from '@material-ui/core/styles'

const useStyles = makeStyles((theme) => ({
  text: {
    width: '50%',
  },
  paper: {
    padding: theme.spacing(2)
  }
}))

export default function RecipeSnippet(props) {
  const title = props.snippet.title;
  const description = props.snippet.description;
  const thumbnails = props.snippet.thumbnails.medium;
  const classes = useStyles()

  return (
    <Grid item container spacing={2}>
      <Paper className={classes.paper}>
        <Grid item container direction="row" spacing={2}>
          <Grid item>
            <img src={thumbnails.url} width={thumbnails.width * 0.8} height={thumbnails.height * 0.8}/>
          </Grid>
          <Grid item xs={8}>
            <Typography variant="subtitle1" gutterBottom>
              {title}
            </Typography>
            <Typography variant="body2" gutterBottom>
              {description}
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    </Grid>
  );
}
