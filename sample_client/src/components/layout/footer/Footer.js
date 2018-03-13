import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import {Col, Container, Row} from "reactstrap";

class Footer extends Component {
    render() {
        return (
            <div className="Footer">
                <footer>
                    <Container fluid className='text-white'>
                        <Row className='bg-fl-light p-4'>
                            <Col>
                                <p className="text-center mb-4">
                                    Find us on:
                                    <a href="#" className="social">
                                        <i className="fa fa-facebook" aria-hidden="true"></i>
                                    </a>
                                    <a href="#" className="social"><i className="fa fa-twitter" aria-hidden="true"></i></a>
                                    <a href="#" className="social"><i className="fa fa-linkedin" aria-hidden="true"></i></a>
                                    <a href="#" className="social"><i className="fa fa-instagram" aria-hidden="true"></i></a>
                                </p>
                                <p className="text-center mb-0">
                                    <Link to="/">Home</Link>
                                    <span className="mx-2">|</span>
                                    <a href="#">Articles</a>
                                    <span className="mx-2">|</span>
                                    <Link to="/about">About Us</Link>
                                    <span className="mx-2">|</span>
                                    <Link to="/profile">My Profile</Link>
                                    <span className="mx-2">|</span>
                                    <a href="#">Privacy Policy</a>
                                </p>
                            </Col>
                        </Row>
                        <div className="row bg-fl-dark p-3">
                            <div className="col text-center">Flofinder 2017. All Rights Reserved.</div>
                        </div>
                    </Container>
                </footer>
            </div>
        );
    }
}

export default Footer;
