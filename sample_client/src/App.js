import React, { Component } from 'react';
// import "bootstrap/dist/css/bootstrap.css";
import 'react-widgets/dist/css/react-widgets.css';
import 'react-select/dist/react-select.css'
import "../global/style.css";
import NavBar from "./components/layout/navbar/NavBar";
import Container from "./components/layout/container/Container";
import Footer from "./components/layout/footer/Footer";

class App extends Component {
  render() {
    return (
      <div className="App">
          <div className='wrapper'>
              <NavBar />
              <Container />
          </div>
          <Footer />
      </div>
    );
  }
}

export default App;
