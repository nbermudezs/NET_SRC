import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

const CustomTableCell = withStyles(theme => ({
  head: {
    backgroundColor: theme.palette.primary.main,
    borderColor: theme.palette.common.white,
    color: theme.palette.common.white,
    fontSize: 14
  },
  body: {
    fontSize: 12,
  },
}))(TableCell);

const FirstColTableCell = withStyles(theme => ({
  body: {
    backgroundColor: theme.palette.primary.main,
    border: 1,
    borderColor: theme.palette.primary.main,
    color: theme.palette.common.white,
    fontSize: 14,
  },
}))(TableCell);

export default class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoaded: false,
      items: null,
      teams: null
    }
  }

  componentWillMount() {
     fetch("/correlation.json")
      .then(res => res.json())
      .then(res => {
        this.setState({
          isLoaded: true,
          items: res
        })
      });

    fetch("/ranking.json")
      .then(res => res.json())
      .then(res => {
        this.setState({
          teams: res
        })
      });
  }

  render() {
    const items = this.state.items;
    const teams = this.state.teams || {};
    const teamNames = Object.keys(teams);
    if (!items) {
      return null;
    }
    return (
      <div>
      <AppBar position="sticky">
        <Toolbar>
          <Typography variant="h6" color="inherit">
            Spearman Rank Correlation for NCAA Basketball ranking methods
          </Typography>
        </Toolbar>
      </AppBar>
      <Grid container spacing={8} alignItems="center">
        <Grid item xs={12}>
          <Grid container justify="center" style={{marginTop: 100}}>
            <Paper>
              <Table>
                <TableHead>
                  <TableRow>
                    <CustomTableCell></CustomTableCell>
                    <CustomTableCell align="right">Ken Pomeroy</CustomTableCell>
                    <CustomTableCell align="right">BPI</CustomTableCell>
                    <CustomTableCell align="right">RPI</CustomTableCell>
                    <CustomTableCell align="right">NET</CustomTableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  <TableRow>
                    <FirstColTableCell>Sagarin</FirstColTableCell>
                    <CustomTableCell align="right">{items['Sagarin_RK']['Pomeroy_RK']}</CustomTableCell>
                    <CustomTableCell align="right">{items['Sagarin_RK']['BPI_RK']}</CustomTableCell>
                    <CustomTableCell align="right">{items['Sagarin_RK']['RPI']}</CustomTableCell>
                    <CustomTableCell align="right">{items['Sagarin_RK']['NET Rank']}</CustomTableCell>
                  </TableRow>

                  <TableRow>
                    <FirstColTableCell>Ken Pomeroy</FirstColTableCell>
                    <CustomTableCell align="right">—</CustomTableCell>
                    <CustomTableCell align="right">{items['Pomeroy_RK']['BPI_RK']}</CustomTableCell>
                    <CustomTableCell align="right">{items['Pomeroy_RK']['RPI']}</CustomTableCell>
                    <CustomTableCell align="right">{items['Pomeroy_RK']['NET Rank']}</CustomTableCell>
                  </TableRow>

                  <TableRow>
                    <FirstColTableCell>BPI</FirstColTableCell>
                    <CustomTableCell align="right">—</CustomTableCell>
                    <CustomTableCell align="right">—</CustomTableCell>
                    <CustomTableCell align="right">{items['BPI_RK']['RPI']}</CustomTableCell>
                    <CustomTableCell align="right">{items['BPI_RK']['NET Rank']}</CustomTableCell>
                  </TableRow>

                  <TableRow>
                    <FirstColTableCell>RPI</FirstColTableCell>
                    <CustomTableCell align="right">—</CustomTableCell>
                    <CustomTableCell align="right">—</CustomTableCell>
                    <CustomTableCell align="right">—</CustomTableCell>
                    <CustomTableCell align="right">{items['RPI']['NET Rank']}</CustomTableCell>
                  </TableRow>

                </TableBody>
              </Table>
            </Paper>
          </Grid>
        </Grid>
        <Grid item xs={12}>
          <Grid container justify="center">
            <Paper>
              <img style={{width: "100%"}} src="/correlation.png" />
            </Paper>
          </Grid>
        </Grid>
      </Grid>
      </div>
    )
  }
}
