import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import TableFooter from '@material-ui/core/TableFooter';
import TablePagination from '@material-ui/core/TablePagination';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import TablePaginationActionsWrapped from './Paginator.jsx';

const CustomTableCell = withStyles(theme => ({
  head: {
    backgroundColor: theme.palette.primary.main,
    borderBottomColor: theme.palette.common.white,
    color: theme.palette.common.white,
    fontSize: 14,
  },
  body: {
    fontSize: 12,
  },
}))(TableCell);

const FirstColTableCell = withStyles(theme => ({
  body: {
    backgroundColor: theme.palette.primary.main,
    borderColor: theme.palette.primary.main,
    color: theme.palette.common.white,
    fontSize: 14,
    width: 220
  },
}))(TableCell);

export default class Rankings extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoaded: false,
      teams: null,
      page: 0,
      rowsPerPage: 5
    }
    this.handleChangePage = this.handleChangePage.bind(this);
    this.handleChangeRowsPerPage = this.handleChangeRowsPerPage.bind(this);
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

  handleChangePage(event, page) {
    this.setState({ page });
  }

  handleChangeRowsPerPage(event) {
    this.setState({ rowsPerPage: parseInt(event.target.value) });
  }

  render() {
    const { rowsPerPage, page } = this.state;
    const teams = this.state.teams || {};
    const teamNames = Object.keys(teams);
    const rows = teamNames.map(name => {
      const updated =  teams[name];
      updated['team'] = name;
      return updated;
    })
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
                  {rows.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map(row => {
                    return <TableRow key={row['team'].replace(' ', '_')}>
                      <FirstColTableCell>{row['team']}</FirstColTableCell>
                      <CustomTableCell align="right">{row['Sagarin_RK']}</CustomTableCell>
                      <CustomTableCell align="right">{row['Pomeroy_RK']}</CustomTableCell>
                      <CustomTableCell align="right">{row['RPI']}</CustomTableCell>
                      <CustomTableCell align="right">{row['BPI_RK']}</CustomTableCell>
                      <CustomTableCell align="right">{row['NET Rank']}</CustomTableCell>
                    </TableRow>
                  })}
                </TableBody>
                <TableFooter>
                  <TableRow>
                    <TablePagination
                      rowsPerPageOptions={[5, 10, 25]}
                      colSpan={3}
                      count={rows.length}
                      rowsPerPage={rowsPerPage}
                      page={page}
                      SelectProps={{
                        native: true,
                      }}
                      onChangePage={this.handleChangePage}
                      onChangeRowsPerPage={this.handleChangeRowsPerPage}
                      ActionsComponent={TablePaginationActionsWrapped}
                    />
                  </TableRow>
                </TableFooter>
              </Table>
            </Paper>
          </Grid>
        </Grid>
      </Grid>
      </div>
    )
  }
}
