import React from 'react';
import ReactDOM from 'react-dom';
import DashboardView from "./components/DashboardView"
import { BrowserRouter } from 'react-router-dom'

import Main from "./components/Main"
import "./css/index.css"

ReactDOM.render(
  <BrowserRouter>
    <Main />
  </BrowserRouter>,
  document.getElementById('root')
);