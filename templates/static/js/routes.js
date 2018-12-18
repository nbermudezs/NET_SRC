import React from 'react';
import { HashRouter, Route, hashHistory, IndexRoute } from 'react-router-dom';
import Home from './components/Home';
import Rankings from './components/Rankings';
// import more components
export default (
    <HashRouter history={hashHistory}>
     <div>
      <Route path='/' exact component={Home} />
      <Route path='/rankings' component={Rankings} />
     </div>
    </HashRouter>
);
