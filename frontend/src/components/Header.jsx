import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

// テーマは後で修正
const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
  link: {
    color: 'inherit',
    textDecoration: 'none',
  },
}));

const Header = () => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" className={classes.title}>
            My App
          </Typography>
          <Button color="inherit" href="/">Home</Button>
          <Button color="inherit" href="/login">Login</Button>
          <Button color="inherit" href="/signup">Sign Up</Button>
          {/* メニューに追加したい内容など。後で修正 */}
        </Toolbar>
      </AppBar>
    </div>
  );
};

export default Header;
