import React, { Component } from 'react';
import Title from "../../components/partials/Title";

class HomeView extends Component {
  render() {
    return (
      <div className="HomeView">
        <Title title='Home'/>
        <div className="container">
          <div className="page-content">
            HomeView content
          </div>
        </div>
      </div>
    );
  }
}

export default HomeView;
