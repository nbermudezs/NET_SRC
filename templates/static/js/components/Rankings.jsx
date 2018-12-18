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
    border: 0,
    color: theme.palette.common.white,
  },
  body: {
    fontSize: 14,
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

export default class Rankings extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoaded: false,
      teams: null
    }
  }
  
  componentWillMount() {
    fetch("/ranking.json")
      .then(res => res.json())
      .then(res => {
        this.setState({
          teams: res
        })
      });
  }
  
  render() {
    const teams = this.state.teams || {};
    const teamNames = Object.keys(teams);
    return (
      <div>
      <AppBar position="sticky">
        <Toolbar>
          <Typography variant="h6" color="inherit">
            NCAA Basketball ranking methods
          </Typography>
        </Toolbar>
      </AppBar>
      <Grid container spacing={8} alignItems="center">
        <Grid item xs={12}>
          <Grid container justify="center">
            <Paper style={{marginTop: 100}}>
              <Table>
                <TableHead>
                  <TableRow>
                    <CustomTableCell>Team</CustomTableCell>
                    <CustomTableCell align="right">Sagarin RK</CustomTableCell>
                    <CustomTableCell align="right">Pomeroy RK</CustomTableCell>
                    <CustomTableCell align="right">RPI RK</CustomTableCell>
                    <CustomTableCell align="right">BPI RK</CustomTableCell>
                    <CustomTableCell align="right">NET RK</CustomTableCell>
                  </TableRow>
                </TableHead>
                
                <TableBody>
                  {teamNames.map(team => {
                    return <TableRow key={team.replace(' ', '_')}>
                      <FirstColTableCell>{team}</FirstColTableCell>
                      <CustomTableCell align="right">{teams[team]['Sagarin_RK']}</CustomTableCell>
                      <CustomTableCell align="right">{teams[team]['Pomeroy_RK']}</CustomTableCell>
                      <CustomTableCell align="right">{teams[team]['RPI']}</CustomTableCell>
                      <CustomTableCell align="right">{teams[team]['BPI_RK']}</CustomTableCell>
                      <CustomTableCell align="right">{teams[team]['NET Rank']}</CustomTableCell>
                    </TableRow>
                  })}
                </TableBody>
              </Table>
            </Paper>
          </Grid>
        </Grid>
      </Grid>
      </div>
    )
  }
}
